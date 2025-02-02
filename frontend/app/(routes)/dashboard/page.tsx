"use client";

import React, { useEffect, useState } from "react";
import { verifyToken } from "@/lib/auth";
import { handleTokenRefresh } from "@/lib/api";
import { Loading } from "@/components/loading";

export default function DashboardPage() {

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        let isValidToken = await verifyToken();

        if (!isValidToken) {
          const refreshSuccess = await handleTokenRefresh();

          if (!refreshSuccess) {
            window.location.href = '/login';
            return;
          }
          
          isValidToken = await verifyToken();
          if (!isValidToken) throw new Error("Token verification failed");          
        }
      } catch (error) {
        window.location.href = '/login';
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (isLoading) {
    return <Loading></Loading>
  }

  return (
    <div className="dashboard p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

      {/* Grid con proporciones 75% - 25% */}
      <div className="grid grid-cols-[3fr_2fr] gap-6">
        {/* Columna Izquierda (75%) */}
        <div className="flex flex-col gap-4">
          <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
            {/* Contenido de la Card */}
          </div>
          <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
            {/* Contenido de la Card */}
          </div>
        </div>

        {/* Columna Derecha (25%) */}
        <div className="flex flex-col gap-4">
          <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
            {/* Contenido de la Card */}
          </div>
          <div className="h-72 bg-[--color-white] border shadow-lg p-4 rounded-lg">
            {/* Contenido de la Card */}
          </div>
        </div>
      </div>
    </div>

  );
}
