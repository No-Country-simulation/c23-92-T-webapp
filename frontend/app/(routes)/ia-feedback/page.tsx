"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { IAFeedbackCard } from "@/components/ia-feedback-card";
import { useJournalStore } from "@/lib/stores/journal-store";
import socket, { InteractionResponse } from "@/lib/socket";
import { Loading } from "@/components/loading";
import { verifyToken } from "@/lib/auth";
import { handleTokenRefresh } from "@/lib/api";

export default function IAFeedbackPage() {
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const currentEntry = useJournalStore((state) => state.currentEntry);
  const clearCurrentEntry = useJournalStore((state) => state.clearCurrentEntry);
  const [responseData, setResponseData] = useState<{
    title: string;
    iaFeedback: string;
  } | null>(null);

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

    if (!currentEntry) return;

    const handleInteractionResponse = (response: InteractionResponse) => {
      if (response.type === "success" && response.success === true) {
        setResponseData({
          title: response.title ?? "Título predeterminado",
          iaFeedback: response.response ?? "",
        });
      } else {
        console.error("Error al recibir la respuesta de la interacción:", response.error);
      }
    };

    socket.on("interaction_response", handleInteractionResponse);

    return () => {
      socket.off("interaction_response", handleInteractionResponse);
    };
  }, [currentEntry]);

  const handleContinue = () => {
    clearCurrentEntry();
    router.push("/dashboard");
  };

  if (isLoading) {
    return <Loading />;
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
        {responseData ? (
          <IAFeedbackCard
            mood={currentEntry.mood || ""}
            content={currentEntry.content}
            iaFeedback={responseData.iaFeedback}
            title={responseData.title}
            onContinue={handleContinue}
          />
        ) : (
          <div className="min-h-screen flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        )}
      </div>
    </div>
  );
}