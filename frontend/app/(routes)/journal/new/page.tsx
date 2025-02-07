"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ChevronLeft } from "lucide-react";
import Link from "next/link";
import { MOODS, MoodType } from "@/lib/constants/moods";
import Image from "next/image";
import { cn } from "@/lib/utils";
import socket from "@/lib/socket"; // Importa el cliente de Socket.IO
import { useJournalStore } from "@/lib/stores/journal-store";
import { verifyToken } from "@/lib/auth";
import { handleTokenRefresh } from "@/lib/api";
import { Loading } from "@/components/loading";



const getMoodButtonClass = (moodId: MoodType, isSelected: boolean) => {
  if (!isSelected) return "bg-secondary hover:bg-secondary/80";
  switch (moodId) {
    case "happy":
      return "bg-green-500 dark:bg-green-600";
    case "neutral":
      return "bg-yellow-500 dark:bg-yellow-600";
    case "sad":
      return "bg-blue-500 dark:bg-blue-600";
    case "angry":
      return "bg-red-500 dark:bg-red-600";
    default:
      return "bg-gray-500 dark:bg-gray-600";
  }
};

export default function NewJournalPage() {

  // editor
 
  const router = useRouter();
  const [content, setContent] = useState("");
  const [selectedMood, setSelectedMood] = useState<MoodType | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const setCurrentEntry = useJournalStore((state) => state.setCurrentEntry);

    useEffect(() => {
      const checkAuth = async () => {
        try {
          let isValidToken = await verifyToken();
          if (!isValidToken) {
            const refreshSuccess = await handleTokenRefresh();
            if (!refreshSuccess) {
              window.location.href = "/login";
              return;
            }
  
            isValidToken = await verifyToken();
            if (!isValidToken) throw new Error("Token verification failed");
          }
        } catch (error) {
          window.location.href = "/login";
        } finally {
          setIsLoading(false);
        }
      };
      checkAuth();
    }, []);
  
    if (isLoading) {
      return <Loading />;
    }

  const handleSubmit = async () => {
    if (!selectedMood || !content) return;

    setIsLoading(true);
    try {
      const newEntry = {
        mood: selectedMood,
        content,
      }

      setCurrentEntry(newEntry);

      socket.emit("generate_interaction", {
        content,
        state: MOODS.find((mood) => mood.id === selectedMood)?.value ?? 1,
      });

      router.push("/ia-feedback");
    } catch (error) {
      console.error("Error al enviar la interacción:", error);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-2xl mx-auto">

        {/* editor */}

        <Card className="border-none shadow-none">
          <CardHeader className="space-y-6">
            <div className="flex items-center gap-4">
              <Link href="/dashboard" className="flex items-center gap-2">
                <Button variant="ghost" size="icon">
                  <ChevronLeft className="h-5 w-5" />
                </Button>
                <h1 className="text-lg font-semibold">Volver</h1>
              </Link>
            </div>
            <div className="space-y-4">
              <h2 className="text-lg font-medium">¿Cómo te sientes hoy?</h2>
              <div className="flex gap-3">
                {MOODS.map((mood) => (
                  <button
                    key={mood.id}
                    onClick={() => setSelectedMood(mood.id)}
                    className={cn(
                      "p-4 rounded-xl transition-all",
                      getMoodButtonClass(mood.id, selectedMood === mood.id),
                      selectedMood === mood.id && "text-white scale-105"
                    )}
                  >
                    <Image
                      src={mood.image}
                      alt={mood.label}
                      width={32}
                      height={32}
                      className="w-8 h-8"
                    />
                  </button>
                ))}
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <h2 className="text-lg font-medium">
                Describe tu estado de ánimo
              </h2>
              <Textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Hoy me siento..."
                className="min-h-[550px] resize-none text-base"
              />
            </div>
            <Button
              onClick={handleSubmit}
              className="w-full py-6 text-lg"
              disabled={!selectedMood || !content || isLoading}
            >
              {isLoading ? "Enviando..." : "Guardar entrada"}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}