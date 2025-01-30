'use client'
import { JournalCard } from "@/components/journal-card";
import { Navbar } from "@/components/navbar/Navbar";
import { BottomNav } from "@/components/navigation/bottom-nav";
import { CreateEntryButton } from "@/components/create-entry-button";
import { MoodType } from "@/lib/constants/moods";
import Sidebar from "@/components/navigation/sidebar";

import React, { useState } from "react";
import { testConnection } from "@/lib/api";

export default function DashboardPage() {
  
  
  // const entries = [
    //   {
      //     id: "1",
      //     title: "Un día productivo",
      //     date: "12 de Octubre, 2023",
      //     content:
      //       "Hoy fue un día muy productivo. Terminé varios proyectos pendientes y aprendí cosas nuevas. Me siento satisfecho con lo que logré y estoy motivado para seguir mejorando.",
      //     mood: "happy" as MoodType,
      //   },
      //   {
        //     id: "2",
        //     title: "Día tranquilo",
        //     date: "11 de Octubre, 2023",
  //     content:
  //       "Hoy fue un día relajado. Pasé tiempo con mi familia y disfruté de una buena película. Fue agradable tener un día sin muchas preocupaciones.",
  //     mood: "neutral" as MoodType,
  //   },
  // ];

  return (
    <div className="dashboard p-6">
  <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

  {/* Grid con proporciones 75% - 25% */}
  <div className="grid grid-cols-[3fr_2fr] gap-6">
    {/* Columna Izquierda (75%) */}
    <div className="flex flex-col gap-4">
      <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
        {/* Contenido de la Card */}
      </div>
      <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
        {/* Contenido de la Card */}
      </div>
    </div>

    {/* Columna Derecha (25%) */}
    <div className="flex flex-col gap-4">
      <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
        {/* Contenido de la Card */}
      </div>
      <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
        {/* Contenido de la Card */}
      </div>
    </div>
  </div>
</div>
  
 

  /* /* <div className="max-w-3xl mx-auto px-4">
        <Navbar />
        <div className="grid gap-4 sm:grid-cols-1 md:grid-cols-2 auto-rows-max">
          {entries.map((entry) => (
            <JournalCard
              key={entry.id}
              id={entry.id}
              title={entry.title}
              date={entry.date}
              content={entry.content}
              mood={entry.mood as MoodType}
            />
          ))}
        </div>
        <BottomNav />
        <CreateEntryButton />
      </div> */ 
    
  );
}
