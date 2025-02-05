import { useEffect, useState } from "react";
import { getSocket } from "@/lib/socket";
import { useSocketEvent } from "@/hooks/useSocket";

interface Interaction {
  id: string;
  title: string;
  content: string;
  mood_intensity?: number;
}

export default function Interactions() {
  const [interactions, setInteractions] = useState<Interaction[]>([]);
  const socket = getSocket();

  useEffect(() => {
    socket.emit("get_interactions_of_today");

    return () => {
      socket.off("interactions_of_today");
    };
  }, []);

  useSocketEvent("interactions_of_today", (data) => {
    if (data.error) {
      console.error("Error fetching interactions:", data.error);
    } else {
      setInteractions(data);
    }
  });

  return (
    <div>
      <h2>Today's Interactions</h2>
      {interactions.length === 0 ? (
        <p>No interactions found.</p>
      ) : (
        <ul>
          {interactions.map((interaction) => (
            <li key={interaction.id}>
              <strong>{interaction.title}</strong>: {interaction.content}{" "}
              {interaction.mood_intensity && `🌡️ Mood: ${interaction.mood_intensity}`}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}


// import React from "react";
// import { cn } from "@/lib/utils";
// import Image from "next/image";
// import { MoodKey, MOODS } from "@/lib/constants/moods";


// type InteractionsListProps = {
//   title: string;
//   date: string;
//   mood: MoodKey;
// };

// const InteractionsList: React.FC<InteractionsListProps> = ({ title, date, mood }) => {
    
//   const moodData = MOODS[mood]; 


//     return (
//       <div className="flex items-center justify-between p-3">
        
//         {/* 📖 Título y  📅 Fecha*/}
//         <div className="ms-2">

//           <h3 className="text-base font-medium text-gray-900">{title}</h3>
//           <p className="text-gray-500 text-xs">{date}</p>

//         </div>

//         {/* 😀 Estado de ánimo */}
//         <span className={cn("text-sm font-bold")}>
        
//         {moodData.icon}
        
      
//         </span>
//       </div>
//     );
//   };

// export default InteractionsList;

