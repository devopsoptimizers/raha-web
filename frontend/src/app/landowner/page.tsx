import { Footer } from "@/components/footer";
import { Header } from "@/components/header";
import { LandownerForm } from "@/components/landowner-form";
import { AnimatedHeading } from "@/components/animated-heading";
import { API_URL } from "@/lib/api";
export const metadata = { title: "Landowner" };
type Block = { key: string; title: string; body: string; image?: string; payload?: Record<string, unknown> };
const defaultBenefits = [
  "Faster project execution through careful planning and proven construction expertise",
  "Elegant, contemporary architecture with intelligently designed spaces",
  "Rigorous quality control and benchmark materials",
  "Elevated living standards with thoughtfully selected amenities",
  "Responsive customer care and dedicated after-sales support",
  "Long-term value across promising locations in Dhaka",
];
export default async function Landowner() {
  let content: Block[] = [];
  try {
    const response = await fetch(`${API_URL}/home/`, { cache: "no-store" }), body = await response.json();
    content = (body.data || body).content || [];
  } catch {}
  const block = (key: string) => content.find((item) => item.key === key),
    hero = block("landowner-hero"),
    intro = block("landowner-introduction"),
    formSection = block("landowner-form-section"),
    configuredBenefits = intro?.payload?.benefits,
    benefits = Array.isArray(configuredBenefits) ? configuredBenefits.map(String) : defaultBenefits;
  return (
    <>
      <Header />
      <main className="landowner-page">
        <section className="landowner-hero" style={hero?.image ? { backgroundImage: `linear-gradient(90deg,rgba(0,25,45,.55),rgba(0,25,45,.12)),url("${hero.image}")` } : undefined}>
          <div className="shell">
            <p>{String(hero?.payload?.label || "Partner with Raha Holdings")}</p>
            <AnimatedHeading as="h1">{hero?.title || "Landowner"}</AnimatedHeading>
          </div>
        </section>
        <section className="landowner-intro">
          <div className="landowner-intro-copy">
            <div>
              <p className="ref-kicker">{String(intro?.payload?.label || "Landowners")}</p>
              <AnimatedHeading>{intro?.title || "Build something enduring with us"}</AnimatedHeading>
              <p>{intro?.body || "Raha Holdings partners with landowners to create considered developments founded on transparency, design quality, and shared long-term value."}</p>
              <AnimatedHeading as="h3">{String(intro?.payload?.benefits_title || "Why choose Raha Holdings?")}</AnimatedHeading>
              <ul>
                {benefits.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
          <div className="landowner-intro-image" style={intro?.image ? { backgroundImage: `url("${intro.image}")` } : undefined} />
        </section>
        <section className="landowner-contact">
          <div className="shell">
            <p className="ref-kicker">{String(formSection?.payload?.label || "Start a conversation")}</p>
            <AnimatedHeading>{formSection?.title || "Meet the Professionals"}</AnimatedHeading>
            <LandownerForm />
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
