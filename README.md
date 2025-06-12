# 🤖 Multi-Agent System avec Agno

Un système multi-agents intelligent utilisant le framework [Agno](https://docs.agno.com) et Ollama pour créer des agents spécialisés capables de collaborer sur diverses tâches.

## ✨ Fonctionnalités

- **5 Agents Spécialisés** : Chaque agent a ses propres outils et compétences
- **Framework Agno** : Architecture moderne et performante pour les systèmes multi-agents
- **Ollama Local** : Modèles de langage exécutés localement (pas de dépendance cloud)
- **Interface CLI** : Interface en ligne de commande intuitive avec Typer
- **Interface Riche** : Affichage coloré et structuré avec Rich
- **Équipe Collaborative** : Les agents peuvent travailler ensemble sur des tâches complexes

## 🤖 Agents Disponibles

| Agent | Description | Outils |
|-------|-------------|--------|
| `general` | 🤖 Assistant général | Conversation générale |
| `search` | 🔍 Recherche web | DuckDuckGo |
| `finance` | 💰 Analyse financière | YFinance (actions, nouvelles, analyses) |
| `code` | 💻 Programmation | Python (calculs, scripts) |
| `system` | ⚙️ Administration système | Shell/Terminal |
| `team` | 👥 Équipe collaborative | Tous les agents ensemble |

## 🚀 Installation Rapide

### 1. Prérequis

- Python 3.10+
- Ollama installé ([https://ollama.ai](https://ollama.ai))

### 2. Installation Automatique

```bash
# Cloner le projet
git clone <votre-repo>
cd local-agent-agno

# Lancer le script de setup
python setup.py
```

Le script va :
- ✅ Vérifier/installer Ollama
- ✅ Installer les dépendances Python
- ✅ Télécharger les modèles nécessaires (mistral, llama3.2, codellama)
- ✅ Tester la configuration

### 3. Installation Manuelle

```bash
# Installer Ollama (macOS)
brew install ollama

# Ou télécharger depuis https://ollama.ai

# Démarrer Ollama
ollama serve

# Télécharger les modèles
ollama pull mistral
ollama pull llama3.2
ollama pull codellama

# Installer les dépendances Python
pip install -r requirements.txt
# ou avec uv
uv sync
```

## 🎯 Utilisation

### Lister les Agents

```bash
python main.py list-agents
```

### Chat avec un Agent Spécifique

```bash
# Agent général
python main.py chat --agent general

# Agent de recherche
python main.py chat --agent search

# Agent financier
python main.py chat --agent finance

# Agent de programmation
python main.py chat --agent code

# Agent système
python main.py chat --agent system

# Équipe collaborative
python main.py chat --agent team
```

### Changer de Modèle

```bash
# Utiliser llama3.2 au lieu de mistral
python main.py chat --agent general --model llama3.2

# Utiliser codellama pour la programmation
python main.py chat --agent code --model codellama
```

### Démonstration Rapide

```bash
python main.py demo
```

## 💡 Exemples d'Utilisation

### Agent de Recherche
```bash
python main.py chat --agent search
> Trouve les dernières nouvelles sur l'intelligence artificielle
```

### Agent Financier
```bash
python main.py chat --agent finance
> Donne-moi le prix actuel d'Apple (AAPL) et les recommandations des analystes
```

### Agent de Programmation
```bash
python main.py chat --agent code
> Écris une fonction Python pour calculer la suite de Fibonacci
```

### Agent Système
```bash
python main.py chat --agent system
> Montre-moi l'utilisation du disque et les processus actifs
```

### Équipe Collaborative
```bash
python main.py chat --agent team
> Recherche des informations sur Tesla, analyse son cours de bourse, et écris un script Python pour tracer l'évolution du prix
```

## 🏗️ Architecture

Le projet utilise le framework Agno qui offre :

- **Agents Lightning Fast** : Instantiation en ~3μs
- **Multi-Modal** : Support texte, image, audio, vidéo
- **Reasoning Intégré** : Capacités de raisonnement avancées
- **Memory & Storage** : Mémoire persistante et stockage de session
- **Model Agnostic** : Support de 23+ fournisseurs de modèles

### Structure du Code

```
local-agent-agno/
├── main.py              # Application principale avec CLI
├── setup.py             # Script d'installation automatique
├── pyproject.toml       # Configuration du projet
├── requirements.txt     # Dépendances Python
└── README.md           # Documentation
```

## ⚙️ Configuration

### Modèles Supportés

- `mistral` (par défaut) - Modèle général équilibré
- `llama3.2` - Alternative performante
- `codellama` - Spécialisé pour le code

### Variables d'Environnement

```bash
# Optionnel : URL personnalisée d'Ollama
export OLLAMA_HOST=http://localhost:11434
```

## 🔧 Développement

### Ajouter un Nouvel Agent

1. Modifier la méthode `_create_agents()` dans `AgentManager`
2. Ajouter les outils nécessaires
3. Définir les instructions spécialisées
4. Mettre à jour `list_agents()`

### Exemple d'Agent Personnalisé

```python
# Agent de traduction
translation_agent = Agent(
    name="TranslationAgent",
    model=self.model,
    tools=[],  # Pas d'outils externes nécessaires
    instructions=[
        "Tu es un expert en traduction multilingue.",
        "Traduis avec précision en préservant le contexte.",
        "Indique la langue source détectée."
    ],
    markdown=True
)
```

## 🐛 Dépannage

### Ollama ne démarre pas
```bash
# Vérifier le statut
ollama list

# Redémarrer le service
ollama serve
```

### Modèle non trouvé
```bash
# Télécharger le modèle manquant
ollama pull mistral
```

### Erreurs d'import
```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

## 📚 Ressources

- [Documentation Agno](https://docs.agno.com)
- [Ollama](https://ollama.ai)
- [Modèles disponibles](https://ollama.ai/library)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amazing-agent`)
3. Commit les changements (`git commit -m 'Add amazing agent'`)
4. Push vers la branche (`git push origin feature/amazing-agent`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

**🚀 Prêt à explorer l'intelligence artificielle locale avec des agents spécialisés !**
