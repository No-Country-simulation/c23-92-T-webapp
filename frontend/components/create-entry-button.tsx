"use client";

import { Plus } from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

export function CreateEntryButton() {
  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{
        type: "spring",
        stiffness: 260,
        damping: 20,
      }}
      className="fixed bottom-4 right-4 z-50"
    >
      <Link href="/journal/new">
        <button
          className={cn(
            "flex items-center justify-center",
            "w-14 h-14 rounded-full",
            "bg-gradient-to-r from-primary/90 to-primary",
            "text-primary-foreground shadow-lg hover:shadow-xl",
            "transition-all duration-300 hover:scale-105",
            "backdrop-blur-sm"
          )}
        >
          <Plus className="w-10 h-10" />
        </button>
      </Link>
    </motion.div>
  );
}
