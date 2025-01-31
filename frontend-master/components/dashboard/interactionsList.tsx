import React from "react";
import { cn } from "@/lib/utils";
import Image from "next/image";
import { MoodKey, MOODS } from "@/lib/constants/moods";


type InteractionsListProps = {
  title: string;
  date: string;
  mood: MoodKey;
};

const InteractionsList: React.FC<InteractionsListProps> = ({ title, date, mood }) => {
    
  const moodData = MOODS[mood]; 


    return (
      <div className="flex items-center justify-between p-3">
        
        {/* 📖 Título y  📅 Fecha*/}
        <div className="ms-2">

          <h3 className="text-base font-medium text-gray-900">{title}</h3>
          <p className="text-gray-500 text-xs">{date}</p>

        </div>

        {/* 😀 Estado de ánimo */}
        <span className={cn("text-sm font-bold")}>
        
        {moodData.icon}
        
      
        </span>
      </div>
    );
  };

export default InteractionsList;