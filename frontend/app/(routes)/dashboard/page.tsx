"use client";
import React, { useEffect, useState } from "react";
import { verifyToken } from "@/lib/auth";
import { handleTokenRefresh } from "@/lib/api";
import { Loading } from "@/components/loading";
import EmotionsComponent from "@/components/EmotionsComponent";
import Calendar from "@/components/dashboard/calendar";
import SubscriptionInvite from "@/components/dashboard/subscription";

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
    <div className="dashboard p-4 sm:p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

      {/* Grid for larger screens, flex column for smaller screens */}
      <div className="flex flex-col xl:grid xl:grid-cols-[3fr_2fr] gap-4 lg:gap-6">

        {/* Left Column */}
        <div className="flex flex-col gap-4">

          {/* Linear Chart */}
          <div className="min-h-[400px] bg-[--color-white] border shadow-lg p-4 rounded-lg">
            <p className="text-lg font-bold my-3 ps-5">Vista general</p>
            <EmotionsComponent />
          </div>

          {/* Two Cards in a Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 auto-rows-fr">
            <div className="h-full flex flex-col bg-[--color-white] border shadow-lg p-4 rounded-lg">
              {/* Card content */}
            </div>
            <div className="h-full flex flex-col">
              <SubscriptionInvite />
            </div>
          </div>

        </div>

        {/* Right Column */}
        <div className="flex flex-col gap-4 h-full">

          {/* Recent Interactions */}
          <div className="flex flex-col flex-1 bg-[--color-white] border shadow-lg p-4 rounded-lg">
            <p className="text-lg font-bold my-3 ps-5">Recientes</p>
            {/* Recent interactions card */}
          </div>
          
          {/* Calendar fills remaining space */}
          <div className="flex flex-col flex-1 rounded-lg">
            <Calendar />
          </div>

        </div>

      </div>
    </div>
  );
}