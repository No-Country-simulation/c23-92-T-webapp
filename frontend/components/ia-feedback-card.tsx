"use client";
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ThumbsUp, ThumbsDown, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";
import Image from "next/image";
import { MOODS } from "@/lib/constants/moods";

interface IAFeedbackCardProps {
  readonly mood: string;
  readonly content: string;
  readonly iaFeedback: string;
  readonly title: string;
  readonly onContinue: () => void;
}

export function IAFeedbackCard({
  mood,
  content,
  iaFeedback,
  title,
  onContinue,
}: IAFeedbackCardProps) {
  const [displayedTitle, setDisplayedTitle] = useState<string>("");
  const [displayedFeedback, setDisplayedFeedback] = useState<string>("");
  const [isTyping, setIsTyping] = useState<boolean>(true);
  const [feedbackRating, setFeedbackRating] = useState<"like" | "dislike" | null>(
    null
  );

  const moodData = MOODS.find((m) => m.id === mood);

  const simulateTyping = (
    text: string,
    updateState: (currentText: string) => void,
    onComplete: () => void
  ) => {
    let currentIndex = 0;
    let currentText = "";

    const interval = setInterval(() => {
      if (currentIndex < text.length) {
        currentText += text[currentIndex];
        updateState(currentText);
        currentIndex++;
      } else {
        clearInterval(interval);
        onComplete();
      }
    }, 10);
  };

  useEffect(() => {
    simulateTyping(
      title,
      (currentText) => setDisplayedTitle(currentText),
      () => {
        simulateTyping(
          iaFeedback,
          (currentText) => setDisplayedFeedback(currentText),
          () => setIsTyping(false)
        );
      }
    );
  }, [title, iaFeedback]);

  const handleFeedbackRating = async (rating: "like" | "dislike") => {
    setFeedbackRating(rating);
  };

  return (
    <Card className="w-full border-none shadow-none">
      <CardHeader className="space-y-4 pt-20">
        <div className="flex items-center gap-3">
          <div className="bg-secondary p-3 rounded-xl">
            {moodData && (
              <Image
                src={moodData.image}
                alt={moodData.label}
                width={32}
                height={32}
                className="w-10 h-10"
              />
            )}
          </div>
          {/* Título animado */}
          <CardTitle className="text-xl">{displayedTitle}</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Contenido original */}
        <div className="bg-secondary/30 p-4 rounded-lg">
          <p className="text-sm leading-relaxed">{content}</p>
        </div>
        {/* Feedback de la IA animado */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium">MIA</h3>
          <div className="bg-primary/10 p-4 rounded-lg">
            <p className="text-sm leading-relaxed">{displayedFeedback}</p>
          </div>
          {/* Botones de rating */}
          {!isTyping && (
            <div className="flex items-center gap-4">
              <p className="text-sm text-muted-foreground">
                ¿Te resultó útil este feedback?
              </p>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleFeedbackRating("like")}
                  className={cn(
                    feedbackRating === "like" && "bg-primary text-white"
                  )}
                >
                  <ThumbsUp className="h-4 w-4" />
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleFeedbackRating("dislike")}
                  className={cn(
                    feedbackRating === "dislike" && "bg-destructive text-white"
                  )}
                >
                  <ThumbsDown className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </div>
        {/* Botón de continuar */}
        {!isTyping && (
          <Button onClick={onContinue} className="w-full mt-6">
            Continuar
            <ArrowRight className="h-4 w-4 ml-2" />
          </Button>
        )}
      </CardContent>
    </Card>
  );
}