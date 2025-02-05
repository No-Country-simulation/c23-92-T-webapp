'use client'

import React from "react";
import InteractionsList from "@/components/dashboard/interactionsList";
import { MoodKey } from "@/lib/constants/moods";
import Calendar from "@/components/dashboard/calendar";

export default function DashboardPage() {
  const entries = [
    {
      id: 1,
      title: "Un día productivo",
      date: "12 Oct, 2023",
      mood: "happy" as MoodKey,
    },
    {
      id: 2,
      title: "Día tranquilo",
      date: "11 Oct, 2023",
      mood: "neutral" as MoodKey,
    },
    {
      id: 3,
      title: "Día con mucho estrés",
      date: "10 Oct, 2023",
      mood: "sad" as MoodKey,
    },
  ];

  return (
    <div className="dashboard p-4 sm:p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

      {/* Grid for larger screens, flex column for smaller screens */}
      <div className="flex flex-col lg:grid lg:grid-cols-[3fr_2fr] gap-4 lg:gap-6">

        {/* Left Column */}
        <div className="flex flex-col gap-4">

          {/* Linear Chart */}
          <div className="h-48 sm:h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
          <p className="text-lg font-bold my-3 ps-5">Vista general</p>
          </div>

          {/* Two Cards in a grid for larger screens, stacked for smaller screens */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="h-48 sm:h-52 bg-[--color-white] border shadow-lg p-4 rounded-lg">
              {/* Card content */}
            </div>
            <div className="h-48 sm:h-52 bg-[--color-white] border shadow-lg p-4 rounded-lg">
              {/* Card content */}
            </div>
          </div>

        </div>

        {/* Right Column */}
        <div className="flex flex-col gap-4">

          {/* Recent Interactions */}
          <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
            <p className="text-lg font-bold my-3 ps-5">Recientes</p>
            {entries.map((entry) => (
              <div
                key={entry.id}
                className="bg-[--color-white] mb-2 hover:border hover:shadow-lg hover:rounded-2xl"
              >
                <InteractionsList
                  // title={entry.title}
                  // date={entry.date}
                  // mood={entry.mood}
                />
              </div>
            ))}
          </div>

          
          <div className="rounded-lg">
          <Calendar />
          </div>

        </div>
      </div>
    </div>
  );
}