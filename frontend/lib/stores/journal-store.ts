import { create } from "zustand";

interface JournalEntry {
  mood: string;
  content: string;
}

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
