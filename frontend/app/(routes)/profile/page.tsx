"use client";
import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Trash2, Lock } from "lucide-react";
import { motion } from "framer-motion";
import { changePassword, getProfile, updateProfile, logout as performLogout, verifyToken } from "@/lib/auth";
import DeleteAccountModal from "@/components/DeleteAccountModal";
import moment from "moment-timezone";
import ReactCountryFlag from "react-country-flag";
import { timezoneCountryMapping } from "@/lib/utils"
import { handleTokenRefresh } from "@/lib/api";
import { Loading } from "@/components/loading";

interface User {
    username: string;
    email: string;
    timezone: string;
}

interface Errors {
    username?: string;
    email?: string;
    timezone?: string;
    password?: string;
    general?: string;
}

export default function ProfilePage() {
    const [mounted, setMounted] = useState(false);
    const [profile, setProfile] = useState<User>({
        username: "",
        email: "",
        timezone: "UTC",
    });
    const [loading, setLoading] = useState(true);
    const [errors, setErrors] = useState<Errors>({});
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [currentPassword, setCurrentPassword] = useState<string>("");
    const [newPassword, setNewPassword] = useState<string>("");
    const timezones = moment.tz.names();
    const [successMessage, setSuccessMessage] = useState<string | null>(null);

    const [isLoading, setIsLoading] = useState(true);

    const fetchProfile = async () => {
        try {
            const response = await getProfile();
            if (response.success) {
                setProfile(response.data);
                console.log("Profile data fetched successfully");
            } else {
                console.error("Invalid profile data", response);
                throw new Error("Invalid profile data");
            }
        } catch (err) {
            setErrors({ ...errors, general: "Error fetching profile data." });
        } finally {
            setLoading(false);
        }
    };

    const validateProfile = () => {
        const newErrors: Errors = {};
        if (!profile.username) newErrors.username = "El nombre de usuario es requerido.";
        if (!profile.email) newErrors.email = "El correo electrónico es requerido.";
        if (!profile.timezone) newErrors.timezone = "La zona horaria es requerida.";
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleUpdateProfile = async () => {
        if (!validateProfile()) return;

        try {
            const response = await updateProfile(profile);
            if (response.success) {
                setSuccessMessage("Perfil actualizado correctamente");
                console.log("Profile updated successfully");
                setErrors({});
            } else {
                console.error("Failed to update profile", response);
                throw new Error("Failed to update profile");
            }
        } catch (err) {
            setErrors({ ...errors, general: "Error updating profile." });
            console.error("Error updating profile:", err);
        }
    };

    const handleChangePassword = async () => {
        if (!currentPassword || !newPassword) {
            setErrors({ ...errors, password: "Ambos campos de contraseña son requeridos." });
            return;
        }
        try {
            const response = await changePassword({ current_password: currentPassword, new_password: newPassword });
            if (response.success) {
                setSuccessMessage("Contraseña cambiada correctamente");
                console.log("Password changed successfully");
                setErrors({});
            } else {
                throw new Error("Failed to change password");
            }
        } catch (err) {
            setErrors({ ...errors, password: "Error changing password." });
            console.error("Error changing password:", err);
        }
    };

    const logout = async () => {
        try {
            const response = await performLogout();
            if (response.success) {
                setSuccessMessage("Sesión cerrada correctamente");
                console.log("Logged out successfully");
                setErrors({});
                window.location.href = "/login";
            } else {
                throw new Error("Failed to logout");
            }
        } catch (err) {
            setErrors({ ...errors, general: "Error logging out." });
            console.error("Error logging out:", err);
        }
    };


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

        setMounted(true);
        fetchProfile();
    }, []);

    if (isLoading) {
        return <Loading />;
    }

    if (!mounted) {
        return null;
    }

    if (loading) {
        return <p className="text-center">Loading...</p>;
    }

    return (
        <div className="min-h-screen bg-background pt-20 pb-24">
            <div className="max-w-3xl mx-auto px-4">
                {/* Mostrar mensaje de éxito */}
                {successMessage && (
                    <p className="text-green-500 text-center mb-4">{successMessage}</p>
                )}

                {/* Profile Section */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-xl">Perfil</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            {/* Username */}
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <span className="font-medium">Nombre de usuario</span>
                                </div>
                                <Input
                                    value={profile.username || ""}
                                    onChange={(e) =>
                                        setProfile({ ...profile, username: e.target.value })
                                    }
                                    placeholder="Nombre de usuario"
                                />
                            </div>
                            {errors.username && <p className="text-destructive">{errors.username}</p>}
                            {/* Email */}
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <span className="font-medium">Correo electrónico</span>
                                </div>
                                <Input
                                    value={profile.email || ""}
                                    onChange={(e) =>
                                        setProfile({ ...profile, email: e.target.value })
                                    }
                                    placeholder="Correo electrónico"
                                />
                            </div>
                            {errors.email && <p className="text-destructive">{errors.email}</p>}
                            {/* Timezone */}
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <span className="font-medium">Zona horaria</span>
                                </div>
                                <Select
                                    value={profile.timezone || "UTC"}
                                    onValueChange={(value) =>
                                        setProfile({ ...profile, timezone: value })
                                    }
                                >
                                    <SelectTrigger className="w-48">
                                        <SelectValue placeholder="Selecciona una zona horaria" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {timezones.map((tz) => (
                                            <SelectItem key={tz} value={tz}>
                                                <div className="flex items-center gap-2">
                                                    {timezoneCountryMapping[tz] ? (
                                                        <ReactCountryFlag
                                                            countryCode={timezoneCountryMapping[tz]}
                                                            svg
                                                            style={{
                                                                width: "1.5em",
                                                                height: "1.5em",
                                                            }}
                                                        />
                                                    ) : (
                                                        <span className="text-muted-foreground">🌐</span>
                                                    )}
                                                    <span>{tz}</span>
                                                </div>
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                            {errors.timezone && <p className="text-destructive">{errors.timezone}</p>}
                            {/* Update Profile Button */}
                            <Button onClick={handleUpdateProfile} className="w-full">
                                Guardar cambios
                            </Button>
                        </CardContent>
                    </Card>
                </motion.div>

                {/* Change Password Section */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <Card className="mt-6">
                        <CardHeader>
                            <CardTitle className="text-xl">Cambiar contraseña</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            {/* Campo para la contraseña actual */}
                            <Input
                                type="password"
                                placeholder="Contraseña actual"
                                value={currentPassword}
                                onChange={(e) => setCurrentPassword(e.target.value)}
                            />
                            {/* Campo para la nueva contraseña */}
                            <Input
                                type="password"
                                placeholder="Nueva contraseña"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                            />
                            {/* Mostrar errores */}
                            {errors.password && <p className="text-destructive">{errors.password}</p>}
                            {/* Botón para cambiar la contraseña */}
                            <Button onClick={handleChangePassword} className="w-full">
                                Cambiar contraseña
                            </Button>
                        </CardContent>
                    </Card>
                </motion.div>
                {/* Logout Section */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <Card className="mt-6">
                        <CardHeader>
                            <CardTitle className="text-xl">Cerrar sesión</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <Button variant="outline" onClick={logout} className="w-full">
                                <Lock className="mr-2 h-4 w-4" /> Cerrar sesión
                            </Button>
                        </CardContent>
                    </Card>
                </motion.div>

                {/* Delete Account Section */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <Card className="mt-6">
                        <CardHeader>
                            <CardTitle className="text-xl">Eliminar cuenta</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <Button
                                variant="destructive"
                                onClick={() => setShowDeleteModal(true)}
                                className="w-full"
                            >
                                <Trash2 className="mr-2 h-4 w-4" /> Eliminar cuenta
                            </Button>
                        </CardContent>
                    </Card>
                </motion.div>
            </div>
            {/* Renderiza el modal de eliminación condicionalmente */}
            {showDeleteModal && (
                <DeleteAccountModal
                    open={showDeleteModal}
                    onClose={() => setShowDeleteModal(false)}
                />
            )}
        </div>
    );
}