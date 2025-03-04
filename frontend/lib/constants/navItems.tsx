import { ReactNode } from "react";
import DashboardIcon from "../../components/icons/sidebar/dashboardIcon";
import NotesIcon from "@/components/icons/sidebar/notesIcon";
import StatisticsIcon from "@/components/icons/sidebar/statisticsIcon";
import CalendarIcon from "@/components/icons/sidebar/calendarIcon";
import SettingsIcon from "@/components/icons/sidebar/settingsIcon";
import UserIcon from "@/components/icons/sidebar/userIcon";

export interface NavItem {
  id: number;
  label: string;
  href: string;
  icon: ReactNode;
}
 
export const navItems: NavItem[] = [
  {
    id: 1,
    label: "Dashboard",
    href: "/dashboard",
    icon: <DashboardIcon size={21} color="#FFF" className=""/>,
  },
  {
    id: 2,
    label: "Notes",
    href: "/diaries",
    icon: <NotesIcon size={24} color="#FFF" />,
  },
  {
    id: 3,
    label: "Stats",
    href: "/stats",
    icon: <StatisticsIcon size={20} color="#FFF" />,
  },
  {
    id: 4,
    label: "Calendar",
    href: "/calendar",
    icon: <CalendarIcon size={24}  color="#FFF" />, //check
  },
  {
    id: 5,
    label: "Settings",
    href: "/settings",
    icon: <SettingsIcon size={24} color="#FFF" />,
  },
  {
    id: 6,
    label: "Profile",
    href: "/profile",
    icon: <UserIcon size={24} color="#FFF" />,
  },

];