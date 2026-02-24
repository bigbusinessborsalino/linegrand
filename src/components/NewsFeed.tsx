import { useEffect, useState } from "react";
import NewsCard, { Article } from "./NewsCard";

const NewsFeed = () => {
  const [articles, setArticles] = useState<Article[]>([]);

  useEffect(() => {
    const fetchLiveNews = async () => {
      try {
        // 🚀 Connected directly to your live database API!
        const response = await fetch('https://smart-corine-gojosggh-59868182.koyeb.app/api/news');
        const liveData = await response.json();
        
        // Formats the database data so your UI can read it
        const formattedData = liveData.map((a: any) => ({
            ...a,
            id: a.id || a.title.replace(/[^a-zA-Z0-9]/g, '').substring(0, 20)
        }));
        
        setArticles(formattedData);
      } catch (err) {
        console.error("Waiting for bot data...", err);
      }
    };

    fetchLiveNews();
    const interval = setInterval(fetchLiveNews, 300000); // Auto-refreshes every 5 mins
    return () => clearInterval(interval);
  }, []);

  if (articles.length === 0) {
    return (
      <div className="text-center py-20 text-muted-foreground font-body">
        📡 Scanning the Grand Line for News...
      </div>
    );
  }

  const [featured, ...rest] = articles;

  return (
    <section className="container mx-auto px-4 py-10">
      <div className="flex items-center gap-4 mb-8">
        <div className="w-1 h-6 bg-primary rounded-full" />
        <h2 className="font-headline font-bold text-2xl text-foreground">Latest Stories</h2>
        <div className="flex-1 h-px bg-border" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">
        <div className="lg:col-span-2">
          {featured && <NewsCard article={featured} variant="featured" />}
        </div>
        <div className="flex flex-col justify-between">
          <div className="bg-card border border-border rounded-xl p-5 h-full" style={{ boxShadow: "var(--card-shadow)" }}>
            <div className="flex items-center gap-2 mb-2 pb-3 border-b border-border">
              <div className="w-1 h-4 bg-primary rounded-full" />
              <h3 className="font-headline font-semibold text-sm uppercase tracking-widest text-muted-foreground">
                Top Stories
              </h3>
            </div>
            {rest.slice(0, 3).map((article) => (
              <NewsCard key={article.id} article={article} variant="compact" />
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {rest.slice(3).map((article) => (
          <NewsCard key={article.id} article={article} variant="default" />
        ))}
      </div>
    </section>
  );
};

export default NewsFeed;
