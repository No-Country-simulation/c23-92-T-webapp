import React from "react";
import { cn } from "@/lib/utils";
import Image from "next/image";
import { MOODS, MoodType } from "@/lib/constants/moods";

type InteractionsListProps = {
  title: string;
  date: string;
  mood: MoodType;
};

const InteractionsList: React.FC<InteractionsListProps> = ({ title, date, mood }) => {
    const moodData = MOODS[mood]; // Ahora TypeScript lo reconoce correctamente
  
    return (
      <div className="flex items-center justify-between p-4">
        
        {/* 📖 Título y  📅 Fecha*/}
        <div className="ms-2">

          <h3 className="text-base font-medium text-gray-900">{title}</h3>
          <p className="text-gray-500 text-xs">{date}</p>

        </div>

        {/* 😀 Estado de ánimo */}
        <span className={cn("text-sm font-bold", moodData.color)}>
          <Image src={moodData.image} alt={moodData.label} className="w-6 h-6 inline-block mr-2" />
        </span>
      </div>
    );
  };

export default InteractionsList;