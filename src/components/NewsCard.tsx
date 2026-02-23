import { Clock, ChevronRight } from "lucide-react";

export interface Article {
  id: string;
  title: string;
  excerpt: string;
  category: string;
  readTime: string;
  date: string;
  imageUrl?: string;
  image?: string;
  featured?: boolean;
}

interface NewsCardProps {
  article: Article;
  variant?: "default" | "featured" | "compact";
}

const NewsCard = ({ article, variant = "default" }: NewsCardProps) => {
  // 1. MATCH THE PYTHON FILE NAME EXACTLY (Strip spaces, keep alphanumeric, max 20 chars)
  const safeName = article.title.replace(/[^a-zA-Z0-9]/g, '').substring(0, 20);
  const articleLink = `/${safeName}.html`;

  // 2. FORCE FIX BROKEN IMAGES (If the bot's image fails, React fetches a new one instantly)
  const fallbackImage = `https://image.pollinations.ai/prompt/${encodeURIComponent(article.title + " news photography")}?width=900&height=600&nologo=true`;
  const imgSrc = article.imageUrl || article.image || fallbackImage;

  if (variant === "featured") {
    return (
      <div className="relative rounded-xl overflow-hidden group cursor-pointer animate-fade-up h-full min-h-[420px]">
        <img
          src={imgSrc}
          alt={article.title}
          className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-secondary/95 via-secondary/50 to-transparent" />
        <div className="absolute inset-0 flex flex-col justify-end p-6">
          <span className="inline-block text-xs font-body font-semibold uppercase tracking-widest text-primary mb-2 bg-primary/10 px-2 py-1 rounded w-fit">
            {article.category || "Trending"}
          </span>
          <h2 className="font-headline font-bold text-2xl md:text-3xl text-white leading-tight mb-3 text-balance">
            {article.title}
          </h2>
          <p className="font-body text-sm text-white/75 line-clamp-2 mb-4">{article.excerpt}</p>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 text-white/60 text-xs font-body">
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {article.readTime || "2 min read"}
              </span>
              <span>{article.date || "Today"}</span>
            </div>
            <a
              href={articleLink}
              className="flex items-center gap-1 text-xs font-body font-semibold text-primary bg-primary/10 hover:bg-primary hover:text-primary-foreground px-3 py-1.5 rounded-full transition-all duration-200"
            >
              Read More <ChevronRight className="w-3 h-3" />
            </a>
          </div>
        </div>
      </div>
    );
  }

  if (variant === "compact") {
    return (
      <a href={articleLink} className="flex gap-4 group cursor-pointer py-4 border-b border-border last:border-0 animate-fade-up">
        <img
          src={imgSrc}
          alt={article.title}
          className="w-20 h-20 rounded-lg object-cover flex-shrink-0 transition-opacity group-hover:opacity-90"
          onError={(e) => { e.currentTarget.src = fallbackImage }}
        />
        <div className="flex flex-col justify-between flex-1 min-w-0">
          <div>
            <span className="text-xs font-body font-semibold text-primary uppercase tracking-wider">
              {article.category || "Trending"}
            </span>
            <h3 className="font-headline font-bold text-sm text-foreground leading-snug mt-1 line-clamp-2 group-hover:text-primary transition-colors">
              {article.title}
            </h3>
          </div>
          <div className="flex items-center gap-2 text-xs text-muted-foreground font-body mt-2">
            <Clock className="w-3 h-3" />
            <span>{article.readTime || "2 min read"}</span>
            <span>·</span>
            <span>{article.date || "Today"}</span>
          </div>
        </div>
      </a>
    );
  }

  // Default card
  return (
    <article
      className="group bg-card rounded-xl overflow-hidden border border-border transition-all duration-300 hover:-translate-y-1 animate-fade-up flex flex-col"
      style={{ boxShadow: "var(--card-shadow)" }}
      onMouseEnter={(e) => (e.currentTarget.style.boxShadow = "var(--card-shadow-hover)")}
      onMouseLeave={(e) => (e.currentTarget.style.boxShadow = "var(--card-shadow)")}
    >
      <div className="overflow-hidden aspect-[16/9]">
        <img
          src={imgSrc}
          alt={article.title}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          loading="lazy"
          onError={(e) => { e.currentTarget.src = fallbackImage }}
        />
      </div>
      <div className="flex flex-col flex-1 p-5">
        <div className="flex items-center gap-2 mb-3">
          <span className="text-xs font-body font-semibold text-primary uppercase tracking-wider">
            {article.category || "Trending"}
          </span>
          <span className="text-muted-foreground text-xs">·</span>
          <span className="text-xs text-muted-foreground font-body">{article.date || "Today"}</span>
        </div>
        <h3 className="font-headline font-bold text-lg text-card-foreground leading-snug mb-2 text-balance group-hover:text-primary transition-colors">
          {article.title}
        </h3>
        <p className="font-body text-sm text-muted-foreground leading-relaxed line-clamp-3 flex-1">
          {article.excerpt}
        </p>
        <div className="flex items-center justify-between mt-4 pt-4 border-t border-border">
          <span className="flex items-center gap-1.5 text-xs text-muted-foreground font-body">
            <Clock className="w-3.5 h-3.5" />
            {article.readTime || "2 min read"}
          </span>
          <a
            href={articleLink}
            className="flex items-center gap-1 text-xs font-body font-semibold text-primary hover:text-primary-hover transition-colors group/btn"
          >
            Read More
            <ChevronRight className="w-3.5 h-3.5 transition-transform group-hover/btn:translate-x-0.5" />
          </a>
        </div>
      </div>
    </article>
  );
};

export default NewsCard;
