"use client";
import formatDate from "@/lib/formatDate";
import { MOODS } from "@/lib/constants/moods";

export interface Interaction {
    readonly title: string;
    readonly content: string;
    readonly response: string;
    readonly date_interaction: string;
    readonly state_interaction: number;
    readonly mood_intensity: number;
}

export default function InteractionCard({ interaction }: { readonly interaction: Interaction }) {
    const mood = MOODS.find((mood) => mood.value === interaction.state_interaction);

    const moodColor = mood?.gradient ?? "from-gray-100 to-transparent dark:from-gray-950/50";
    const moodEmoji = mood?.image ?? "😐"; // Usa la imagen del mood o un emoji predeterminado

    return (
        <div className={`rounded-lg p-4 shadow-md bg-gradient-to-br ${moodColor}`}>
            <h3 className="text-lg font-bold flex items-center gap-2">
                {/* Mostrar la imagen del mood */}
                {typeof moodEmoji === 'string' ? (
                    <img src={moodEmoji} alt={mood?.label ?? "Mood"} className="w-6 h-6" />
                ) : (
                    <img src={moodEmoji.src} alt={mood?.label ?? "Mood"} className="w-6 h-6" />
                )}
                {interaction.title}
            </h3>
            <div>
                <h4 className="mt-2 font-bold">Contenido</h4>
                <p className="mt-2">{interaction.content}</p>
            </div>
            <div>
                <h4 className="mt-2 font-bold">Respuesta</h4>
                <p className="mt-2 italic">{interaction.response}</p>
            </div>
            <p className="mt-2 text-sm text-muted-foreground">
                Fecha: {formatDate(interaction.date_interaction)}
            </p>
        </div>
    );
}