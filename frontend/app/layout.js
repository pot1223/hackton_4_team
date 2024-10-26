import localFont from "next/font/local";
import "./globals.css";
import Header from "./components/Header";


const pretendard = localFont({
  src: "../static/fonts/PretendardVariable.woff2",
  display: "swap",
  weight: "45 920",
  variable: "--font-pretendard",
});

export default function RootLayout({ children }) {
  return (
    <html lang="kr" className={`${pretendard.variable}`}>
      <body className={pretendard.className}>
        <Header/>
        {children}
      </body>
    </html>
  );
}
