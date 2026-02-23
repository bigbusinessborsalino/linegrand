import { Link } from "react-router-dom";
import { Anchor, Twitter, Github, Rss } from "lucide-react";

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-card mt-16">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          {/* Brand */}
          <div>
            <Link to="/" className="flex items-center gap-2.5 mb-3 group w-fit">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                <Anchor className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="font-headline font-bold text-lg text-foreground">Grand Line News</span>
            </Link>
            <p className="text-sm text-muted-foreground font-body leading-relaxed max-w-xs">
              Navigating the world's stories, compiled and rephrased by AI from current web trends.
            </p>
            <div className="flex gap-3 mt-5">
              {[Twitter, Github, Rss].map((Icon, i) => (
                <a
                  key={i}
                  href="#"
                  className="w-8 h-8 flex items-center justify-center rounded-full border border-border text-muted-foreground hover:text-primary hover:border-primary transition-colors"
                >
                  <Icon className="w-4 h-4" />
                </a>
              ))}
            </div>
          </div>

          {/* Topics */}
          <div>
            <h4 className="font-headline font-semibold text-sm uppercase tracking-widest text-muted-foreground mb-4">
              Topics
            </h4>
            <ul className="space-y-2">
              {["World", "Technology", "Science", "Culture", "Business"].map((t) => (
                <li key={t}>
                  <Link
                    to="/"
                    className="text-sm font-body text-muted-foreground hover:text-primary transition-colors"
                  >
                    {t}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-headline font-semibold text-sm uppercase tracking-widest text-muted-foreground mb-4">
              Legal
            </h4>
            <ul className="space-y-2">
              <li>
                <Link
                  to="/terms"
                  className="text-sm font-body text-muted-foreground hover:text-primary transition-colors"
                >
                  Terms & Conditions
                </Link>
              </li>
              <li>
                <Link
                  to="/disclaimer"
                  className="text-sm font-body text-muted-foreground hover:text-primary transition-colors"
                >
                  Disclaimer
                </Link>
              </li>
              <li>
                <Link
                  to="/"
                  className="text-sm font-body text-muted-foreground hover:text-primary transition-colors"
                >
                  Privacy Policy
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-border mt-10 pt-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-xs text-muted-foreground font-body">
            © {year} Grand Line News. All rights reserved.
          </p>
          <p className="text-xs text-muted-foreground font-body text-center">
            Content compiled & rephrased by AI. For informational purposes only.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
