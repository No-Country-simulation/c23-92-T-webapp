"use client";
import { useState, useEffect } from "react";
import { useTheme } from "next-themes";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Trash2, Lock } from "lucide-react";
import { motion } from "framer-motion";
import { changePassword, getProfile, updateProfile, logout as performLogout, deleteAccount } from "@/lib/auth";

export default function ProfilePage() {
    const [mounted, setMounted] = useState(false);
    const [profile, setProfile] = useState({
        username: "",
        email: "",
        timezone: "UTC",
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setMounted(true);
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const response = await getProfile();
            if (response.success && response.data) {
                setProfile(response.data);
                console.log("Profile data fetched successfully");
            } else {
                throw new Error("Invalid profile data");
            }
        } catch (err) {
            setError("Error fetching profile data.");
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateProfile = async () => {
        try {
            const response = await updateProfile(profile);
            if (response.success) {
                console.log("Profile updated successfully");
            } else {
                throw new Error("Failed to update profile");
            }
        } catch (err) {
            setError("Error updating profile.");
        }
    };

    const handleChangePassword = async (currentPassword: string, newPassword: string) => {
        try {
            const response = await changePassword(currentPassword, newPassword);
            if (response.success) {
                console.log("Password changed successfully!");
            } else {
                throw new Error("Failed to change password");
            }
        } catch (err) {
            setError("Error changing password.");
        }
    };

    const logout = async () => {
        try {
            const response = await performLogout();
            if (response && response.success) {
                console.log("Logout successful");
            } else {
                throw new Error("Failed to logout");
            }
        } catch (err) {
            setError("Error logging out.");
        }
    };

    const handleDeleteAccount = async () => {
        try {
            const response = await deleteAccount();
            if (response.success) {
                console.log("Account deleted successfully");
                logout();
            } else {
                throw new Error("Failed to delete account");
            }
        } catch (err) {
            setError("Error deleting account.");
        }
    };

    if (!mounted) {
        return null;
    }

    if (loading) {
        return <p className="text-center">Loading...</p>;
    }

    if (error) {
        return <p className="text-destructive text-center">{error}</p>;
    }

    return (
        <div className="min-h-screen bg-background pt-20 pb-24">
            <div className="max-w-3xl mx-auto px-4">
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
                                        <SelectItem value="UTC">UTC</SelectItem>
                                        <SelectItem value="America/New_York">New York</SelectItem>
                                        <SelectItem value="Europe/London">London</SelectItem>
                                        <SelectItem value="Asia/Tokyo">Tokyo</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

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
                            <Input type="password" placeholder="Contraseña actual" />
                            <Input type="password" placeholder="Nueva contraseña" />
                            <Button
                                onClick={() => handleChangePassword("oldPass", "newPass")}
                                className="w-full"
                            >
                                Cambiar contraseña
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
                                onClick={handleDeleteAccount}
                                className="w-full"
                            >
                                <Trash2 className="mr-2 h-4 w-4" /> Eliminar cuenta
                            </Button>
                        </CardContent>
                    </Card>
                </motion.div>
            </div>
        </div>
    );
}