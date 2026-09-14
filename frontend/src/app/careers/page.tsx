import Link from "next/link";
import { Header } from "@/components/header";
import { Footer } from "@/components/footer";
import { JobApplicationForm } from "@/components/job-application-form";
import { AnimatedHeading } from "@/components/animated-heading";
import { API_URL } from "@/lib/api";
type Job = {
  id: string;
  title: string;
  slug: string;
  department: string;
  job_type: string;
  location: string;
  application_deadline: string;
};
type Block = {
  key: string;
  title: string;
  body: string;
  image?: string;
  payload?: Record<string, unknown>;
};
export const metadata = { title: "Careers" };
export default async function Careers() {
  let jobs: Job[] = [];
  let content: Block[] = [];
  try {
    const [jobResponse, homeResponse] = await Promise.all([
      fetch(`${API_URL}/jobs/?page_size=50`, { cache: "no-store" }),
      fetch(`${API_URL}/home/`, { cache: "no-store" }),
    ]);
    const jobBody = await jobResponse.json(),
      homeBody = await homeResponse.json(),
      home = homeBody.data || homeBody;
    jobs = jobBody.data || jobBody.results || [];
    content = home.content || [];
  } catch {}
  const primary = jobs[0],
    block = (key: string) => content.find((item) => item.key === key),
    hero = block("careers-hero"),
    intro = block("careers-introduction"),
    application = block("careers-application-panel"),
    paragraphs = (intro?.body || "").split(/\n\s*\n/).filter(Boolean);
  return (
    <>
      <Header />
      <main className="career-page">
        <section
          className="career-hero"
          style={hero?.image ? { backgroundImage: `url("${hero.image}")` } : undefined}
        >
          <div className="career-hero-shade" />
          <div className="shell">
            <p>{String(hero?.payload?.label || "Build your future with us")}</p>
            <AnimatedHeading as="h1">{hero?.title || "Career"}</AnimatedHeading>
          </div>
        </section>
        <section className="career-content">
          <div className="shell">
            <div className="career-intro">
              <p>{String(intro?.payload?.label || "Our people")}</p>
              <AnimatedHeading>{intro?.title || "Why Join Us?"}</AnimatedHeading>
              <div>
                {(paragraphs.length ? paragraphs : ["Add careers introduction content from the admin panel."]).map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
              </div>
            </div>
            {primary ? (
              <>
                <div className="career-opening">
                  <div>
                    <span>Current opening · {primary.department}</span>
                    <h3>{primary.title}</h3>
                    <p>
                      {primary.location} ·{" "}
                      {primary.job_type.replaceAll("_", " ")} · Apply by{" "}
                      {primary.application_deadline}
                    </p>
                  </div>
                  <Link href={`/careers/${primary.slug}`}>View Position →</Link>
                </div>
                <div className="career-apply">
                  <div
                    className="career-apply-image"
                    style={application?.image ? { backgroundImage: `url("${application.image}")` } : undefined}
                  >
                    <div>
                      <span>{String(application?.payload?.image_label || "Join the team")}</span>
                      <AnimatedHeading>{String(application?.payload?.image_title || "Do meaningful work with great people.")}</AnimatedHeading>
                    </div>
                  </div>
                  <JobApplicationForm job={primary.id} label={String(application?.payload?.label || "Apply now")} title={application?.title || "Submit your application"} />
                </div>
              </>
            ) : (
              <div className="career-no-opening">
                <h3>There are no open positions right now.</h3>
                <p>Please check again soon for new opportunities.</p>
              </div>
            )}
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
