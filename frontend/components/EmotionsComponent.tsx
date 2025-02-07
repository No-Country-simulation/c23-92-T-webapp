import React, { useEffect, useState } from "react";
import EmotionLineChart, { EmotionData } from "./charts/EmotionLineChart";
import socket from "@/lib/socket";
import { Skeleton, Alert, Typography } from "@mui/material";

interface EmotionEvolutionChartData {
    success: boolean;
    data: EmotionData[];
    time_range: string;
    week_offset: number;
    error?: string;
}

const EmotionsComponent = () => {
    const [data, setData] = useState<EmotionData[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        socket.emit("get_mood_evolution");
        socket.on("mood_evolution_data", (response: EmotionEvolutionChartData) => {
            if (response.success) {
                if (response.data && response.data.length > 0) {
                    setData(response.data);
                } else {
                    setError("No hay datos disponibles.");
                }
            } else {
                setError(response.error ?? "Error al obtener los datos de evolución del estado de ánimo.");
            }
            setLoading(false);
        });

        return () => {
            socket.off("mood_evolution_data");
        };
    }, []);

    if (loading) {
        // Mostrar esqueletos mientras se cargan los datos
        return (
            <div className="w-full h-full flex flex-col justify-center items-center">
                <Typography variant="h5" gutterBottom>
                    Cargando datos...
                </Typography>
                <Skeleton variant="rectangular" width={600} height={400} animation="wave" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="w-full h-full flex flex-col justify-center items-center">
                <Alert severity="error">{error}</Alert>
            </div>
        );
    }

    return (
        <div className="w-full h-full flex flex-col justify-center items-center">
            <Typography variant="h4" className="font-bold mb-4">
                Gráfico de Emociones
            </Typography>
            {data.length > 0 ? (
                <div className="w-full h-full">
                    <EmotionLineChart data={data} />
                </div>
            ) : (
                <Alert severity="info">No hay datos disponibles para mostrar.</Alert>
            )}
        </div>
    );
};

export default EmotionsComponent;