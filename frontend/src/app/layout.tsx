import "./globals.css";
import React from "react";

export const metadata = {
  title: "NetraGati Command Center",
  description: "City ANPR & Spatial Intercept Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
