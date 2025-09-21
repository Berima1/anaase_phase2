import Header from "../components/Header";
import Footer from "../components/Footer";
import Hero from "../components/Hero";
import AskAnaase from "../components/AskAnaase";

export default function Home() {
  return (
    <div>
      <Header />
      <main>
        <Hero />
        <AskAnaase />
      </main>
      <Footer />
    </div>
  );
}
