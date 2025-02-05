import { useEffect } from "react";
import { getSocket } from "@/lib/socket";

export function useSocketEvent(eventName: string, callback: (data: any) => void) {
  useEffect(() => {
    const socket = getSocket();
    socket.on(eventName, callback);

    return () => {
      socket.off(eventName, callback);
    };
  }, [eventName, callback]);
}
