import { Link } from "react-router-dom";
import { ArrowLeft, FileText } from "lucide-react";
import Header from "../components/Header";
import Footer from "../components/Footer";

interface TermsProps {
  theme: "light" | "dark";
  onToggleTheme: () => void;
}

const sections = [
  {
    title: "1. Acceptance of Terms",
    body: "By accessing and using Grand Line News ('the Platform'), you accept and agree to be bound by the terms and provisions of this agreement. If you do not agree to abide by these terms, please do not use this service.",
  },
  {
    title: "2. Use of Content",
    body: "All content published on Grand Line News is for general informational purposes only. You may view, download, and print pages from the Platform subject to the conditions set out below. You must not reproduce, duplicate, copy, sell, resell, or exploit any portion of the Platform without express written permission.",
  },
  {
    title: "3. AI-Generated Content",
    body: "The content on this Platform is researched, compiled, and rephrased by Artificial Intelligence based on current web trends and publicly available information. While we strive for accuracy, we make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, or suitability of the information.",
  },
  {
    title: "4. Intellectual Property",
    body: "Unless otherwise stated, Grand Line News and/or its licensors own the intellectual property rights for all material on the Platform. All intellectual property rights are reserved. You may access this from Grand Line News for your own personal use subject to restrictions set in these terms.",
  },
  {
    title: "5. Limitation of Liability",
    body: "In no event shall Grand Line News, its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your access to or use of (or inability to access or use) the service.",
  },
  {
    title: "6. Links to Other Websites",
    body: "Our Platform may contain links to third-party websites or services that are not owned or controlled by Grand Line News. We have no control over, and assume no responsibility for, the content, privacy policies, or practices of any third-party websites or services.",
  },
  {
    title: "7. Privacy",
    body: "Your use of Grand Line News is also governed by our Privacy Policy. Please review our Privacy Policy, which is incorporated into these Terms by this reference. By using the Platform, you agree to be bound by our Privacy Policy.",
  },
  {
    title: "8. Changes to Terms",
    body: "Grand Line News reserves the right, at its sole discretion, to modify or replace these Terms at any time. What constitutes a material change will be determined at our sole discretion. By continuing to access or use our Platform after those revisions become effective, you agree to be bound by the revised terms.",
  },
  {
    title: "9. Contact Information",
    body: "If you have any questions about these Terms, please contact us at legal@grandlinenews.example.com. These Terms were last updated on February 20, 2026.",
  },
];

const Terms = ({ theme, onToggleTheme }: TermsProps) => {
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
            <FileText className="w-5 h-5 text-accent-foreground" />
          </div>
          <span className="text-xs font-body font-semibold text-primary uppercase tracking-widest">Legal</span>
        </div>

        <h1 className="font-headline font-black text-4xl text-foreground mb-2 animate-fade-up">
          Terms & Conditions
        </h1>
        <p className="font-body text-muted-foreground mb-10">
          Last updated: February 20, 2026 · Effective immediately upon use of this platform.
        </p>

        <div className="space-y-8 animate-fade-up">
          {sections.map((section) => (
            <div key={section.title} className="pb-8 border-b border-border last:border-0">
              <h2 className="font-headline font-bold text-xl text-foreground mb-3">{section.title}</h2>
              <p className="font-body text-muted-foreground leading-relaxed">{section.body}</p>
            </div>
          ))}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Terms;
