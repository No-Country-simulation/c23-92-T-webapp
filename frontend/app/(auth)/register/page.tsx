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
import { PasswordInput } from "@/components/ui/password-input";
import { useRouter } from "next/navigation";
import { register, verifyToken } from "@/lib/auth";
import { Loading } from "@/components/loading";

const validateEmail = (email: string): boolean => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
};

const validatePassword = (password: string): boolean => {
  const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~])[A-Za-z\d!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]{8,}$/;
  return re.test(String(password));
};

const validateUsername = (username: string): boolean => {
  return username.length >= 3 && username.length <= 20;
};

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  const { theme } = useTheme();
  const router = useRouter();

  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

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

  const validateForm = (): boolean => {
    if (!username || !email || !password || !confirmPassword) {
      setErrorMessage("Todos los campos son obligatorios");
      return false;
    }

    if (!validateUsername(username)) {
      setErrorMessage("El nombre de usuario debe tener entre 3 y 20 caracteres");
      return false;
    }

    if (!validateEmail(email)) {
      setErrorMessage("El formato del correo electrónico no es válido");
      return false;
    }

    if (!validatePassword(password)) {
      setErrorMessage(
        "La contraseña debe contener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial"
      );
      return false;
    }

    if (password !== confirmPassword) {
      setErrorMessage("Las contraseñas no coinciden");
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await register(username, email, password, timezone);
      console.log("Usuario registrado:", response);
      router.push("/login");
    } catch (error: any) {
      console.error("Error al registrar usuario:", error);
      setErrorMessage(error.message || "Error al registrar usuario");
    } finally {
      setIsSubmitting(false);
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
              <div className="space-y-2">
                <Input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="h-12"
                  disabled={isSubmitting}
                />
              </div>
              <div className="space-y-2">
                <Input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="h-12"
                  disabled={isSubmitting}
                />
              </div>
              <PasswordInput
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <PasswordInput
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
              {errorMessage && (
                <p className="text-red-500 text-sm mt-2">{errorMessage}</p>
              )}
              <Button
                type="submit"
                className="w-full h-12 text-lg"
                disabled={isSubmitting}
              >
                {isSubmitting ? "Creando cuenta..." : "Crear cuenta"}
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