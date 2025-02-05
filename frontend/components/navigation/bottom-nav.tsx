"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Smile, Calendar, Grid, User } from "lucide-react";

const navItems = [
  {
    href: "/dashboard",
    icon: Smile,
    label: "Diario",
  },
  {
    href: "/calendar",
    icon: Calendar,
    label: "Calendario",
  },
  {
    href: "/stats",
    icon: Grid,
    label: "Estadísticas",
  },
  {
    href: "/settings",
    icon: User,
    label: "Perfil",
  },
];

interface BottomNavProps {
  className?: string;
}

export function BottomNav({ className }: Readonly<BottomNavProps>) {
  const pathname = usePathname();
  return (
    <div
      className={cn(
        "fixed bottom-4 left-0 right-0 z-50 px-4",
        className
      )}
    >
      <div className="max-w-3xl mx-auto">
        <nav className="bg-card/80 dark:bg-card/80 backdrop-blur-sm rounded-full h-14 flex justify-around items-center shadow-lg border border-border">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex flex-col items-center justify-center w-full h-full transition-colors",
                  isActive
                    ? "text-primary"
                    : "text-muted-foreground hover:text-primary"
                )}
              >
                <Icon className="h-5 w-5" />
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
}