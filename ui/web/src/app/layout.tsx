import type { Metadata } from "next";
import "./globals.css";
import { Inter } from "next/font/google";
import { ThemeProvider } from "@/components/theme-provider";
import { cn } from "@/lib/utils";

const fontSans = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Système Multi-Agents | IA Avancée",
  description: "Plateforme d'intelligence artificielle avec agents spécialisés pour tous vos besoins",
  keywords: ["IA", "Intelligence Artificielle", "Agents", "Chat", "Assistant", "Recherche", "Création"],
  authors: [{ name: "Système Multi-Agents" }],
  creator: "Système Multi-Agents",
  openGraph: {
    type: "website",
    locale: "fr_FR",
    url: "https://multi-agents.ai",
    title: "Système Multi-Agents | IA Avancée",
    description: "Plateforme d'intelligence artificielle avec agents spécialisés",
    siteName: "Système Multi-Agents",
  },
  twitter: {
    card: "summary_large_image",
    title: "Système Multi-Agents | IA Avancée",
    description: "Plateforme d'intelligence artificielle avec agents spécialisés",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    google: "your-google-verification-code",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="manifest" href="/site.webmanifest" />
        <meta name="theme-color" content="#000000" />
        <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
      </head>
      <body 
        className={cn(
          "min-h-screen bg-background font-sans antialiased",
          fontSans.variable
        )}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
