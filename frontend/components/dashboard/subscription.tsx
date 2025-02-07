import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import Gift from "@/components/icons/gift"

const SubscriptionInvite = () => {
  return (
    <Card className="h-full p-4 border text-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
    <CardHeader>
      <CardTitle className="flex flex-col items-center gap-2">
        <Gift size={40} /> 
        <h2 className="text-2xl font-extrabold">Hazte Premium</h2>
      </CardTitle>
    </CardHeader>
    <CardContent>
      <p className="text-white text-base mb-4">
        Consigue más memoria y beneficios exclusivos al actualizar tu suscripción.
      </p>
      {/* Centering the Button */}
      <div className="flex justify-center">
        <Button className="flex items-center gap-2 
            bg-white text-blue-600 font-semibold
            transition-all duration-300 hover:scale-105 hover:bg-white">
          Ver plan <ArrowRight size={16} />
        </Button>
      </div>
    </CardContent>
  </Card>
  );
};

export default SubscriptionInvite;

