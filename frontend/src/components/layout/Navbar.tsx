"use client";

import { BarChart3, Database, Home, Info, Lightbulb, Menu, X, Activity } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  const navigation = [
    {
      name: "Home",
      href: "/",
      icon: <Home className="h-4 w-4" />,
      description: "Return to homepage",
    },
    {
      name: "Dashboard",
      href: "/dashboard",
      icon: <BarChart3 className="h-4 w-4" />,
      description: "Health AI readiness scores and metrics",
    },
    {
      name: "Analytics",
      href: "/analytics",
      icon: <Activity className="h-4 w-4" />,
      description: "Live data collection metrics and system performance",
    },
    {
      name: "Country Profiles",
      href: "/countries",
      icon: <Lightbulb className="h-4 w-4" />,
      description: "Explore the data in detailed analysis by country",
    },
    {
      name: "Methodology",
      href: "/methodology",
      icon: <Database className="h-4 w-4" />,
      description: "Data collection, assessment framework, and scoring",
    },
    {
      name: "About",
      href: "/about",
      icon: <Info className="h-4 w-4" />,
      description: "Learn more about AHAII and our other work",
    },
  ];

  const isActive = (href: string) => pathname === href;

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <Image
              src="/images/logos/logo-transparent-bg.png"
              width={60}
              height={30}
              alt="AHAII"
              className="mr-2"
            />
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                AHAII
              </h1>
              <span className="text-xs text-gray-600 dark:text-gray-400 -mt-1 block">
                African Health AI Infrastructure Index
              </span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`group relative px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive(item.href)
                    ? "bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300"
                    : "text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-800/50"
                }`}
              >
                <div className="flex items-center space-x-2">
                  {item.icon}
                  <span>{item.name}</span>
                </div>

                {/* Tooltip */}
                <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 w-48 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded-lg py-2 px-3 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-50">
                  {item.description}
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-900 dark:border-b-gray-700"></div>
                </div>
              </Link>
            ))}

            {/* Language Toggle */}
            <div className="flex items-center space-x-3 ml-4 pl-4 border-l border-gray-200 dark:border-gray-700">
              <button className="text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium px-2 py-1 rounded transition-colors">
                EN
              </button>
              <span className="text-slate-400">|</span>
              <button className="text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 px-2 py-1 rounded transition-colors">
                FR
              </button>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="lg:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              {isOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="lg:hidden border-t border-gray-200 dark:border-gray-700 py-4">
            <div className="space-y-2">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className={`block px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive(item.href)
                      ? "bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300"
                      : "text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-800/50"
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    {item.icon}
                    <div>
                      <div>{item.name}</div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {item.description}
                      </div>
                    </div>
                  </div>
                </Link>
              ))}

              {/* Language Toggle - Mobile */}
              <div className="flex items-center justify-center space-x-3 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  Language:
                </span>
                <button className="text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium px-2 py-1 rounded transition-colors">
                  EN
                </button>
                <span className="text-slate-400">|</span>
                <button className="text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 px-2 py-1 rounded transition-colors">
                  FR
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}