"use client";

import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { MOODS, MoodType } from "@/lib/constants/moods";
import Image from "next/image";

type JournalCardProps = {
  id: string;
  title: string;
  date: string;
  content: string;
  mood: MoodType;
};

const getMoodConfig = (moodId: MoodType) => {
  switch (moodId) {
    case "happy":
      return {
        border: "border-green-400 dark:border-green-700",
        gradient: "from-green-100 to-transparent dark:from-green-950/50",
      };
    case "neutral":
      return {
        border: "border-yellow-400 dark:border-yellow-700",
        gradient: "from-yellow-100 to-transparent dark:from-yellow-950/50",
      };
    case "sad":
      return {
        border: "border-blue-400 dark:border-blue-700",
        gradient: "from-blue-100 to-transparent dark:from-blue-950/50",
      };
    case "angry":
      return {
        border: "border-red-400 dark:border-red-700",
        gradient: "from-red-100 to-transparent dark:from-red-950/50",
      };
    default:
      return {
        border: "border-gray-400 dark:border-gray-700",
        gradient: "from-gray-100 to-transparent dark:from-gray-950/50",
      };
  }
};

export function JournalCard({
  id,
  title,
  date,
  content,
  mood,
}: JournalCardProps) {
  const moodConfig = getMoodConfig(mood);
  const moodData = MOODS.find((m) => m.id === mood);

  return (
    <Link href={`/journal/${id}`}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        whileHover={{ scale: 1.02 }}
        transition={{ duration: 0.2 }}
      >
        <Card
          className={cn(
            "overflow-hidden border-2",
            "hover:shadow-lg transition-all duration-300",
            "bg-card dark:bg-card/50",
            moodConfig.border
          )}
        >
          <CardContent className="p-0">
            <div className={cn("bg-gradient-to-b", moodConfig.gradient, "p-6")}>
              <div className="flex items-start justify-between mb-4">
                <div className="space-y-1">
                  <h3 className="font-semibold text-lg line-clamp-1">
                    {title}
                  </h3>
                  <p className="text-sm text-muted-foreground">{date}</p>
                </div>
                {moodData && (
                  <Image
                    src={moodData.image}
                    alt={moodData.label}
                    width={32}
                    height={32}
                    className="w-10 h-10"
                  />
                )}
              </div>

              <p className="text-sm text-muted-foreground line-clamp-3">
                {content}
              </p>

              <div className="flex items-center justify-end mt-4">
                <span className="text-xs text-muted-foreground">
                  Toca para ver más
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </Link>
  );
}
