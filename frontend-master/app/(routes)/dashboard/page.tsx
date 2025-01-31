'use client'

import React, { useState } from "react";
import InteractionsList from "@/components/dashboard/interactionsList";
import { MoodType } from "@/lib/constants/moods";

export default function DashboardPage() {
  
  // borrar las entries al hacer fetch con las interactions
  const entries = [
    {
      id: "1",
      title: "Un día productivo",
      date: "12 Oct, 2023",
      mood: "happy" as MoodType
    },
    {
      id: "2",
      title: "Día tranquilo",
      date: "11 Oct, 2023",
      mood: "neutral" as MoodType
    },
    {
      id: "2",
      title: "Día con mucho estrés",
      date: "10 Oct, 2023",
      mood: "angry" as MoodType
    },
  ];

  return (
    <div className="dashboard p-6">
  <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

  {/* Grid con proporciones 75% - 25% */}
  <div className="grid grid-cols-[3fr_2fr] gap-6">

    {/* Columna Izquierda (75%) */}
    <div className="flex flex-col gap-4">

      <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
        {/* Linear chart */}
      </div>

      <div className="columns-2 h-52">
        {/* Contenido de la Card */}

        <div className="h-52 bg-[--color-white] border shadow-lg p-4 rounded-lg">

        </div>

        <div className="h-52 bg-[--color-white] border shadow-lg p-4 rounded-lg">

        </div>
      </div>

      

    </div>



    {/* Columna Derecha (25%) */}
    <div className="flex flex-col gap-4">

      <p className="text-lg font-bold">Recientes</p>

      {entries.map((entry) => (
        <div className="bg-[--color-white] border shadow-lg rounded-lg">
          <InteractionsList key={entry.id} title={entry.title} date={entry.date} mood={entry.mood}  />

        </div>
      ))}

      

      <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
        {/* Contenido de la Card */}
      </div>

    </div>
  </div>
</div>
  
 

    
  );
}
