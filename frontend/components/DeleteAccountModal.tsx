// DeleteAccountModal.tsx
import { Card, CardContent, CardHeader } from "@mui/material";
import { CardTitle } from "./ui/card";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { deleteAccount, logout } from "@/lib/auth";

interface DeleteAccountModalProps {
    open: boolean;
    onClose: () => void;
}

const DeleteAccountModal = ({ open, onClose }: DeleteAccountModalProps) => {
    const [error, setError] = useState<string | null>(null);

    if (!open) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle>Eliminar cuenta</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-sm text-muted-foreground mb-4">
                        ¿Estás seguro de que quieres eliminar este usuario? Se perderán todos tus datos.
                    </p>
                    <div className="flex justify-end gap-2">
                        <Button
                            variant="outline"
                            onClick={onClose}
                        >
                            No
                        </Button>
                        <Button
                            variant="destructive"
                            onClick={async () => {
                                onClose(); // Cierra el modal
                                try {
                                    const response = await deleteAccount();
                                    if (response.success) {
                                        console.log("Cuenta eliminada exitosamente");
                                        logout();
                                    } else {
                                        throw new Error("No se pudo eliminar la cuenta");
                                    }
                                } catch (err) {
                                    setError("Error al eliminar la cuenta.");
                                }
                            }}
                        >
                            Sí
                        </Button>
                    </div>
                    {error && (
                        <p className="text-red-500 text-sm mt-2">{error}</p>
                    )}
                </CardContent>
            </Card>
        </div>
    );
};

export default DeleteAccountModal;
