"use client";
import formatDate from "@/lib/formatDate";
import { Interaction } from "./InteractionCard";

export interface Journal {
    date_journal: string;
    interactions_count: number;
    interactions: Interaction[];
}

interface JournalListProps {
    journals: Journal[];
    selectedJournal: Journal | null;
    onSelect: (journal: Journal) => void;
}

export default function JournalList({
    journals,
    selectedJournal,
    onSelect,
}: Readonly<JournalListProps>) {
    return (
        <ul>
            {journals
                .sort(
                    (a, b) =>
                        new Date(b.date_journal).getTime() -
                        new Date(a.date_journal).getTime()
                )
                .map((journal, index) => {
                    const isActive = selectedJournal?.date_journal === journal.date_journal;

                    return (
                        <li
                            key={index}
                            className={`cursor-pointer p-2 rounded-md ${isActive ? "bg-primary text-white" : "hover:bg-accent"
                                }`}
                            onClick={() => onSelect(journal)}
                        >
                            <span>{formatDate(journal.date_journal)}</span>
                        </li>
                    );
                })}
        </ul>
    );
}