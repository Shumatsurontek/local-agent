"use client"

import { useEffect, useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { toast } from "sonner"
import { Message, apiService } from "@/lib/api"
import { cn } from "@/lib/utils"
import { 
  Bot, 
  User, 
  Send, 
  X, 
  Loader2, 
  MessageSquare,
  Clock,
  CheckCheck
} from "lucide-react"

interface ChatInterfaceProps {
  agentName: string
  agentId: string
  onClose: () => void
}

export function ChatInterface({ agentName, agentId, onClose }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    apiService.connect()
    const unsubscribe = apiService.onMessage((message) => {
      setMessages((prev) => [...prev, message])
      setIsTyping(false)
    })

    return () => {
      unsubscribe()
      apiService.disconnect()
    }
  }, [])

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    if (scrollAreaRef.current) {
      const scrollElement = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]')
      if (scrollElement) {
        scrollElement.scrollTop = scrollElement.scrollHeight
      }
    }
  }, [messages, isTyping])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: "user",
      timestamp: new Date().toISOString(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)
    setIsTyping(true)

    try {
      await apiService.sendMessage(input, agentId)
    } catch (error) {
      toast.error("Erreur lors de l'envoi du message")
      console.error(error)
      setIsTyping(false)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const getAgentIcon = () => {
    switch (agentId) {
      case "1": return Bot
      case "2": return MessageSquare
      case "3": return MessageSquare
      default: return Bot
    }
  }

  const getAgentColor = () => {
    switch (agentId) {
      case "1": return "from-blue-500 to-cyan-500"
      case "2": return "from-green-500 to-emerald-500"
      case "3": return "from-purple-500 to-pink-500"
      default: return "from-blue-500 to-cyan-500"
    }
  }

  const AgentIcon = getAgentIcon()

  return (
    <Card className="w-full max-w-4xl mx-auto h-[700px] flex flex-col shadow-2xl border-0 bg-gradient-to-br from-card to-card/90 backdrop-blur-sm">
      {/* Header */}
      <CardHeader className="flex-none border-b bg-gradient-to-r from-muted/50 to-muted/30 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Avatar className={`h-10 w-10 bg-gradient-to-r ${getAgentColor()}`}>
              <AvatarFallback className="bg-transparent">
                <AgentIcon className="h-5 w-5 text-white" />
              </AvatarFallback>
            </Avatar>
            <div>
              <CardTitle className="text-lg font-semibold">{agentName}</CardTitle>
              <div className="flex items-center gap-2 mt-1">
                <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse" />
                <span className="text-xs text-muted-foreground">En ligne</span>
              </div>
            </div>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose} className="h-8 w-8 p-0">
            <X className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>

      {/* Messages */}
      <CardContent className="flex-1 p-0 overflow-hidden">
        <ScrollArea className="h-full" ref={scrollAreaRef}>
          <div className="p-6 space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <div className={`mx-auto mb-4 h-16 w-16 rounded-full bg-gradient-to-r ${getAgentColor()} flex items-center justify-center`}>
                  <AgentIcon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-lg font-semibold mb-2">Commencez une conversation</h3>
                <p className="text-muted-foreground text-sm">
                  Posez votre première question à {agentName}
                </p>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={cn(
                  "flex w-full gap-3 animate-in fade-in-0 slide-in-from-bottom-1",
                  message.role === "user" ? "justify-end" : "justify-start"
                )}
              >
                {message.role === "assistant" && (
                  <Avatar className={`h-8 w-8 bg-gradient-to-r ${getAgentColor()}`}>
                    <AvatarFallback className="bg-transparent">
                      <AgentIcon className="h-4 w-4 text-white" />
                    </AvatarFallback>
                  </Avatar>
                )}
                
                <div className={cn(
                  "max-w-[80%] space-y-1",
                  message.role === "user" && "flex flex-col items-end"
                )}>
                  <div
                    className={cn(
                      "rounded-2xl px-4 py-3 text-sm",
                      message.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted"
                    )}
                  >
                    <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                  </div>
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <Clock className="h-3 w-3" />
                    <span>{new Date(message.timestamp).toLocaleTimeString('fr-FR', { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}</span>
                    {message.role === "user" && (
                      <CheckCheck className="h-3 w-3 text-green-500" />
                    )}
                  </div>
                </div>

                {message.role === "user" && (
                  <Avatar className="h-8 w-8 bg-gradient-to-r from-gray-500 to-gray-600">
                    <AvatarFallback className="bg-transparent">
                      <User className="h-4 w-4 text-white" />
                    </AvatarFallback>
                  </Avatar>
                )}
              </div>
            ))}

            {isTyping && (
              <div className="flex gap-3 animate-in fade-in-0">
                <Avatar className={`h-8 w-8 bg-gradient-to-r ${getAgentColor()}`}>
                  <AvatarFallback className="bg-transparent">
                    <AgentIcon className="h-4 w-4 text-white" />
                  </AvatarFallback>
                </Avatar>
                <div className="bg-muted rounded-2xl px-4 py-3">
                  <div className="flex space-x-1">
                    <div className="h-2 w-2 bg-muted-foreground/60 rounded-full animate-bounce" />
                    <div className="h-2 w-2 bg-muted-foreground/60 rounded-full animate-bounce [animation-delay:0.1s]" />
                    <div className="h-2 w-2 bg-muted-foreground/60 rounded-full animate-bounce [animation-delay:0.2s]" />
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
      </CardContent>

      <Separator />

      {/* Input */}
      <CardFooter className="flex-none p-6 bg-gradient-to-r from-muted/20 to-muted/10 rounded-b-lg">
        <form onSubmit={handleSubmit} className="w-full flex gap-3">
          <div className="flex-1 relative">
            <Textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Tapez votre message..."
              className="resize-none pr-12 min-h-[44px] max-h-32"
              rows={1}
              disabled={isLoading}
            />
            <Badge 
              variant="secondary" 
              className="absolute bottom-2 right-2 text-xs px-2 py-0.5"
            >
              {input.length}/1000
            </Badge>
          </div>
          <Button 
            type="submit" 
            disabled={isLoading || !input.trim()}
            className="h-11 px-6"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </form>
      </CardFooter>
    </Card>
  )
} 