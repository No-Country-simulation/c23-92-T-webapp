"use client"

import { navItems } from "../../lib/constants/navItems";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const Sidebar = () => {
  const pathname = usePathname();

  return (
    <nav
      className="
        absolute top-1/2 left-4
        transform -translate-y-1/2
        h-auto w-fit px-3 py-8
        bg-[--color-lila] text-[--color-white]
        rounded-[30px]
        shadow-lg
      "
    >
      <ul>
        {navItems.map((item) => {
          const isActive = pathname === item.href;

          return (
            <li key={item.id} className={item.label === "Settings" ? "mt-40" : ""}>
              <Link
                href={item.href}
                className={cn(
                  "flex items-center justify-center mb-6 p-3 rounded-full transition-colors",
                  isActive ? "bg-[#483A9A]" : "hover:bg-[#6153D3]"
                )}
              >
                {item.icon}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
};

export default Sidebar;

