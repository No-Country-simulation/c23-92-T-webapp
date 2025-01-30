"use client";

import { Button } from "@/components/ui/button";
import { useState } from "react";
import Image from "next/image";
import { MOODS, MoodType } from "@/lib/constants/moods";

interface MoodSelectorProps {
  onSelect: (mood: MoodType) => void;
}

export function MoodSelector({ onSelect }: MoodSelectorProps) {
  const [selectedMood, setSelectedMood] = useState<MoodType | null>(null);

  return (
    <div className="space-y-2">
      <p className="text-sm text-muted-foreground">¿Cómo te sientes hoy?</p>
      <div className="flex gap-2 flex-wrap">
        {MOODS.map((mood) => (
          <Button
            key={mood.id}
            variant={selectedMood === mood.id ? "default" : "outline"}
            size="sm"
            className="p-2 h-auto aspect-square"
            onClick={() => {
              setSelectedMood(mood.id);
              onSelect(mood.id);
            }}
            aria-label={`Seleccionar estado de ánimo: ${mood.label}`}
          >
            <Image
              src={mood.image}
              alt={mood.label}
              width={32}
              height={32}
              className="w-8 h-8"
            />
          </Button>
        ))}
      </div>
    </div>
  );
}
