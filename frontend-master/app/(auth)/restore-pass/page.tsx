"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { motion } from "framer-motion";
import Link from "next/link";
import { useTheme } from "next-themes";
import Image from "next/image";
import Logo from "@/public/images/logo-white.png";

export default function RestorePassPage() {
  const [email, setEmail] = useState("");
  const [isSent, setIsSent] = useState(false);
  const { theme } = useTheme();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSent(true);
    // Implementar lógica de recuperación
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <Card className="border-none shadow-lg">
          <CardHeader className="space-y-3 items-center">
            <motion.div
              initial={{ scale: 0.5 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5 }}
            >
              <Image
                src={Logo}
                alt="Logo"
                width={100}
                height={100}
                className="w-full h-auto"
              />
            </motion.div>
            <h1 className="text-2xl font-bold text-center">
              Recupera tu contraseña
            </h1>
            <p className="text-muted-foreground text-center">
              Te enviaremos un enlace para restablecer tu contraseña
            </p>
          </CardHeader>
          <CardContent>
            {!isSent ? (
              <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="h-12"
                />
                <Button type="submit" className="w-full h-12 text-lg">
                  Enviar enlace
                </Button>
              </form>
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center space-y-4"
              >
                <p className="text-green-500">
                  ¡Revisa tu correo! Te hemos enviado las instrucciones.
                </p>
              </motion.div>
            )}

            <div className="mt-6 text-center">
              <Link href="/login" className="text-primary hover:underline">
                Volver al inicio de sesión
              </Link>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
