import { Link } from "react-router-dom";
import { ArrowLeft, AlertTriangle, Bot, Globe, Shield } from "lucide-react";
import Header from "../components/Header";
import Footer from "../components/Footer";

interface DisclaimerProps {
  theme: "light" | "dark";
  onToggleTheme: () => void;
}

const Disclaimer = ({ theme, onToggleTheme }: DisclaimerProps) => {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header theme={theme} onToggleTheme={onToggleTheme} />

      <main className="flex-1 container mx-auto px-4 py-12 max-w-3xl">
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-sm font-body text-muted-foreground hover:text-primary transition-colors mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to News
        </Link>

        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-full bg-accent flex items-center justify-center flex-shrink-0">
            <AlertTriangle className="w-5 h-5 text-accent-foreground" />
          </div>
          <span className="text-xs font-body font-semibold text-primary uppercase tracking-widest">Legal Notice</span>
        </div>

        <h1 className="font-headline font-black text-4xl text-foreground mb-2 animate-fade-up">
          Disclaimer
        </h1>
        <p className="font-body text-muted-foreground mb-10">
          Please read this disclaimer carefully before using Grand Line News.
        </p>

        {/* Key disclaimer box */}
        <div className="bg-accent border-l-4 border-primary rounded-r-xl px-6 py-5 mb-10 animate-fade-up">
          <div className="flex items-start gap-3">
            <Bot className="w-6 h-6 text-accent-foreground flex-shrink-0 mt-0.5" />
            <div>
              <h2 className="font-headline font-bold text-lg text-foreground mb-2">AI-Generated Content Notice</h2>
              <p className="font-body text-foreground leading-relaxed text-base">
                All news articles on this platform are researched, compiled, and rephrased by Artificial Intelligence based on current web trends.
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-10 animate-fade-up">
          {/* Section 1 */}
          <div className="flex gap-5">
            <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center flex-shrink-0 mt-1">
              <Bot className="w-5 h-5 text-muted-foreground" />
            </div>
            <div>
              <h2 className="font-headline font-bold text-xl text-foreground mb-3">Nature of AI-Generated Content</h2>
              <p className="font-body text-muted-foreground leading-relaxed mb-3">
                Grand Line News uses advanced Artificial Intelligence systems to research, compile, and rephrase news articles based on publicly available information and current web trends. The AI processes large volumes of data to identify, summarize, and present information in a readable format.
              </p>
              <p className="font-body text-muted-foreground leading-relaxed">
                While we employ sophisticated AI systems, the content generated may contain inaccuracies, omissions, or interpretations that differ from original source material. Readers are encouraged to verify important information through primary sources.
              </p>
            </div>
          </div>

          <div className="h-px bg-border" />

          {/* Section 2 */}
          <div className="flex gap-5">
            <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center flex-shrink-0 mt-1">
              <Globe className="w-5 h-5 text-muted-foreground" />
            </div>
            <div>
              <h2 className="font-headline font-bold text-xl text-foreground mb-3">No Guarantee of Accuracy</h2>
              <p className="font-body text-muted-foreground leading-relaxed mb-3">
                The information provided on this platform is for general informational purposes only. Grand Line News makes no representations or warranties of any kind, express or implied, regarding the accuracy, completeness, reliability, or suitability of the information contained herein.
              </p>
              <p className="font-body text-muted-foreground leading-relaxed">
                Any reliance you place on the information presented is strictly at your own risk. We strongly advise you to consult authoritative news sources, official government publications, or qualified professionals for decisions of any significance.
              </p>
            </div>
          </div>

          <div className="h-px bg-border" />

          {/* Section 3 */}
          <div className="flex gap-5">
            <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center flex-shrink-0 mt-1">
              <Shield className="w-5 h-5 text-muted-foreground" />
            </div>
            <div>
              <h2 className="font-headline font-bold text-xl text-foreground mb-3">Limitation of Liability</h2>
              <p className="font-body text-muted-foreground leading-relaxed mb-3">
                Grand Line News, its owners, operators, employees, or affiliates shall not be held liable for any loss, damage, or negative consequence — direct or indirect — arising from your reliance on information provided on this platform.
              </p>
              <p className="font-body text-muted-foreground leading-relaxed">
                This includes, but is not limited to, financial loss, reputational harm, or decisions made based on AI-generated content published here. Users assume full responsibility for how they use the information provided.
              </p>
            </div>
          </div>

          <div className="h-px bg-border" />

          {/* Section 4 */}
          <div className="pb-2">
            <h2 className="font-headline font-bold text-xl text-foreground mb-3">Third-Party Sources</h2>
            <p className="font-body text-muted-foreground leading-relaxed mb-3">
              Our AI systems draw from a wide variety of publicly available web sources. We do not claim ownership of the original facts or events described in any article. Links to third-party websites, where provided, do not constitute an endorsement of those sites or their content.
            </p>
            <p className="font-body text-muted-foreground leading-relaxed">
              This disclaimer was last updated on February 20, 2026. For questions, contact us at{" "}
              <a href="mailto:legal@grandlinenews.example.com" className="text-primary hover:underline">
                legal@grandlinenews.example.com
              </a>.
            </p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Disclaimer;
