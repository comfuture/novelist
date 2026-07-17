import type { Metadata } from "next";
import { headers } from "next/headers";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host = requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host") ?? "localhost:3000";
  const protocol = requestHeaders.get("x-forwarded-proto") ?? (host.startsWith("localhost") ? "http" : "https");
  const origin = `${protocol}://${host}`;

  return {
    metadataBase: new URL(origin),
    title: { default: "Novelist — Build continuity-safe novels", template: "%s — Novelist" },
    description: "Plan, write, illustrate, and publish structured Markdown novels with continuity-safe Codex workflows.",
    icons: { icon: "/logo.png", shortcut: "/logo.png", apple: "/logo.png" },
    openGraph: {
      title: "Novelist — Keep the whole novel in view",
      description: "A Codex plugin for continuity-safe writing and validated EPUB publishing.",
      type: "website",
      url: origin,
      images: [{ url: `${origin}/og.png`, width: 1200, height: 630, alt: "Novelist Codex plugin" }],
    },
    twitter: {
      card: "summary_large_image",
      title: "Novelist — Keep the whole novel in view",
      description: "A Codex plugin for continuity-safe writing and validated EPUB publishing.",
      images: [`${origin}/og.png`],
    },
  };
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>{children}</body>
    </html>
  );
}
