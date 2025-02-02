"use client";

import Image from "next/image";
import Logo from "@/public/images/logo-white.png";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export function Navbar() {
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="w-full fixed top-0 left-0 right-0 bg-background/80 backdrop-blur-sm border-b border-border z-50">
      <div className="max-w-3xl mx-auto w-full px-4 sm:px-6 lg:px-8">
        <div className="h-16 flex items-center justify-center">
          <Image src={Logo} alt="Logo" width={200} height={200} priority />
        </div>
      </div>
    </div>
  );
}
