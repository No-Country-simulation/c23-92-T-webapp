import HappyEmoji from "@/public/images/emoji-feliz.png";
import NeutralEmoji from "@/public/images/emoji-natural.png";
import SadEmoji from "@/public/images/emoji-triste.png";
import AngryEmoji from "@/public/images/emoji-enojado.png";

export const MOODS = {
  happy: {
    image: HappyEmoji,
    label: "Feliz",
    color: "text-green-500",
    gradient: "from-green-100 to-transparent dark:from-green-950/50",
  },
  neutral: {
    image: NeutralEmoji,
    label: "Neutral",
    color: "text-yellow-500",
    gradient: "from-yellow-100 to-transparent dark:from-yellow-950/50",
  },
  sad: {
    image: SadEmoji,
    label: "Triste",
    color: "text-blue-500",
    gradient: "from-blue-100 to-transparent dark:from-blue-950/50",
  },
  angry: {
    image: AngryEmoji,
    label: "Enojado",
    color: "text-red-500",
    gradient: "from-red-100 to-transparent dark:from-red-950/50",
  },
} as const;

export type MoodType = keyof typeof MOODS;

