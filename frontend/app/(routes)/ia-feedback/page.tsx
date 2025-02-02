"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { IAFeedbackCard } from "@/components/ia-feedback-card";
import { useJournalStore } from "@/lib/stores/journal-store";

export default function IAFeedbackPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const currentEntry = useJournalStore((state) => state.currentEntry);
  const clearCurrentEntry = useJournalStore((state) => state.clearCurrentEntry);
  const [iaFeedback, setIaFeedback] = useState<string>("");

  useEffect(() => {
    const generateFeedback = async () => {
      if (!currentEntry) {
        setIsLoading(false);
        return;
      }

      // Simulamos la generación de feedback (implementar después con la API)
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setIaFeedback(
        "Basado en tu entrada, noto un estado de ánimo positivo. Es importante mantener este optimismo y seguir cultivando las actividades que te hacen sentir bien."
      );
      setIsLoading(false);
    };

    generateFeedback();
  }, [currentEntry]);

  const handleContinue = () => {
    clearCurrentEntry();
    router.push("/dashboard");
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!currentEntry) {
    return (
      <div className="min-h-screen flex items-center justify-center flex-col gap-4">
        <p className="text-lg">No se encontró ninguna entrada</p>
        <button
          onClick={() => router.push("/journal/new")}
          className="text-primary hover:underline"
        >
          Crear nueva entrada
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-3xl mx-auto px-4">
        <IAFeedbackCard
          mood={currentEntry.mood || ""}
          content={currentEntry.content}
          iaFeedback={iaFeedback}
          onContinue={handleContinue}
        />
      </div>
    </div>
  );
}
