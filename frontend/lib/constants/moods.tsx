import { ReactNode } from "react";
import HappyIcon from "@/components/icons/mood/happy";
import SadIcon from "@/components/icons/mood/sad";
import NeutralIcon from "@/components/icons/mood/neutral";
import AngryIcon from "@/components/icons/mood/angry";

export const MOODS = {
    happy: { icon: <HappyIcon size={24}/>, label: "Happy" },
    sad: { icon: <SadIcon size={24}/>, label: "Sad" },
    neutral: { icon: <NeutralIcon size={24} />, label: "Neutral" },
    angry: { icon: <AngryIcon size={24} />, label: "Angry" }
    
}
export type MoodKey = keyof typeof MOODS;