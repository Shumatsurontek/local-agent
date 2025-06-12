"""
Streamlit interface for chatting with agents
"""

import streamlit as st
from agents import general_agent, search_agent, finance_agent, code_agent, system_agent
from teams import collaborative_team

# Page configuration
st.set_page_config(
    page_title="Multi-Agent System",
    page_icon="🤖",
    layout="wide"
)

# Available agents and teams
AGENTS = {
    "🤖 Agent Général": general_agent,
    "🔍 Agent de Recherche": search_agent,
    "💰 Agent Financier": finance_agent,
    "💻 Agent de Code": code_agent,
    "⚙️ Agent Système": system_agent
}

TEAMS = {
    "👥 Équipe Collaborative": collaborative_team
}

def main():
    st.title("🤖 Multi-Agent System")
    st.markdown("### Interface de chat avec les agents spécialisés")
    
    # Sidebar for agent selection
    with st.sidebar:
        st.header("Sélection")
        
        # Choose between agent or team
        mode = st.radio("Mode", ["Agents", "Équipes"])
        
        if mode == "Agents":
            selected_name = st.selectbox("Choisir un agent", list(AGENTS.keys()))
            selected_entity = AGENTS[selected_name]
        else:
            selected_name = st.selectbox("Choisir une équipe", list(TEAMS.keys()))
            selected_entity = TEAMS[selected_name]
        
        st.markdown("---")
        st.markdown(f"**{selected_name}**")
        st.markdown(f"*{selected_entity.description or 'Description non disponible'}*")
        
        # Show model info
        if hasattr(selected_entity, 'model'):
            model_name = getattr(selected_entity.model, 'id', 'Inconnu')
            st.markdown(f"**Modèle:** {model_name}")
        
        # Show tools
        if hasattr(selected_entity, 'tools') and selected_entity.tools:
            st.markdown("**Outils:**")
            for tool in selected_entity.tools:
                st.markdown(f"- {tool.__class__.__name__}")
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Tapez votre message..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get agent response
            with st.chat_message("assistant"):
                with st.spinner(f"{selected_entity.name} réfléchit..."):
                    try:
                        response = selected_entity.run(prompt)
                        st.markdown(response.content)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response.content
                        })
                    except Exception as e:
                        error_msg = f"❌ Erreur: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg
                        })
    
    with col2:
        st.subheader("Actions")
        
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.messages = []
            st.experimental_rerun()
        
        if st.button("📋 Exporter la conversation"):
            conversation = "\n\n".join([
                f"**{msg['role'].title()}:** {msg['content']}" 
                for msg in st.session_state.messages
            ])
            st.download_button(
                label="📄 Télécharger",
                data=conversation,
                file_name="conversation.md",
                mime="text/markdown"
            )
        
        st.markdown("---")
        st.subheader("Statistiques")
        st.metric("Messages", len(st.session_state.messages))
        
        user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
        assistant_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        
        st.metric("Messages utilisateur", user_msgs)
        st.metric("Réponses agent", assistant_msgs)

if __name__ == "__main__":
    main() 