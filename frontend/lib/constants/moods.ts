import HappyEmoji from "@/public/images/emoji-feliz.png";
import NeutralEmoji from "@/public/images/emoji-natural.png";
import SadEmoji from "@/public/images/emoji-triste.png";
import AngryEmoji from "@/public/images/emoji-enojado.png";

export const MOODS = [
  {
    id: "happy",
    image: HappyEmoji,
    label: "Feliz",
    color: "green",
    gradient: "from-green-100 to-transparent dark:from-green-950/50",
    value: 1
  },
  {
    id: "neutral",
    image: NeutralEmoji,
    label: "Neutral",
    color: "yellow",
    gradient: "from-yellow-100 to-transparent dark:from-yellow-950/50",
    value: 2
  },
  {
    id: "sad",
    image: SadEmoji,
    label: "Triste",
    color: "blue",
    gradient: "from-blue-100 to-transparent dark:from-blue-950/50",
    value: 3
  },
  {
    id: "angry",
    image: AngryEmoji,
    label: "Enojado",
    color: "red",
    gradient: "from-red-100 to-transparent dark:from-red-950/50",
    value: 4
  },
] as const;

export type MoodType = (typeof MOODS)[number]["id"];
