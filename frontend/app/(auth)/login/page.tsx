"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { motion } from "framer-motion";
import Link from "next/link";
import { useTheme } from "next-themes";
import Image from "next/image";

import Logo from "@/public/images/logo-white.png";
import { useRouter } from "next/navigation";
import { login, verifyToken } from "@/lib/auth";
import { Loading } from "@/components/loading";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const { theme } = useTheme();
  const router = useRouter();


    useEffect(() => {
      const checkAuthentication = async () => {
        try {
          const isAuthenticated = await verifyToken();
          if (isAuthenticated) {
            router.push("/dashboard");
          }
        } catch (error) {
          console.error("Error verifying token:", error);
        } finally {
          setIsCheckingAuth(false);
        }
      };
  
      checkAuthentication();
    }, [router]);
  
    if (isCheckingAuth) {
      return (
        <Loading></Loading>
      );
    }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Implementar lógica de login
    setError(null);
    try {
      const response = await login(username, password);
      console.log("Login exitoso:", response);
      
      
      router.push("/dashboard");
    } catch (err: any) {
      setError("Error al iniciar sesión. Verifica tus credenciales.");
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
            <h1 className="text-2xl font-bold text-center">
              Bienvenid@ a tu diario
            </h1>
            <p className="text-muted-foreground text-center">
              Inicia sesión en tu diario
            </p>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Input
                  type="username"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="h-12"
                />
              </div>
              <div className="space-y-2">
                <Input
                  type="password"
                  placeholder="Contraseña"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="h-12"
                />
              </div>
              <Button type="submit" className="w-full h-12 text-lg">
                Iniciar sesión
              </Button>
            </form>
            {error && (
              <p className="mt-4 text-red-500 text-center">{error}</p>
            )}

            <div className="mt-6 text-center space-y-4">
              <Link
                href="/restore-pass"
                className="text-sm text-primary hover:underline"
              >
                ¿Olvidaste tu contraseña?
              </Link>
              <div className="text-sm text-muted-foreground">
                ¿No tienes una cuenta?{" "}
                <Link href="/register" className="text-primary hover:underline">
                  Regístrate
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
