import React, { useEffect, useState } from "react";
import EmotionLineChart, { EmotionData } from "./charts/EmotionLineChart";
import socket from "@/lib/socket";

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
        return <p className="text-center text-gray-500">Cargando datos...</p>;
    }

    if (error) {
        return <p className="text-center text-red-500">{error}</p>;
    }

    return (
        <div className="w-full h-full flex flex-col justify-center items-center">
            <h1 className="text-xl font-bold mb-4">Gráfico de Emociones</h1>
            {data.length > 0 ? (
                <div className="w-full h-full">
                    <EmotionLineChart data={data} />
                </div>
            ) : (
                <p className="text-center text-gray-500">No hay datos disponibles.</p>
            )}
        </div>
    );
};

export default EmotionsComponent;