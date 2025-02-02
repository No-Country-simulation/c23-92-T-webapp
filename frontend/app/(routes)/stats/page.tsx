"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BottomNav } from "@/components/navigation/bottom-nav";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { motion } from "motion/react";
import { Navbar } from "@/components/navbar/Navbar";

const moodData = [
  { name: "Lun", value: 4, mood: "😊" },
  { name: "Mar", value: 3, mood: "😐" },
  { name: "Mie", value: 2, mood: "😔" },
  { name: "Jue", value: 5, mood: "😊" },
  { name: "Vie", value: 4, mood: "😊" },
  { name: "Sab", value: 3, mood: "😐" },
  { name: "Dom", value: 4, mood: "😊" },
];

const monthlyStats = {
  totalEntries: 45,
  avgEntriesPerWeek: 12,
  topMood: "😊",
  moodDistribution: [
    { mood: "😊", percentage: 45 },
    { mood: "😐", percentage: 30 },
    { mood: "😔", percentage: 15 },
    { mood: "😤", percentage: 10 },
  ],
  streakDays: 5,
  bestTime: "Tarde",
  commonTopics: ["trabajo", "familia", "ejercicio", "lectura"],
};

export default function StatsPage() {
  return (
    <div className="min-h-screen bg-background pt-20 pb-24">
      <Navbar /> 
      <div className="max-w-3xl mx-auto px-4">
        <Tabs defaultValue="week" className="space-y-4">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="week">Esta semana</TabsTrigger>
            <TabsTrigger value="month">Este mes</TabsTrigger>
          </TabsList>

          <TabsContent value="week" className="space-y-4">
            {/* Gráfico de estados de ánimo */}
            <Card>
              <CardHeader>
                <CardTitle className="text-xl">Estados de ánimo</CardTitle>
              </CardHeader>
              <CardContent className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={moodData}>
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="hsl(var(--primary))" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-4">
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">
                      Racha actual
                    </p>
                    <div className="flex items-center gap-2">
                      <span className="text-2xl font-bold">
                        {monthlyStats.streakDays}
                      </span>
                      <span className="text-sm text-muted-foreground">
                        días
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">
                      Mejor momento
                    </p>
                    <p className="text-2xl font-bold">
                      {monthlyStats.bestTime}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Topics Cloud */}
            <Card>
              <CardHeader>
                <CardTitle className="text-xl">Temas frecuentes</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {monthlyStats.commonTopics.map((topic, index) => (
                    <motion.div
                      key={topic}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <span className="px-3 py-1 bg-primary/10 rounded-full text-sm">
                        {topic}
                      </span>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="month" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-xl">Resumen mensual</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">
                      Total entradas
                    </p>
                    <p className="text-2xl font-bold">
                      {monthlyStats.totalEntries}
                    </p>
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">
                      Promedio semanal
                    </p>
                    <p className="text-2xl font-bold">
                      {monthlyStats.avgEntriesPerWeek}
                    </p>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-sm text-muted-foreground">
                    Distribución de estados
                  </h3>
                  {monthlyStats.moodDistribution.map((item) => (
                    <div key={item.mood} className="flex items-center gap-4">
                      <span className="text-2xl">{item.mood}</span>
                      <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
                        <div
                          className="h-full bg-primary"
                          style={{ width: `${item.percentage}%` }}
                        />
                      </div>
                      <span className="text-sm text-muted-foreground">
                        {item.percentage}%
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        <BottomNav />
      </div>
    </div>
  );
}
