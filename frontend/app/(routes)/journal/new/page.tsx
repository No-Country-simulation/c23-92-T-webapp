"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ChevronLeft } from "lucide-react";
import Link from "next/link";
import { useJournalStore } from "@/lib/stores/journal-store";
import { MOODS, MoodKey } from "@/lib/constants/moods";
import Image from "next/image";
import { cn } from "@/lib/utils";

const getMoodButtonClass = (mood: MoodKey, isSelected: boolean) => {
  if (!isSelected) return "bg-secondary hover:bg-secondary/80";

  switch (mood) {
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
  const router = useRouter();
  const [content, setContent] = useState("");
  const [selectedMood, setSelectedMood] = useState<MoodKey | null>(null);

  const handleSubmit = async () => {
    if (!selectedMood) return;

    try {
      const entry = {
        content,
        mood: selectedMood,
        timestamp: new Date().toISOString(),
      };

      useJournalStore.getState().setCurrentEntry(entry);
      router.push(`/ia-feedback`);
    } catch (error) {
      console.error("Error al guardar la entrada:", error);
    }
  };

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-2xl mx-auto">
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
              {Object.entries(MOODS).map(([key, mood]) => (
                  <button
                    key={key}
                    onClick={() => setSelectedMood(key as MoodKey)}
                    className={cn(
                      "p-4 rounded-xl transition-all",
                      getMoodButtonClass(key as MoodKey, selectedMood === key),
                      selectedMood === key && "text-white scale-105"
                    )}
                  >
                    {mood.icon}
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
              disabled={!selectedMood || !content}
            >
              Guardar entrada
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
