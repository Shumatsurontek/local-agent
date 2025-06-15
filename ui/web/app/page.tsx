"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { useState } from "react"
import { ChatInterface } from "@/components/chat/chat-interface"
import { ThemeToggle } from "@/components/theme-toggle"
import { Toaster } from "sonner"
import { 
  Bot, 
  Search, 
  Sparkles, 
  MessageSquare, 
  Zap, 
  Brain,
  ArrowRight,
  Star,
  Users,
  Lightbulb,
  Target,
  DollarSign,
  Code,
  Terminal,
  GitBranch,
  ExternalLink
} from "lucide-react"

const agents = [
  {
    id: "general",
    name: "Assistant Général",
    description: "Agent conversationnel polyvalent pour l'assistance générale et les informations",
    icon: Bot,
    color: "bg-gradient-to-br from-blue-500 to-cyan-500",
    hoverColor: "hover:from-blue-600 hover:to-cyan-600",
    badge: "Généraliste",
    badgeColor: "bg-blue-50 text-blue-700 border-blue-200",
    features: ["Conversation naturelle", "Assistance générale", "Informations variées"],
    stats: "Modèle: Qwen3:8b",
    model: "qwen3:8b"
  },
  {
    id: "search", 
    name: "Agent de Recherche",
    description: "Expert en recherche web avec DuckDuckGo pour des informations en temps réel",
    icon: Search,
    color: "bg-gradient-to-br from-green-500 to-emerald-500",
    hoverColor: "hover:from-green-600 hover:to-emerald-600",
    badge: "Recherche Web",
    badgeColor: "bg-green-50 text-green-700 border-green-200",
    features: ["Recherche DuckDuckGo", "Informations temps réel", "Veille web"],
    stats: "Modèle: Qwen3:8b",
    model: "qwen3:8b"
  },
  {
    id: "finance",
    name: "Agent Financier", 
    description: "Spécialiste en analyse financière et données boursières avec YFinance",
    icon: DollarSign,
    color: "bg-gradient-to-br from-yellow-500 to-orange-500",
    hoverColor: "hover:from-yellow-600 hover:to-orange-600",
    badge: "Finance",
    badgeColor: "bg-yellow-50 text-yellow-700 border-yellow-200",
    features: ["Analyse boursière", "Données YFinance", "Informations financières"],
    stats: "Modèle: Qwen3:8b",
    model: "qwen3:8b"
  },
  {
    id: "code",
    name: "Agent de Code",
    description: "Expert en exécution Python, calculs mathématiques et assistance programmation",
    icon: Code,
    color: "bg-gradient-to-br from-purple-500 to-pink-500",
    hoverColor: "hover:from-purple-600 hover:to-pink-600",
    badge: "Développement",
    badgeColor: "bg-purple-50 text-purple-700 border-purple-200",
    features: ["Exécution Python", "Calculs mathématiques", "Assistance dev"],
    stats: "Modèle: Qwen2.5-Coder:7b",
    model: "qwen2.5-coder:7b"
  },
  {
    id: "system",
    name: "Agent Système",
    description: "Administrateur système pour l'exécution de commandes shell et gestion de fichiers",
    icon: Terminal,
    color: "bg-gradient-to-br from-red-500 to-rose-500",
    hoverColor: "hover:from-red-600 hover:to-rose-600",
    badge: "SysAdmin",
    badgeColor: "bg-red-50 text-red-700 border-red-200",
    features: ["Commandes shell", "Administration système", "Gestion fichiers"],
    stats: "Modèle: Phi3:mini",
    model: "phi3:mini"
  },
  {
    id: "research_team",
    name: "Équipe Recherche",
    description: "Équipe collaborative multi-agents combinant recherche, analyse et synthèse",
    icon: Users,
    color: "bg-gradient-to-br from-indigo-500 to-purple-500",
    hoverColor: "hover:from-indigo-600 hover:to-purple-600",
    badge: "Équipe",
    badgeColor: "bg-indigo-50 text-indigo-700 border-indigo-200",
    features: ["Collaboration multi-agents", "Recherche approfondie", "Synthèse intelligente"],
    stats: "Search + Finance + General",
    model: "team"
  },
]

const features = [
  {
    icon: Zap,
    title: "Performance Ultra-Rapide",
    description: "Réponses en moins de 2 secondes avec notre infrastructure Ollama optimisée"
  },
  {
    icon: Brain,
    title: "Framework Agno",
    description: "Construit sur le framework Agno moderne pour une architecture robuste"
  },
  {
    icon: Users,
    title: "Collaboration Multi-Agents",
    description: "Équipes d'agents qui collaborent pour résoudre vos problèmes complexes"
  },
  {
    icon: Target,
    title: "Agents Spécialisés",
    description: "Chaque agent est optimisé avec des outils spécifiques à son domaine"
  }
]

