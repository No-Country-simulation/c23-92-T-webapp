import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import FireIcon from "../icons/fireicon";
import { useEffect, useState } from "react";
import socket from "@/lib/socket";

interface StreakData {
    current_streak: number;
    max_streak: number;
}

interface StreakDataResponse {
    success: boolean;
    data: StreakData;
    error?: string;
}

const Streak = () => {
    const [streakData, setStreakData] = useState<StreakData | null>(null);

    useEffect(() => {
        socket.emit("get_journals_streak");
        socket.on("journals_streak_data", (response: StreakDataResponse) => {
            if (response.success) {
                setStreakData(response.data);
            } else {
                console.error("Error al obtener los datos de racha:", response.error);
            }
        });
    });

    return (
        <Card className="h-full p-4 border text-center bg-gradient-to-r from-orange-400 to-orange-600 text-white">
            <CardHeader>
                <CardTitle className="flex flex-col items-center gap-2">
                    <FireIcon size={40} color="white" />
                    <h2 className="text-3xl font-extrabold">Racha</h2>
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-white text-base mb-4">
                    Racha Actual
                </p>
                <div className="flex items-center gap-2 justify-center">
                    <span className="text-2xl font-bold text-orange-100 text-center">
                        {`${streakData?.current_streak} días`}
                    </span>
                </div>
            </CardContent>
        </Card>
    );
};

export default Streak;

