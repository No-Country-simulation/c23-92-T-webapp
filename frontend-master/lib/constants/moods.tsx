import { ReactNode } from "react";
import HappyIcon from "@/components/icons/mood/happy";
import SadIcon from "@/components/icons/mood/sad";
import NeutralIcon from "@/components/icons/mood/neutral";

export const MOODS = {
    happy: { icon: <HappyIcon size={24}/>, label: "Feliz" },
    sad: { icon: <SadIcon size={24}/>, label: "Triste" },
    neutral: { icon: <NeutralIcon size={24} />, label: "Neutral" },
    angry: { icon: <HappyIcon size={24} />, label: "Neutral" }
    
}
export type MoodKey = keyof typeof MOODS;



