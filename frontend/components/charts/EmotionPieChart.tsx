import { PieChart } from "@mui/x-charts/PieChart";


export interface EmotionPieData {
    Feliz: number
    Normal: number 
    Triste: number
    Enojado: number
}

interface EmotionPieChartProps {
    data: EmotionPieData | null;
    loading?: boolean;
}

const EmotionPieChart: React.FC<EmotionPieChartProps> = ({ data, loading }) => {

    if (loading) {
        return (
            <div className="w-full h-full p-10 flex items-center justify-center">
                <p>Cargando datos...</p>
            </div>
        )
    }

    if (!data) {
        return (
            <div className="w-full h-full p-10 flex items-center justify-center">
                <p>No hay datos disponibles</p>
            </div>
        )
    }

    const pieData = [
        { emotion: "Feliz", value: data.Feliz, color: "#34D399" },
        { emotion: "Normal", value: data.Normal, color: "#FBBF24" },
        { emotion: "Triste", value: data.Triste , color: "#60A5FA" },
        { emotion: "Enojado", value: data.Enojado, color: "#F87171" },
    ];

    return (
        <div className="w-full h-full p-10">
            <PieChart 
                series={[
                    {
                        data: pieData.map(
                            (item, index) => ({ id: index, value: item.value ?? 0, label: item.emotion, color: item.color })
                        ),
                        highlightScope: { fade: 'global', highlight: 'item'},
                        faded: { innerRadius: 30, additionalRadius: -30, color: '#f0f0f0'}
                    }
                ]}
                width={600}
                height={400}
            />
        </div>
    );
};

export default EmotionPieChart;