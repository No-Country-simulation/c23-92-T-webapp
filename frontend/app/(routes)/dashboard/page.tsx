"use client";
import React, { useEffect, useState } from "react";
import { verifyToken } from "@/lib/auth";
import { handleTokenRefresh } from "@/lib/api";
import { Loading } from "@/components/loading";
import EmotionsComponent from "@/components/EmotionsComponent";

export default function DashboardPage() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        let isValidToken = await verifyToken();
        if (!isValidToken) {
          const refreshSuccess = await handleTokenRefresh();
          if (!refreshSuccess) {
            window.location.href = "/login";
            return;
          }

          isValidToken = await verifyToken();
          if (!isValidToken) throw new Error("Token verification failed");
        }
      } catch (error) {
        window.location.href = "/login";
      } finally {
        setIsLoading(false);
      }
    };
    checkAuth();
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="dashboard p-6 h-full overflow-y-auto">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

      {/* Grid con proporciones responsivas */}
      <div className="grid grid-cols-1 md:grid-cols-[3fr_1fr] gap-6">
        {/* Columna Izquierda (75%) */}
        <div className="flex flex-col gap-4">
          <div className="min-h-[400px] bg-[--color-white] border shadow-lg p-4 rounded-lg">
            {/* Contenido de la Card */}
            <EmotionsComponent />
          </div>
          <div className="min-h-[200px] bg-[--color-white] border shadow-lg p-4 rounded-lg">
            {/* Contenido de la Card */}
          </div>
        </div>

        {/* Columna Derecha (25%) */}
        <div className="flex flex-col gap-4">
          <div className="min-h-[200px] bg-[--color-white] border shadow-lg p-4 rounded-lg">
            {/* Contenido de la Card */}
          </div>
          <div className="min-h-[200px] bg-[--color-white] border shadow-lg p-4 rounded-lg">
            {/* Contenido de la Card */}
          </div>
        </div>
      </div>
    </div>
  );
}