export default function Home() {
  const [selectedAgent, setSelectedAgent] = useState<typeof agents[0] | null>(null)
  const [showChat, setShowChat] = useState(false)

  const handleStartChat = (agent: typeof agents[0]) => {
    setSelectedAgent(agent)
    setShowChat(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
      {/* Theme Toggle */}
      <div className="fixed top-6 right-6 z-50">
        <ThemeToggle />
      </div>

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-16">
        <div className="absolute inset-0 bg-grid-slate-100 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))] dark:bg-grid-slate-700/25 dark:[mask-image:linear-gradient(0deg,rgba(255,255,255,0.1),rgba(255,255,255,0.5))]" />
        
        <div className="relative mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <div className="mb-8 flex justify-center">
              <div className="relative rounded-full px-3 py-1 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20 dark:text-gray-300 dark:ring-gray-800 dark:hover:ring-gray-700">
                <span className="flex items-center gap-1">
                  <Lightbulb className="h-4 w-4" />
                  Alimenté par Ollama + Framework Agno
                </span>
              </div>
            </div>
            
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
              Système{" "}
              <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-600 bg-clip-text text-transparent">
                Multi-Agents
              </span>
            </h1>
            
            <p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
              Découvrez la puissance de l'intelligence artificielle spécialisée avec Agno. 
              Chaque agent est optimisé avec des outils spécifiques pour exceller dans son domaine.
            </p>
            
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Button 
                size="lg" 
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg"
                onClick={() => document.getElementById('agents')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Commencer maintenant
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <div className="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400">
                <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                <span className="font-semibold">5 Agents</span>
                <span>+ 1 Équipe</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Agents Section */}
      <section id="agents" className="py-24 bg-white/50 dark:bg-slate-900/50">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              Choisissez votre expert IA
            </h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
              Agents spécialisés avec outils dédiés et équipe collaborative
            </p>
          </div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent) => {
              const IconComponent = agent.icon
              return (
                <Card
                  key={agent.id}
                  className="group relative overflow-hidden border-0 bg-white/80 backdrop-blur-sm shadow-lg shadow-slate-200/50 transition-all duration-500 hover:shadow-xl hover:shadow-slate-300/50 hover:-translate-y-1 dark:bg-slate-800/50 dark:shadow-slate-800/50"
                >
                  <CardHeader className="space-y-4 pb-4">
                    <div className="flex items-start justify-between">
                      <div className={`p-3 rounded-xl ${agent.color} text-white shadow-lg`}>
                        <IconComponent className="h-6 w-6" />
                      </div>
                      <Badge 
                        variant="secondary" 
                        className={`${agent.badgeColor} border font-medium`}
                      >
                        {agent.badge}
                      </Badge>
                    </div>
                    
                    <div>
                      <CardTitle className="text-xl font-semibold text-gray-900 dark:text-white group-hover:text-blue-600 transition-colors">
                        {agent.name}
                      </CardTitle>
                      <CardDescription className="mt-2 text-gray-600 dark:text-gray-300">
                        {agent.description}
                      </CardDescription>
                    </div>
                  </CardHeader>
                  
                  <CardContent className="space-y-6">
                    <div className="space-y-3">
                      <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                        Capacités principales
                      </p>
                      <div className="flex flex-wrap gap-1.5">
                        {agent.features.map((feature, index) => (
                          <Badge 
                            key={index} 
                            variant="outline" 
                            className="text-xs py-1 px-2 bg-gray-50 text-gray-700 border-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700"
                          >
                            {feature}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div className="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-700">
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        {agent.stats}
                      </div>
                      <Button 
                        onClick={() => handleStartChat(agent)}
                        className={`${agent.color} ${agent.hoverColor} text-white border-0 shadow-md hover:shadow-lg transition-all duration-300`}
                      >
                        <MessageSquare className="h-4 w-4 mr-2" />
                        Chat
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              Pourquoi notre système ?
            </h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
              Une plateforme conçue pour l'excellence avec le framework Agno
            </p>
          </div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
            {features.map((feature, index) => {
              const IconComponent = feature.icon
              return (
                <div 
                  key={index}
                  className="relative group text-center"
                >
                  <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-2xl bg-gradient-to-br from-blue-50 to-purple-50 text-blue-600 dark:from-blue-950 dark:to-purple-950 dark:text-blue-400 mb-6 transition-transform group-hover:scale-110">
                    <IconComponent className="h-8 w-8" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Footer with GitHub Link */}
      <footer className="border-t border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50">
        <div className="mx-auto max-w-7xl px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <GitBranch className="h-5 w-5 text-gray-600 dark:text-gray-400" />
              <span className="text-gray-600 dark:text-gray-400">Open Source</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Explorez le code source
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-6 max-w-2xl mx-auto">
              Ce projet est open source et construit avec le framework Agno. 
              Découvrez l'architecture, contribuez ou déployez votre propre instance.
            </p>
            <Button 
              variant="outline"
              className="bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
              onClick={() => window.open('https://github.com/Shumatsurontek/local-agent/tree/feat/agno-integration', '_blank')}
            >
              <GitBranch className="h-4 w-4 mr-2" />
              Voir sur GitHub
              <ExternalLink className="h-4 w-4 ml-2" />
            </Button>
          </div>
        </div>
      </footer>

      {/* Chat Modal */}
      {selectedAgent && showChat && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <ChatInterface
            agentName={selectedAgent.name}
            agentId={selectedAgent.id}
            onClose={() => setShowChat(false)}
          />
        </div>
      )}

      <Toaster richColors position="top-right" />
    </div>
  )
} 