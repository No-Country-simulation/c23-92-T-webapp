import React, { useState } from "react";
import WordCloud from "react-d3-cloud";

export interface WordCloudData {
    success: boolean;
    global_word_frequencies: Record<string, number>;
    positive_words: Record<string, number>;
    negative_words: Record<string, number>;
    error?: string;
}

interface WordCloudProps {
    data?: WordCloudData;
}

const EmotionCloudChart: React.FC<WordCloudProps> = ({ data }) => {
    const [showPositive, setShowPositive] = useState(true);

    const defaultData = {
        success: true,
        global_word_frequencies: {
            feliz: 10,
            contento: 6,
            triste: 2,
            enojado: 2,
            bien: 2,
            mal: 1,
            gracias: 1,
            seguro: 1,
        },
        positive_words: {
            feliz: 10,
            contento: 6,
            bien: 2,
            gracias: 1,
            seguro: 1,
        },
        negative_words: {
            triste: 2,
            enojado: 2,
            mal: 1,
        },
    };

    const wordData = data || defaultData;

    const formatWords = (words: Record<string, number>) =>
        Object.entries(words).map(([text, value]) => ({
            text,
            value,
        }));

    const positiveWords = formatWords(wordData.positive_words);
    const negativeWords = formatWords(wordData.negative_words);

    const fontSize = (word: { value: number }) => Math.log2(word.value + 1) * 20;

    const hasPositiveWords = positiveWords.length > 0;
    const hasNegativeWords = negativeWords.length > 0;

    return (
        <div className="w-full h-full p-5">
            {/* Botones para alternar entre palabras positivas y negativas */}
            <div className="flex justify-center space-x-4 mb-4">
                <button
                    className={`px-4 py-2 rounded ${showPositive ? "bg-green-500 text-white" : "bg-gray-200"}`}
                    onClick={() => setShowPositive(true)}
                >
                    Palabras Positivas
                </button>
                <button
                    className={`px-4 py-2 rounded ${!showPositive ? "bg-red-500 text-white" : "bg-gray-200"}`}
                    onClick={() => setShowPositive(false)}
                >
                    Palabras Negativas
                </button>
            </div>

            {/* Contenedor para la nube de palabras o mensaje */}
            <div style={{ width: "100%", height: "100%", position: "relative" }}>
                {showPositive && !hasPositiveWords ? (
                    <div
                        className="flex items-center justify-center w-full h-full bg-gray-100 text-gray-500"
                        style={{ position: "absolute", top: 0, left: 0 }}
                    >
                        No hay palabras positivas encontradas.
                    </div>
                ) : !showPositive && !hasNegativeWords ? (
                    <div
                        className="flex items-center justify-center w-full h-full bg-gray-100 text-gray-500"
                        style={{ position: "absolute", top: 0, left: 0 }}
                    >
                        No hay palabras negativas encontradas.
                    </div>
                ) : (
                    <WordCloud
                        data={showPositive ? positiveWords : negativeWords}
                        fontSize={fontSize}
                        rotate={0}
                    />
                )}
            </div>
        </div>
    );
};

export default EmotionCloudChart;