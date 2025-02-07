import { LineChart } from "@mui/x-charts/LineChart";

export interface EmotionData {
    date: string;
    Feliz: number | null;
    Normal: number | null;
    Triste: number | null;
    Enojado: number | null;
}

interface EmotionLineChartProps {
    data: EmotionData[];
}

const EmotionLineChart: React.FC<EmotionLineChartProps> = ({ data }) => {
    const dates = data.map((item) => item.date); // Eje X: Fechas
    const felizValues = data.map((item) => item.Feliz ?? null); // Valores para "Feliz"
    const normalValues = data.map((item) => item.Normal ?? null); // Valores para "Normal"
    const tristeValues = data.map((item) => item.Triste ?? null); // Valores para "Triste"
    const enojadoValues = data.map((item) => item.Enojado ?? null); // Valores para "Enojado"
    
    return (
        <div className="h-full">
            <LineChart
                xAxis={[
                    {
                        id: "date-axis",
                        data: dates,
                        scaleType: "band", // Escala de fechas
                        label: "Días de la Semana",
                        // labelStyle: { fill: "#ffffff" }, // Color del texto del eje X
                        // tickLabelStyle: { fill: "#ffffff" }, // Color de las etiquetas del eje X
                    },
                ]}
                series={[
                    {
                        id: "feliz",
                        data: felizValues,
                        label: "Feliz",
                        color: "#34D399",
                    },
                    {
                        id: "normal",
                        data: normalValues,
                        label: "Normal",
                        color: "#FBBF24",
                    },
                    {
                        id: "triste",
                        data: tristeValues,
                        label: "Triste",
                        color: "#60A5FA",
                    },
                    {
                        id: "enojado",
                        data: enojadoValues,
                        label: "Enojado",
                        color: "#F87171",
                    },
                ]}
                yAxis={[
                    {
                        id: "emotion-axis",
                        min: 0,
                        max: 10, // Rango del 1 al 10
                        label: "Intensidad Emocional",
                        // labelStyle: { fill: "#ffffff" }, // Color del texto del eje Y
                        // tickLabelStyle: { fill: "#ffffff" }, // Color de las etiquetas del eje Y
                    },
                ]}
                width={750} // Ancho fijo (ajustable)
                height={300} // Alto fijo (ajustable)
                // sx={{
                //     backgroundColor: "#121212", // Fondo oscuro para el gráfico
                // }}
            />
        </div>
    );
};

export default EmotionLineChart;