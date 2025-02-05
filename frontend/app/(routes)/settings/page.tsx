"use client";

import { useState, useEffect } from "react";
import { useTheme } from "next-themes";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { BottomNav } from "@/components/navigation/bottom-nav";
import { motion } from "framer-motion";
import {
  Bell,
  Moon,
  Sun,
  Download,
  Trash2,
  Shield,
  Languages,
  Clock,
} from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Navbar } from "@/components/navbar/Navbar";

export default function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const [reminderTime, setReminderTime] = useState("21:00");
  const [language, setLanguage] = useState("es");

  useEffect(() => {
    setMounted(true);
  }, []);

  const settingsSections = [
    {
      title: "Preferencias",
      items: [
        {
          icon: Bell,
          label: "Notificaciones diarias",
          component: (
            <Switch
              checked={notifications}
              onCheckedChange={setNotifications}
              aria-label="Toggle notifications"
            />
          ),
        },
        {
          icon: Moon,
          label: "Modo oscuro",
          component: mounted ? (
            <Switch
              checked={theme === "dark"}
              onCheckedChange={(checked) =>
                setTheme(checked ? "dark" : "light")
              }
              aria-label="Toggle dark mode"
            />
          ) : null,
        },
        {
          icon: Clock,
          label: "Hora del recordatorio",
          component: (
            <Select value={reminderTime} onValueChange={setReminderTime}>
              <SelectTrigger className="w-24">
                <SelectValue placeholder="Hora" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="19:00">19:00</SelectItem>
                <SelectItem value="20:00">20:00</SelectItem>
                <SelectItem value="21:00">21:00</SelectItem>
                <SelectItem value="22:00">22:00</SelectItem>
              </SelectContent>
            </Select>
          ),
        },
        {
          icon: Languages,
          label: "Idioma",
          component: (
            <Select value={language} onValueChange={setLanguage}>
              <SelectTrigger className="w-24">
                <SelectValue placeholder="Idioma" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="es">Español</SelectItem>
                <SelectItem value="en">English</SelectItem>
              </SelectContent>
            </Select>
          ),
        },
      ],
    },
    {
      title: "Datos y privacidad",
      items: [
        {
          icon: Download,
          label: "Exportar datos",
          component: (
            <Button variant="outline" size="sm">
              Exportar
            </Button>
          ),
        },
        {
          icon: Shield,
          label: "Política de privacidad",
          component: (
            <Button variant="ghost" size="sm">
              Ver
            </Button>
          ),
        },
      ],
    },
    {
      title: "Tu cuenta",
      items: [
        {
          icon: Trash2,
          label: "Eliminar cuenta",
          component: (
            <Button variant="destructive" size="sm">
              Eliminar
            </Button>
          ),
        },
      ],
    },
  ];

  if (!mounted) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background pt-20 pb-24">
      <div className="max-w-3xl mx-auto px-4">
        <div className="space-y-6">
          {settingsSections.map((section, sectionIndex) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: sectionIndex * 0.1 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="text-xl">{section.title}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  {section.items.map((item, itemIndex) => (
                    <motion.div
                      key={item.label}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: (sectionIndex + itemIndex) * 0.1 }}
                      className="flex items-center justify-between"
                    >
                      <div className="flex items-center gap-3">
                        <item.icon className="h-5 w-5 text-muted-foreground" />
                        <span className="font-medium">{item.label}</span>
                      </div>
                      {item.component}
                    </motion.div>
                  ))}
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
