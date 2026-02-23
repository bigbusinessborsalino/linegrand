import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Sun, Moon, Menu, X, Anchor } from "lucide-react";

interface HeaderProps {
  theme: "light" | "dark";
  onToggleTheme: () => void;
}

const navItems = [
  { label: "Home", to: "/" },
  { label: "World", to: "/" },
  { label: "Technology", to: "/" },
  { label: "Science", to: "/" },
];

const Header = ({ theme, onToggleTheme }: HeaderProps) => {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  return (
    <header
      className={`sticky top-0 z-50 w-full transition-all duration-300 ${
        scrolled
          ? "shadow-md backdrop-blur-md bg-[var(--header-bg)] border-b border-[var(--header-border)]"
          : "bg-[var(--header-bg)] border-b border-[var(--header-border)]"
      }`}
    >
      {/* Top bar */}
      <div className="bg-primary text-primary-foreground text-xs py-1.5 px-4 text-center font-body tracking-wide">
        Breaking: Stay informed with the latest from the Grand Line
      </div>

      <div className="container mx-auto flex items-center justify-between h-16 px-4">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0 transition-transform group-hover:scale-105">
            <Anchor className="w-4 h-4 text-primary-foreground" />
          </div>
          <div>
            <span className="font-headline font-bold text-xl leading-none tracking-tight text-foreground">
              Grand Line
            </span>
            <span className="block text-[10px] font-body uppercase tracking-[0.2em] text-muted-foreground leading-none mt-0.5">
              News
            </span>
          </div>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-1">
          {navItems.map((item) => (
            <Link
              key={item.label}
              to={item.to}
              className="px-3 py-2 text-sm font-body font-medium text-muted-foreground hover:text-foreground hover:bg-muted rounded-md transition-colors"
            >
              {item.label}
            </Link>
          ))}
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={onToggleTheme}
            aria-label="Toggle theme"
            className="w-9 h-9 flex items-center justify-center rounded-full border border-border hover:bg-muted transition-colors text-muted-foreground hover:text-foreground"
          >
            {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>

          {/* Mobile menu */}
          <button
            onClick={() => setMenuOpen((v) => !v)}
            aria-label="Toggle menu"
            className="md:hidden w-9 h-9 flex items-center justify-center rounded-full border border-border hover:bg-muted transition-colors text-muted-foreground"
          >
            {menuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="md:hidden border-t border-border bg-card animate-fade-in">
          <nav className="flex flex-col p-3 gap-1">
            {navItems.map((item) => (
              <Link
                key={item.label}
                to={item.to}
                className="px-4 py-3 text-sm font-body font-medium text-foreground hover:bg-muted rounded-md transition-colors"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      )}
    </header>
  );
};

export default Header;
