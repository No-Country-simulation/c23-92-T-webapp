import { create } from "zustand";
import { JournalEntry } from "@/lib/api";
import { MoodType } from "@/lib/constants/moods";

interface JournalStore {
  currentEntry: JournalEntry | null;
  setCurrentEntry: (entry: JournalEntry) => void;
  clearCurrentEntry: () => void;
}

export const useJournalStore = create<JournalStore>((set) => ({
  currentEntry: null,
  setCurrentEntry: (entry) => set({ currentEntry: entry }),
  clearCurrentEntry: () => set({ currentEntry: null }),
}));
