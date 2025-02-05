"use client";
import { useState, useEffect } from "react";
import JournalList, { Journal } from "@/components/JournalList";
import InteractionCard from "@/components/InteractionCard";
import formatDate from "@/lib/formatDate";
import socket from "@/lib/socket";

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

export default function JournalPage() {
    const [journals, setJournals] = useState<Journal[]>([]);
    const [selectedJournal, setSelectedJournal] = useState<Journal | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);


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
                    setSelectedJournal(sortedJournals[0]);
                } else {
                    setError("No se encontraron journals.");
                }
            } catch (err) {
                setError("Ocurrió un error al cargar los journals.");
            } finally {
                setLoading(false);
            }
        }

        loadJournals();
    }, []);

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

    return (
        <div className="flex min-h-screen bg-background text-foreground">
            {/* Listado de Journals */}
            <aside className="w-1/4 p-4 border-r border-border">
                <h2 className="text-lg font-bold mb-4">Journals</h2>
                <JournalList
                    journals={journals}
                    selectedJournal={selectedJournal}
                    onSelect={(journal) => setSelectedJournal(journal)}
                />
            </aside>

            {/* Contenido Principal */}
            <main className="flex-1 p-4">
                {selectedJournal ? (
                    <>
                        <h2 className="text-xl font-bold mb-4">
                            Interacciones - {formatDate(selectedJournal.date_journal)}
                        </h2>
                        <div className="space-y-4">
                            {selectedJournal.interactions.map((interaction, index) => (
                                <InteractionCard key={index} interaction={interaction} />
                            ))}
                        </div>
                    </>
                ) : (
                    <p className="text-center text-muted-foreground">
                        Selecciona un journal para ver sus interacciones.
                    </p>
                )}
            </main>
        </div>
    );
}