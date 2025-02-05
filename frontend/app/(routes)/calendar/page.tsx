"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  ChevronLeft,
  ChevronRight,
  Calendar as CalIcon,
  TrendingUp,
  Clock,
} from "lucide-react";
import { BottomNav } from "@/components/navigation/bottom-nav";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Navbar } from "@/components/navbar/Navbar";
import socket from "@/lib/socket";

type DayData = {
  mood: keyof typeof moodColors;
  content: string;
};

type MoodDataType = {
  [date: string]: DayData;
};

const moodData: MoodDataType = {
  "2024-03-01": { mood: "😊", content: "Día productivo en el trabajo" },
  "2024-03-02": { mood: "😐", content: "Día tranquilo en casa" },
  "2024-03-03": { mood: "😔", content: "Me sentí un poco cansado" },
  "2024-03-04": { mood: "😊", content: "Gran día con amigos" },
};

const moodColors = {
  "😊": "bg-green-400",
  "😐": "bg-yellow-400",
  "😔": "bg-blue-400",
  "😤": "bg-red-400",
};

const monthStats = {
  totalEntries: 15,
  topMood: "😊",
  mostProductiveDay: "Martes",
  mostProductiveTime: "Tarde",
  streakDays: 5,
};

interface JournalDate {
  success: boolean;
  date: string;
}

interface JournalData {
  date_journal: string;
  interactions_count: number;
  mood_journal_intensity: number;
  interactions: string;
}

interface Interactions {
  title: string;
  content: string;
  response: string;
  date_interaction: string;
  state_interaction: string;
}

export default function CalendarPage() {
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [currentMonth, setCurrentMonth] = useState(new Date());

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDay = new Date(year, month, 1).getDay();
    return { daysInMonth, firstDay };
  };

  const { daysInMonth, firstDay } = getDaysInMonth(currentMonth);

  const handlePrevMonth = () => {
    setCurrentMonth(
      new Date(currentMonth.setMonth(currentMonth.getMonth() - 1))
    );
  };

  const handleNextMonth = () => {
    setCurrentMonth(
      new Date(currentMonth.setMonth(currentMonth.getMonth() + 1))
    );
  };

  const getDayData = (date: string) => {
    socket.emit("get_journal_by_date");
    socket.on("journal_by_date", (data) => {
      console.log(data);
    });
  }

  return (
    <div className="min-h-screen bg-background pt-20 pb-24">
      <div className="max-w-3xl mx-auto px-4">
        <Navbar />
        <Card className="mb-4">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
            <CardTitle className="text-xl font-bold">
              {currentMonth.toLocaleString("es-ES", {
                month: "long",
                year: "numeric",
              })}
            </CardTitle>
            <div className="flex gap-2">
              <Button variant="outline" size="icon" onClick={handlePrevMonth}>
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <Button variant="outline" size="icon" onClick={handleNextMonth}>
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {/* Grid del calendario */}
            <div className="grid grid-cols-7 gap-1">
              {["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"].map((day) => (
                <div
                  key={day}
                  className="text-center text-sm font-medium text-muted-foreground p-2"
                >
                  {day}
                </div>
              ))}
              {Array.from({ length: firstDay }).map((_, index) => (
                <div key={`empty-${index}`} className="aspect-square" />
              ))}
              {Array.from({ length: daysInMonth }).map((_, index) => {
                const day = index + 1;
                const dateString = `2024-03-${day.toString().padStart(2, "0")}`;
                const dayData = moodData[dateString];

                return (
                  <motion.div
                    key={day}
                    whileHover={{ scale: 1.1 }}
                    className={cn(
                      "aspect-square p-1 cursor-pointer",
                      selectedDate === dateString &&
                        "ring-2 ring-primary rounded-lg"
                    )}
                    onClick={() => setSelectedDate(dateString)}
                  >
                    <div
                      className={cn(
                        "w-full h-full rounded-lg flex items-center justify-center",
                        dayData ? moodColors[dayData.mood] : "bg-secondary",
                        "transition-colors duration-200"
                      )}
                    >
                      <span className="text-sm font-medium">{day}</span>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Detalle del día seleccionado */}
        {selectedDate && moodData[selectedDate] && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center gap-4 mb-4">
                  <div
                    className={cn(
                      "w-12 h-12 rounded-full flex items-center justify-center text-2xl",
                      moodColors[moodData[selectedDate].mood]
                    )}
                  >
                    {moodData[selectedDate].mood}
                  </div>
                  <div>
                    <h3 className="font-semibold">
                      {new Date(selectedDate).toLocaleDateString("es-ES", {
                        weekday: "long",
                        day: "numeric",
                        month: "long",
                      })}
                    </h3>
                  </div>
                </div>
                <p className="text-muted-foreground">
                  {moodData[selectedDate].content}
                </p>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Patrones semanales */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle className="text-xl">Patrones semanales</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes",
                "Sábado",
                "Domingo",
              ].map((day) => (
                <div key={day} className="flex items-center gap-4">
                  <span className="w-24 text-sm text-muted-foreground">
                    {day}
                  </span>
                  <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{
                        width:
                          day === monthStats.mostProductiveDay ? "80%" : "30%",
                      }}
                      className="h-full bg-primary"
                      transition={{ duration: 1 }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
