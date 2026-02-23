import { Link } from "react-router-dom";
import { TrendingUp, ChevronRight } from "lucide-react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import NewsFeed from "../components/NewsFeed";
import { mockArticles, trendingTopics } from "../data/articles";
import heroBg from "../assets/hero-bg.jpg";

interface HomeProps {
  theme: "light" | "dark";
  onToggleTheme: () => void;
}

const Home = ({ theme, onToggleTheme }: HomeProps) => {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header theme={theme} onToggleTheme={onToggleTheme} />

      {/* Hero Section */}
      <section className="relative w-full overflow-hidden" style={{ minHeight: "420px" }}>
        <img
          src={heroBg}
          alt="Grand Line News hero"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0" style={{ background: "var(--hero-overlay)" }} />

        <div className="relative container mx-auto px-4 py-20 flex flex-col items-start justify-end h-full" style={{ minHeight: "420px" }}>
          <div className="animate-fade-up max-w-2xl">
            <div className="flex items-center gap-2 mb-4">
              <span className="bg-primary text-primary-foreground text-xs font-body font-semibold uppercase tracking-widest px-3 py-1.5 rounded-full">
                Trending Now
              </span>
              <TrendingUp className="w-4 h-4 text-primary" />
            </div>
            <h1 className="font-headline font-black text-4xl md:text-5xl lg:text-6xl text-white leading-tight mb-4 text-balance">
              Navigate the World's Stories
            </h1>
            <p className="font-body text-white/75 text-lg max-w-xl mb-6">
              AI-researched and rephrased news from across the globe, curated for clarity and depth.
            </p>

            {/* Trending Topics */}
            <div className="flex flex-wrap gap-2">
              {trendingTopics.map((topic) => (
                <Link
                  key={topic}
                  to="/"
                  className="flex items-center gap-1 text-xs font-body font-medium text-white/80 hover:text-white bg-white/10 hover:bg-white/20 border border-white/20 px-3 py-1.5 rounded-full transition-all duration-200"
                >
                  {topic}
                  <ChevronRight className="w-3 h-3" />
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* News Feed */}
      <main className="flex-1">
        <NewsFeed articles={mockArticles} />
      </main>

      <Footer />
    </div>
  );
};

export default Home;
