"use client";
import { Card, CardContent } from "@/components/ui/card";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { motion } from "framer-motion";
import { Navbar } from "@/components/navbar/Navbar";
import EmotionPieChart, { EmotionPieData } from "@/components/charts/EmotionPieChart";
import { useEffect, useState } from "react";
import socket from "@/lib/socket";
import { Loading } from "@/components/loading";
import { format, parseISO, isValid } from "date-fns";
import { es } from "date-fns/locale";
import EmotionCloudChart, { WordCloudData } from "@/components/charts/EmotionCloudChart";
import EmotionsComponent from "@/components/EmotionsComponent";
import { verifyToken } from "@/lib/auth";
import { handleTokenRefresh } from "@/lib/api";

interface MoodDayData {
  date: string;
  average_intensity: number;
}

interface MoodDayEvolution {
  success: boolean;
  data: MoodDayData[];
  week_offset: number;
  error?: string;
}

interface EmotionPieChartData {
  success: boolean;
  mood_proportions: EmotionPieData;
  total_interactions: number;
  happiest_day: string;
  saddest_day: string;
  error?: string;
}

interface StreakData {
  current_streak: number;
  max_streak: number;
}

interface StreakDataResponse {
  success: boolean;
  data: StreakData;
  error?: string;
}

interface AverageInteractionsPerMonth {
  success: boolean;
  data: AverageInteractionsPerMonthData;
  error?: string;
}

interface AverageInteractionsPerMonthData {
  avg_interactions_per_week: number;
  total_interactions: number;
  weeks_with_interactions: number;
}

interface EmotionalProbabilitiesData {
  emotional_probabilities: {
    Feliz: number;
    Normal: number;
    Triste: number;
    Enojado: number;
  }
}

interface EmotionalProbabilities {
  success: boolean;
  data: EmotionalProbabilitiesData;
  total_interactions: number;
  error?: string;
}

