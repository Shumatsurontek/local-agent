from dataclasses import dataclass
from typing import Optional

from agno.agent import Agent
from agno.document.chunking.agentic import AgenticChunking
from agno.embedder.ollama import OllamaEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.ollama import Ollama
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.pgvector import PgVector, SearchType, HNSW
from .settings import get_model

@dataclass
class WhatsAppMessage:
    from_number: str
    message_id: str
    timestamp: str
    text: str

    @classmethod
    def from_webhook(cls, webhook_data: dict) -> Optional['WhatsAppMessage']:
        try:
            message = webhook_data['entry'][0]['changes'][0]['value']['messages'][0]
            return cls(
                from_number=message['from'],
                message_id=message['id'],
                timestamp=message['timestamp'],
                text=message['text']['body']
            )
        except (KeyError, IndexError):
            return None

class WhatsAppAgent:
    name = "whatsapp"
    description = "WhatsApp Agent"
    model = get_model()
    tools = [
        ReasoningTools(
            add_instructions=True,
        )
    ]
    instructions = [
        "Include sources in your response when using knowledge.",
        "Always search your knowledge before answering questions.",
        "Use reasoning to analyze search results before responding.",
        "Format responses appropriately for WhatsApp (concise and clear).",
        "Remember user preferences and past interactions."
    ]

    def __init__(
        self,
        db_url: str = "postgresql+psycopg://ai:ai@localhost:5532/ai",
        memory_path: str = "data/whatsapp_memory.db",
        knowledge_urls: list[str] = None
    ):
        # Configure embedder using local Ollama
        self.embedder = OllamaEmbedder(
            id="nomic-embed-text",  # Efficient local embedding model
            host="http://localhost:11434"  # <-- utiliser host, pas base_url
        )
        
        # Configure vector database with HNSW index for better performance
        self.vector_db = PgVector(
            table_name="whatsapp_knowledge",
            schema="public",
            db_url=db_url,
            search_type=SearchType.hybrid,
            embedder=self.embedder,
            vector_index=HNSW(
                m=16,  # Number of connections per element
                ef_construction=100  # Size of dynamic candidate list for construction
            ),
            vector_score_weight=0.7,  # Bias towards vector similarity in hybrid search
            prefix_match=True  # Enable prefix matching for better keyword search
        )
        
        # Configure shared memory with SQLite
        self.memory_db = SqliteMemoryDb(
            table_name="whatsapp_memory",
            db_file=memory_path
        )
        self.memory = Memory(db=self.memory_db)
        
        # Setup knowledge base with Agentic Chunking
        self.knowledge_base = PDFUrlKnowledgeBase(
            urls=knowledge_urls or [],
            vector_db=self.vector_db,
            chunking_strategy=AgenticChunking(
                model=Ollama(id="mistral:latest"),  # Use Mistral for chunking
                max_chunk_size=2000  # Smaller chunks for better context
            )
        )
        
        # Initialize the agent with Agentic RAG capabilities
        self.agent = Agent(
            model=self.model,
            name="WhatsAppAgent",
            knowledge=self.knowledge_base,
            memory=self.memory,
            tools=self.tools,
            enable_user_memories=True,
            search_knowledge=True,
            show_tool_calls=True,
            markdown=True,
            instructions=self.instructions,
            description="You are a helpful WhatsApp assistant with access to knowledge bases and memory of past interactions."
        )

    async def load_knowledge(self, recreate: bool = False) -> None:
        """Load or reload the knowledge base asynchronously"""
        await self.knowledge_base.aload(recreate=recreate)

    async def handle_message(self, message: str, user_id: str) -> str:
        """Process a message and return the response asynchronously"""
        return await self.agent.aget_response(
            message,
            user_id=user_id,
            stream=False,
            show_full_reasoning=True
        )

    async def handle_webhook(self, webhook_data: dict) -> Optional[dict]:
        """Handle incoming WhatsApp webhook data and return response asynchronously"""
        message = WhatsAppMessage.from_webhook(webhook_data)
        if not message:
            return None
            
        response = await self.handle_message(
            message.text,
            user_id=message.from_number
        )
        
        return {
            "to": message.from_number,
            "body": response
        }

    def get_user_memories(self, user_id: str) -> list[dict]:
        """Get all memories for a specific user"""
        return self.memory.get_user_memories(user_id=user_id)

    def run(self, message: str, **kwargs):
        """
        Point d'entrée standard pour l'API.
        Délègue à self.agent (Agno) en mode synchrone.
        """
        # Si tu veux supporter le streaming ou d'autres kwargs, adapte ici
        return self.agent.run(message, **kwargs)

# Create a singleton instance
whatsapp_agent = WhatsAppAgent() 