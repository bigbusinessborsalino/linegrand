import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Clock, Calendar, Share2, Bookmark } from "lucide-react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import NewsCard from "../components/NewsCard";

interface ArticleProps {
  theme: "light" | "dark";
  onToggleTheme: () => void;
}

const Article = ({ theme, onToggleTheme }: ArticleProps) => {
  const { id } = useParams<{ id: string }>();
  const [article, setArticle] = useState<any>(null);
  const [related, setRelated] = useState<any[]>([]);

  useEffect(() => {
    // 🚀 Fetches the exact article from your database
    fetch('https://smart-corine-gojosggh-59868182.koyeb.app/api/news')
      .then(res => res.json())
      .then(data => {
        const formattedData = data.map((a: any) => ({
            ...a,
            id: a.id || a.title.replace(/[^a-zA-Z0-9]/g, '').substring(0, 20)
        }));
        
        const found = formattedData.find((a: any) => a.id === id);
        if (found) {
          setArticle(found);
          setRelated(formattedData.filter((a: any) => a.id !== id).slice(0, 3));
        }
      })
      .catch(err => console.error("Error fetching article:", err));
  }, [id]);

  if (!article) {
    return (
      <div className="min-h-screen bg-background flex flex-col">
        <Header theme={theme} onToggleTheme={onToggleTheme} />
        <main className="flex-1 flex items-center justify-center">
          <div className="text-center py-20 text-muted-foreground font-body">Loading AI Article...</div>
        </main>
        <Footer />
      </div>
    );
  }

  // Grabs the full story from MongoDB, or falls back to the excerpt
  const contentToDisplay = article.full_content || article.excerpt || "Content generating...";

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header theme={theme} onToggleTheme={onToggleTheme} />

      <main className="flex-1">
        {article.imageUrl && (
          <div className="w-full relative overflow-hidden" style={{ maxHeight: "480px" }}>
            <img
              src={article.imageUrl}
              alt={article.title}
              className="w-full h-full object-cover animate-fade-in"
              style={{ maxHeight: "480px" }}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent" />
          </div>
        )}

        <article className="container mx-auto px-4 py-10 max-w-3xl">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-sm font-body text-muted-foreground hover:text-primary transition-colors mb-8"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to News
          </Link>

          <div className="mb-4">
            <span className="text-xs font-body font-semibold text-primary uppercase tracking-widest bg-accent px-3 py-1.5 rounded-full">
              {article.category || "Trending"}
            </span>
          </div>

          <h1 className="font-headline font-black text-3xl md:text-4xl lg:text-5xl text-foreground leading-tight mb-6 text-balance animate-fade-up">
            {article.title}
          </h1>

          <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground font-body mb-8 pb-8 border-b border-border">
            <span className="flex items-center gap-1.5">
              <Calendar className="w-4 h-4" />
              {article.date}
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="w-4 h-4" />
              {article.readTime || "3 min read"}
            </span>
            <div className="flex-1" />
            <button className="flex items-center gap-1.5 hover:text-primary transition-colors">
              <Bookmark className="w-4 h-4" />
              Save
            </button>
            <button className="flex items-center gap-1.5 hover:text-primary transition-colors">
              <Share2 className="w-4 h-4" />
              Share
            </button>
          </div>

          <div className="bg-accent border border-primary/20 rounded-lg px-4 py-3 mb-8 flex items-start gap-3">
            <div className="w-5 h-5 rounded-full bg-primary flex-shrink-0 flex items-center justify-center mt-0.5">
              <span className="text-primary-foreground text-[10px] font-bold">AI</span>
            </div>
            <p className="text-xs font-body text-muted-foreground leading-relaxed">
              This article was researched, compiled, and rephrased by Artificial Intelligence based on current web trends.{" "}
              <Link to="/disclaimer" className="text-primary underline underline-offset-2 hover:text-primary-hover">
                Read our disclaimer.
              </Link>
            </p>
          </div>

          <div className="prose prose-lg max-w-none">
            {contentToDisplay.split("\n").map((para: string, i: number) => {
              if (!para.trim()) return null;
              return (
                <p
                  key={i}
                  className="font-body text-foreground leading-[1.85] text-[1.0625rem] mb-6 animate-fade-up"
                  style={{ animationDelay: `${(i % 5) * 0.05}s` }}
                >
                  {para}
                </p>
              );
            })}
          </div>
        </article>

        {related.length > 0 && (
          <section className="container mx-auto px-4 pb-16 max-w-5xl">
            <div className="flex items-center gap-4 mb-8">
              <div className="w-1 h-6 bg-primary rounded-full" />
              <h2 className="font-headline font-bold text-2xl text-foreground">Related Stories</h2>
              <div className="flex-1 h-px bg-border" />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              {related.map((a) => (
                <NewsCard key={a.id} article={a} variant="default" />
              ))}
            </div>
          </section>
        )}
      </main>

      <Footer />
    </div>
  );
};

export default Article;
