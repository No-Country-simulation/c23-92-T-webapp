import React, { useState, useEffect } from "react";
import { MoodType } from "@/lib/constants/moods";
import socket from "@/lib/socket";
import InteractionsList from "../InteractionsList";

interface Interaction {
    title: string;
    content: string;
    response: string;
    date_interaction: string;
    state_interaction: number;
    mood_intensity: number;
}

interface Journal {
    date_journal: string;
    interactions_count: number;
    interactions: Interaction[];
}

export default function Interactions() {
    const [journals, setJournals] = useState<Journal[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    async function fetchJournals(): Promise<Journal[]> {
        return new Promise((resolve, reject) => {
            socket.emit("get_all_journals");
            socket.once("all_journals", (data: Journal[]) => {
                if (data && Array.isArray(data)) {
                    resolve(data);
                } else {
                    reject("Los datos recibidos no son válidos.");
                }
            });
            socket.once("error", (err: string) => {
                reject(err);
            });
        });
    }

    useEffect(() => {
        async function loadJournals() {
            try {
                const data = await fetchJournals();
                if (data.length > 0) {
                    const sortedJournals = [...data].sort(
                        (a, b) =>
                            new Date(b.date_journal).getTime() -
                            new Date(a.date_journal).getTime()
                    );
                    setJournals(sortedJournals);
                }
            } catch (err) {
                setError("Ocurrió un error al cargar los journals.");
            } finally {
                setLoading(false);
            }
        }
        loadJournals();
    }, []);

    const getMoodKey = (stateInteraction: number): MoodType => {
        switch (stateInteraction) {
            case 1:
                return "happy";
            case 2:
                return "neutral";
            case 3:
                return "sad";
            case 4:
                return "angry";
            default:
                return "neutral";
        }
    };

    if (loading) {
        return (
            <div className="flex min-h-screen justify-center items-center">
                <p className="text-muted-foreground">Cargando journals...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex min-h-screen justify-center items-center">
                <p className="text-destructive">{error}</p>
            </div>
        );
    }

    if (journals.length === 0) {
        return (
            <div className="flex min-h-screen justify-center items-center">
                <p className="text-muted-foreground">No hay journals disponibles.</p>
            </div>
        );
    }

    const limitedJournals = journals.slice(0, 1);

    return (
        <div className="px-4 py-2 hover:border hover:shadow-lg hover:rounded-2xl rounded-2xl transition-all duration-300 hover:scale-10">
            {limitedJournals.map((journal, journalIndex) => {
                const mostRecentInteraction = journal.interactions[0];

                if (!mostRecentInteraction) return null;

                return (
                    <div key={journalIndex}>
                        <h2 className="text-lg font-bold mb-1 ms-1">
                            Journal - {new Date(journal.date_journal).toLocaleDateString()}
                        </h2>
                        <div className="space-y-2">
                            {/* Renderizar solo la interacción más reciente */}
                            <InteractionsList
                                key={0}
                                title={mostRecentInteraction.title}
                                date={new Date(mostRecentInteraction.date_interaction).toLocaleString()}
                                mood={getMoodKey(mostRecentInteraction.state_interaction)}
                            />
                        </div>
                    </div>
                );
            })}
        </div>
    );
}