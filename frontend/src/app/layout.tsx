import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "文本转思维导图",
  description: "将文本转换为思维导图",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh">
      <body>{children}</body>
    </html>
  );
}