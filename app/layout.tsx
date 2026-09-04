import type { Metadata, Viewport } from "next";
import { siteUrl } from "@/lib/site";
import { emailAddress, freelanceProfileUrl, telegramUrl } from "@/lib/contact";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: "Telegram-боты, AI-автоматизация и веб-сервисы — Александр",
  description:
    "Разработка Telegram-ботов, AI-автоматизации, веб-сервисов и интеграций под задачи бизнеса — от прототипа до стабильного запуска.",
  keywords: [
    "AI автоматизация",
    "разработка веб-сервисов",
    "Telegram боты",
    "цифровые продукты",
    "интеграции",
  ],
  authors: [{ name: "Александр" }],
  creator: "Александр",
  applicationName: "Портфолио Александра",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    locale: "ru_RU",
    url: "/",
    siteName: "Alexuys — разработка цифровых продуктов",
    title: "Telegram-боты, AI-автоматизация и веб-сервисы — Александр",
    description:
      "Разработка Telegram-ботов, AI-автоматизации, веб-сервисов и интеграций — от прототипа до стабильного запуска.",
  },
  twitter: {
    card: "summary",
    title: "Telegram-боты, AI-автоматизация и веб-сервисы — Александр",
    description:
      "Разработка Telegram-ботов, AI-автоматизации, веб-сервисов и интеграций — от прототипа до стабильного запуска.",
  },
  robots: {
    index: true,
    follow: true,
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  colorScheme: "dark",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const structuredData = [
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "@id": `${siteUrl}/#website`,
      url: `${siteUrl}/`,
      name: "Alexuys — разработка цифровых продуктов",
      inLanguage: "ru-RU",
    },
    {
      "@context": "https://schema.org",
      "@type": "Person",
      "@id": `${siteUrl}/#person`,
      name: "Александр",
      url: `${siteUrl}/`,
      jobTitle: "Разработчик цифровых продуктов и автоматизации",
      description: "Разрабатывает Telegram-ботов, AI-автоматизацию, веб-сервисы и интеграции под задачи бизнеса.",
      email: emailAddress,
      sameAs: [telegramUrl, freelanceProfileUrl],
      knowsAbout: [
        "AI-автоматизация",
        "разработка веб-сервисов",
        "разработка Telegram-ботов",
        "API-интеграции",
        "доработка IT-проектов",
      ],
    },
    {
      "@context": "https://schema.org",
      "@type": "ProfilePage",
      "@id": `${siteUrl}/#profile`,
      url: `${siteUrl}/`,
      name: "Портфолио разработчика цифровых продуктов Александра",
      inLanguage: "ru-RU",
      isPartOf: { "@id": `${siteUrl}/#website` },
      mainEntity: { "@id": `${siteUrl}/#person` },
    },
  ];

  return (
    <html lang="ru">
      <body className="antialiased">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(structuredData).replace(/</g, "\\u003c"),
          }}
        />
        {children}
      </body>
    </html>
  );
}
