"use client"; // Este archivo es un componente de cliente

import { useState, useEffect } from "react";

function useIsSmallScreen(threshold: number): boolean {
    const [isSmallScreen, setIsSmallScreen] = useState<boolean>(
        typeof window !== "undefined" ? window.innerWidth <= threshold : false
    );

    useEffect(() => {
        const mediaQuery = window.matchMedia(`(max-width: ${threshold}px)`);
        const handleChange = (e: MediaQueryListEvent) => setIsSmallScreen(e.matches);

        setIsSmallScreen(mediaQuery.matches);

        mediaQuery.addEventListener("change", handleChange);

        return () => mediaQuery.removeEventListener("change", handleChange);
    }, [threshold]);

    return isSmallScreen;
}

export default function DeviceDetector({ children }: { children: React.ReactNode }) {
    const isMobile = useIsSmallScreen(768); // Umbral de 768px

    return (
        <div data-is-mobile={isMobile}>
            {children}
        </div>
    );
}