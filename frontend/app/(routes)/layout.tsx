import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "../globals.css";
import Sidebar from "@/components/navigation/sidebar";
import { ThemeProvider } from "@/components/theme-provider";
import { BottomNav } from "@/components/navigation/bottom-nav";
import DeviceDetector from "@/lib/hooks/DeviceDetector";
import { CreateEntryButton } from "@/components/create-entry-button";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});
const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ThemeProvider attribute="class" defaultTheme="system">
          <DeviceDetector>
            <div className="flex relative max-w-screen-2xl min-h-screen m-auto 
                    bg-[#F6F4FA]
                    rounded-3xl">
              {/* Mostrar Sidebar solo en escritorio */}
              <aside className="relative hidden-if-mobile">
                <Sidebar />
              </aside>

              {/* Contenido principal */}
              <main className="flex-1 ps-28 py-12 pe-6 h-full data-[is-mobile=true]:ms-0">
                {children}
              </main>

              <CreateEntryButton />

              {/* Mostrar BottomNav solo en móviles */}
              <BottomNav className="block-if-mobile" />
            </div>
          </DeviceDetector>
        </ThemeProvider>
      </body>
    </html>
  );
}