import React from "react";
import Image from "next/image";
import { MoodType, MOODS } from "@/lib/constants/moods";

type InteractionsListProps = {
    title: string;
    date: string;
    mood: MoodType;
};

const InteractionsList: React.FC<InteractionsListProps> = ({ title, date, mood }) => {
    const moodData = MOODS.find((item) => item.id === mood);

    if (!moodData) {
        return null;
    }

    return (
        <div className="flex items-center justify-between p-1">
            <div className="ms-2">
                <h3 className="text-base font-medium text-gray-900">{title}</h3>
                <p className="text-gray-500 text-xs">{date}</p>
            </div>
            <div className="relative w-6 h-6">
                <Image
                    src={moodData.image}
                    alt={moodData.label}
                    layout="fill"
                    objectFit="contain"
                    className="rounded-full"
                />
            </div>
        </div>
    );
};

export default InteractionsList;