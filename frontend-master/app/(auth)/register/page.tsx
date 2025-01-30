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
import { PasswordInput } from "@/components/ui/password-input";
import { useRouter } from "next/navigation";
import { register } from "@/lib/auth";


export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const { theme } = useTheme();
  const router = useRouter();

  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Implementar lógica de registro
    if (password !== confirmPassword) {
      setErrorMessage("Las contraseñas no coinciden.");
      return;
    }

    try {
      const response = await register(username, email, password, timezone);
      console.log("Usuario registrado:", response);
      router.push("/login"); // Redirige al login tras el registro
    } catch (error: any) {
      console.error("Error al registrar usuario:", error.message);
      setErrorMessage(error.message); // Muestra el error al usuario
    }
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
            <h1 className="text-2xl font-bold text-center">Crea tu cuenta</h1>
            <p className="text-muted-foreground text-center">
              Comienza tu viaje de reflexión personal
            </p>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Campos del formulario */}
              <div className="space-y-2">
                <Input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) =>
                    setUsername(e.target.value)
                  }
                  className="h-12"
                />
              </div>
              {/* Correo electronico */}
              <div className="space-y-2">
                <Input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => 
                    setEmail(e.target.value)
                  }
                  className="h-12"
                />
              </div>
              {/* Contraseña con componente para ocultar contraseña */}
              <PasswordInput
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
              />
              {/* Confirmar contraseña */}
              <PasswordInput
                value={confirmPassword}
                onChange={(e) =>
                  setConfirmPassword(e.target.value)
                }
              />
              {/* Mensaje de error */}
              {errorMessage && (
                <p className="text-red-500 text-sm">{errorMessage}</p>
              )}


              <Button type="submit" className="w-full h-12 text-lg">
                Crear cuenta
              </Button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-sm text-muted-foreground">
                ¿Ya tienes una cuenta?{" "}
                <Link href="/login" className="text-primary hover:underline">
                  Inicia sesión
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