export default function StatsPage() {
  const [data, setData] = useState<EmotionPieData | null>(null);
  const [weekData, setWeekData] = useState<EmotionPieData | null>(null);
  const [monthData, setMonthData] = useState<EmotionPieData | null>(null);
  const [dayData, setDayData] = useState<MoodDayData[]>([]);
  const [happiestDay, setHappiestDay] = useState<string | null>(null);
  const [saddestDay, setSaddestDay] = useState<string | null>(null);
  const [happiestDayOfWeek, setHappiestDayOfWeek] = useState<string | null>(null);
  const [saddestDayOfWeek, setSaddestDayOfWeek] = useState<string | null>(null);
  const [happiestDayOfMonth, setHappiestDayOfMonth] = useState<string | null>(null);
  const [saddestDayOfMonth, setSaddestDayOfMonth] = useState<string | null>(null);
  const [totalInteractions, setTotalInteractions] = useState<number | null>(null);
  const [weekTotalInteractions, setWeekTotalInteractions] = useState<number | null>(null);
  const [monthTotalInteractions, setMonthTotalInteractions] = useState<number | null>(null);
  const [commonMood, setCommonMood] = useState<string | null>(null);
  const [weekCommonMood, setWeekCommonMood] = useState<string | null>(null);
  const [monthCommonMood, setMonthCommonMood] = useState<string | null>(null);
  const [cloudData, setCloudData] = useState<WordCloudData>();
  const [streakData, setStreakData] = useState<StreakData | null>(null);
  const [averageInteractionsPerWeek, setAverageInteractionsPerWeek] = useState<number | null>(null);
  const [weeksWithInteractions, setWeeksWithInteractions] = useState<number | null>(null);
  const [emotionalProbabilities, setEmotionalProbabilities] = useState<EmotionalProbabilitiesData | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const getMostCommonMood = (data: EmotionPieChartData) => {
    const { mood_proportions } = data;

    let mostCommonMood = "";
    let maxProportion = 0;

    for (const [mood, proportion] of Object.entries(mood_proportions)) {
      if (proportion > maxProportion) {
        mostCommonMood = mood;
        maxProportion = proportion;
        if (mostCommonMood === 'Feliz') {
          mostCommonMood = '😊';
        } else if (mostCommonMood === 'Normal') {
          mostCommonMood = '😐';
        } else if (mostCommonMood === 'Triste') {
          mostCommonMood = '😔';
        } else if (mostCommonMood === 'Enojado') {
          mostCommonMood = '😤'
        }
      }
    }

    return mostCommonMood;
  };

  useEffect(() => {
    const checkAuth = async () => {
          try {
            let isValidToken = await verifyToken();
            if (!isValidToken) {
              const refreshSuccess = await handleTokenRefresh();
              if (!refreshSuccess) {
                window.location.href = "/login";
                return;
              }
    
              isValidToken = await verifyToken();
              if (!isValidToken) throw new Error("Token verification failed");
            }
          } catch (error) {
            window.location.href = "/login";
          } finally {
            setIsLoading(false);
          }
        };
      checkAuth();

    socket.emit("get_mood_proportions");
    socket.on("mood_proportions_data", (response: EmotionPieChartData) => {
      if (response.success) {
        setData(response.mood_proportions);
        setTotalInteractions(response.total_interactions);
        setCommonMood(getMostCommonMood(response));
        const formattedHappiestDay = formatDate(response.happiest_day);
        const formattedSaddestDay = formatDate(response.saddest_day);
        setHappiestDay(formattedHappiestDay);
        setSaddestDay(formattedSaddestDay);
      } else {
        setError(response.error ?? "Error al obtener los datos de proporciones de estado de ánimo.");
      }
      setLoading(false);
    });

    socket.emit("get_mood_proportions_weekly");
    socket.on("mood_proportions_weekly_data", (response: EmotionPieChartData) => {
      if (response.success) {
        setWeekData(response.mood_proportions);
        setWeekTotalInteractions(response.total_interactions);
        setWeekCommonMood(getMostCommonMood(response));
        const formattedHappiestDay = formatDate(response.happiest_day);
        const formattedSaddestDay = formatDate(response.saddest_day);

        setHappiestDayOfWeek(formattedHappiestDay);
        setSaddestDayOfWeek(formattedSaddestDay);
      } else {
        setError(response.error ?? "Error al obtener los datos de proporciones de estado de ánimo semanal.");
      }
    });

    socket.emit("get_mood_proportions_monthly");
    socket.on("mood_proportions_monthly_data", (response: EmotionPieChartData) => {
      if (response.success) {
        setMonthData(response.mood_proportions);
        setMonthTotalInteractions(response.total_interactions);
        setMonthCommonMood(getMostCommonMood(response));
        const formattedHappiestDay = formatDate(response.happiest_day);
        const formattedSaddestDay = formatDate(response.saddest_day);

        setHappiestDayOfMonth(formattedHappiestDay);
        setSaddestDayOfMonth(formattedSaddestDay);
      } else {
        setError(response.error ?? "Error al obtener los datos de proporciones de estado de ánimo mensual.");
      }
    });

    socket.emit("get_mood_evolution_by_day");
    socket.on("mood_evolution_by_day_data", (response: MoodDayEvolution) => {
      if (response.success) {
        const formattedData = response.data.map((day) => ({
          date: format(parseISO(day.date), "EEE", { locale: es }),
          average_intensity: day.average_intensity,
        }));
        setDayData(formattedData);
      } else {
        console.error("Error al obtener los datos de evolución del estado de ánimo por día:", response.error);
      }
    });

    socket.emit("get_word_cloud");
    socket.on("word_cloud_data", (response: WordCloudData) => {
      if (response.success) {
        setCloudData(response);
      } else {
        console.error("Error al obtener los datos de la nube de palabras:", response.error);
      }
    });

    socket.emit("get_journals_streak");
    socket.on("journals_streak_data", (response: StreakDataResponse) => {
      if (response.success) {
        setStreakData(response.data);
      } else {
        console.error("Error al obtener los datos de racha:", response.error);
      }
    });

    socket.emit("get_avg_interactions_per_week_in_current_month");
    socket.on("avg_interactions_per_week_in_current_month_data", (response: AverageInteractionsPerMonth) => {
      if (response.success) {
        setAverageInteractionsPerWeek(response.data.avg_interactions_per_week);
        console.log("Promedio de interacciones por semana:", response.data.avg_interactions_per_week);
        setWeeksWithInteractions(response.data.weeks_with_interactions);
        console.log("Cantidad de semanas con interacciones:", response.data.weeks_with_interactions);
      } else {
        console.error("Error al obtener los datos de interacciones promedio por semana:", response.error);
      }
    });

    socket.emit("get_emotional_probabilities");
    socket.on("emotional_probabilities_data", (response: EmotionalProbabilities) => {
      if (response.success) {
        setEmotionalProbabilities(response.data);
      } else {
        console.error("Error al obtener los datos de probabilidades emocionales:", response.error);
      }
    });

    return () => {
      socket.off("mood_proportions_data");
      socket.off("mood_proportions_weekly_data");
      socket.off("mood_proportions_monthly_data");
      socket.off("mood_evolution_by_day_data");
      socket.off("word_cloud_data");
      socket.off("journals_streak_data");
      socket.off("avg_interactions_per_week_in_current_month");
      socket.off("emotional_probabilities_data");
    };
  }, []);

  const formatDate = (dateString: string | null | undefined): string | null => {
    if (!dateString) {
      return null;
    }

    try {
      const parsedDate = parseISO(dateString);
      if (isValid(parsedDate)) {
        return format(parsedDate, "EEEE, dd/MM/yyyy", { locale: es });
      }
    } catch (error) {
      console.error("Error al formatear la fecha:", error);
    }

    return null;
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="min-h-screen bg-background pt-20 pb-24">
      <Navbar />
      <div className="max-w-3xl mx-auto px-4">
        <Tabs defaultValue="general" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="general">General</TabsTrigger>
            <TabsTrigger value="week">Esta semana</TabsTrigger>
            <TabsTrigger value="month">Este mes</TabsTrigger>
          </TabsList>
          <TabsContent value="general" className="space-y-4">
            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-4">
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Racha actual</p>
                    <div className="flex items-center gap-2">
                      <span className="text-2xl font-bold">{streakData?.current_streak ?? 0}</span>
                      <span className="text-sm text-muted-foreground">días</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Racha Máxima</p>
                    <p className="text-2xl font-bold">{streakData?.max_streak ?? 0}</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Estado más común</p>
                    <p className="text-2xl font-bold">{commonMood ?? 'No tienes un estado común por el momento'}</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Día más feliz 😊</p>
                    <p className="text-xl font-bold">
                      {happiestDay ?? "No tienes un día más feliz por el momento"}
                    </p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Total interacciones</p>
                    <p className="text-xl font-bold">{totalInteractions ?? "No tienes interacciones hechas por el momento"}</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Día más triste 😔</p>
                    <p className="text-xl font-bold">
                      {saddestDay ?? "No tienes un día más triste por el momento"}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
            <Card>
              {loading ? (
                <Loading />
              ) : error ? (
                <p className="text-red-500">{error}</p>
              ) : data ? (
                <EmotionPieChart data={data} loading={loading} />
              ) : (
                <p>No hay datos disponibles.</p>
              )}
            </Card>
            {/* Topics Cloud */}
            <Card>
              <CardContent className="p-10">
                {/* Contenedor principal con diseño vertical */}
                <div className="flex flex-col items-center gap-10 text-center">
                  {/* Título */}
                  <p className="text-xl text-muted-foreground">Palabras Positivas</p>

                  {/* Contenedor de palabras */}
                  <div className="flex flex-wrap items-center justify-center gap-3">
                    {cloudData?.positive_words && Object.keys(cloudData.positive_words).length > 0 ? (
                      Object.entries(cloudData.positive_words).map(([word], index) => (
                        <motion.div
                          key={word}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                        >
                          <span className="px-3 py-1 bg-green-400 rounded-full text-l text-white">{word}</span>
                        </motion.div>
                      ))
                    ) : (
                      <p>No hay datos de palabras positivas disponibles.</p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-10">
                {/* Contenedor principal con diseño vertical */}
                <div className="flex flex-col items-center gap-10 text-center">
                  {/* Título */}
                  <p className="text-xl text-muted-foreground">Palabras Negativas</p>

                  {/* Contenedor de palabras */}
                  <div className="flex flex-wrap items-center justify-center gap-3">
                    {cloudData?.negative_words && Object.keys(cloudData.negative_words).length > 0 ? (
                      Object.entries(cloudData.negative_words).map(([word], index) => (
                        <motion.div
                          key={word}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                        >
                          <span className="px-3 py-1 bg-blue-400 rounded-full text-l text-white">{word}</span>
                        </motion.div>
                      ))
                    ) : (
                      <p>No hay datos de palabras Negativas disponibles.</p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="week" className="space-y-4">
            {/* Gráfico de estados de ánimo */}
            <Card>
              <CardContent className="p-6">
                <EmotionsComponent />
              </CardContent>
            </Card>
            <Card>
              <CardContent className="h-[30vw] p-5">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={dayData}>
                    <XAxis dataKey="date" />
                    <YAxis domain={[0, 10]} ticks={[0, 2, 4, 6, 8, 10]} />
                    <Tooltip />
                    <Bar dataKey="average_intensity" fill="hsl(var(--primary))" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-4">
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Estado más común de la semana</p>
                    <p className="text-2xl font-bold">{weekCommonMood ?? "No tienes estado más común de la semana por el momento"}</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Día más feliz de la semana😊</p>
                    <p className="text-xl font-bold">
                      {happiestDayOfWeek ?? "No tienes un día más feliz de la semana por el momento"}
                    </p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Total de interacciones de la semana</p>
                    <p className="text-xl font-bold">{weekTotalInteractions ?? "No has hecho interacciones por el momento"}</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Día más triste de la semana😔</p>
                    <p className="text-xl font-bold">
                      {saddestDayOfWeek ?? "No tienes un día más triste de la semana por el momento"}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
            <Card>
              {loading ? (
                <Loading />
              ) : error ? (
                <p className="text-red-500">{error}</p>
              ) : data ? (
                <EmotionPieChart data={weekData} loading={loading} />
              ) : (
                <p>No hay datos disponibles para esta semana.</p>
              )}
            </Card>
          </TabsContent>
          <TabsContent value="month" className="space-y-4">
            <Card>
              <CardContent className="space-y-6 p-10">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Promedio de interacciones por semana del mes</p>
                    <p className="text-2xl font-bold">{averageInteractionsPerWeek ?? "No has hecho interacciones durante el mes"}</p>
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Cantidad de semanas con interacciones del mes</p>
                    <p className="text-2xl font-bold">{weeksWithInteractions ?? "No has hecho interacciones durante las semanas de este mes"}</p>
                  </div>
                </div>
                <div className="space-y-4">
                  <h3 className="text-sm text-muted-foreground">Probabilidad de estados emocionales durante el mes</h3>
                  {emotionalProbabilities && Object.entries(emotionalProbabilities.emotional_probabilities).map(([mood, percentage]) => {
                    let emoji = '';
                    if (mood === 'Feliz') {
                      emoji = '😊';
                    } else if (mood === 'Normal') {
                      emoji = '😐';
                    } else if (mood === 'Triste') {
                      emoji = '😔';
                    } else if (mood === 'Enojado') {
                      emoji = '😤';
                    }
                    return (
                      <div key={mood} className="flex items-center gap-4">
                        <span className="text-2xl">{emoji}</span>
                        <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary"
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                        <span className="text-sm text-muted-foreground">{percentage}%</span>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
            {/* Gráfico de estados de ánimo */}
            <div className="grid grid-cols-2 gap-4">
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Estado más común del mes</p>
                    <p className="text-2xl font-bold">{monthCommonMood ?? "No tienes un estado más común del mes"}</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Día más feliz del mes😊</p>
                    <p className="text-xl font-bold">
                      {happiestDayOfMonth ?? "No tienes un día más feliz del mes"}
                    </p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Total de interacciones del mes</p>
                    <p className="text-xl font-bold">{monthTotalInteractions ?? "No has hecho interacciones este mes"}</p>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">Día más triste del mes😔</p>
                    <p className="text-xl font-bold">
                      {saddestDayOfMonth ?? "No tienes un día más triste del mes"}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
            <Card>
              {loading ? (
                <Loading />
              ) : error ? (
                <p className="text-red-500">{error}</p>
              ) : data ? (
                <EmotionPieChart data={monthData} loading={loading} />
              ) : (
                <p>No hay datos disponibles para este mes.</p>
              )}
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}