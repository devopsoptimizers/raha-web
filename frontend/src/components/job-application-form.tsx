"use client";
import { FormEvent, useState } from "react";
import { API_URL } from "@/lib/api";
import { SubmissionSuccessModal } from "@/components/submission-success-modal";
export function JobApplicationForm({
  job,
  label = "Apply now",
  title = "Submit your application",
}: {
  job: string;
  label?: string;
  title?: string;
}) {
  const [state, setState] = useState("");
  const [fileName, setFileName] = useState("");
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!window.confirm("Are you sure you want to submit this job application?")) return;
    setState("Submitting…");
    const form = e.currentTarget;
    const data = new FormData(form);
    try {
      const r = await fetch(`${API_URL}/jobs/${job}/apply/`, {
        method: "POST",
        body: data,
      });
      if (r.ok) {
        form.reset();
        setFileName("");
        setState("Application received. Thank you.");
      } else {
        const body = await r.json().catch(() => ({}));
        const errors = body.errors || body;
        const first = Object.values(errors).flat().find(Boolean);
        setState(
          String(
            first ||
              body.message ||
              "Unable to submit. Check every field and try again.",
          ),
        );
      }
    } catch {
      setState(
        "Unable to connect. Please check your connection and try again.",
      );
    }
  }
  return (
    <>
    <aside className="career-application-card">
      <p className="eyebrow">{label}</p>
      <h2>{title}</h2>
      <form onSubmit={submit} className="career-application-form">
        <label className="career-field-full">
          <span>
            Full Name <b>*</b>
          </span>
          <input name="applicant_name" required placeholder="Full Name" />
        </label>
        <label>
          <span>
            Contact Number <b>*</b>
          </span>
          <input
            name="phone"
            type="tel"
            required
            placeholder="017XXXXXXXX"
            pattern="(?:\+?88)?01[3-9]\d{8}"
          />
        </label>
        <label>
          <span>
            Email <b>*</b>
          </span>
          <input name="email" type="email" required placeholder="Email" />
        </label>
        <label>
          <span>
            Years of Experience <b>*</b>
          </span>
          <input name="years_of_experience" required placeholder="Text" />
        </label>
        <label>
          <span>
            Previous Organization <b>*</b>
          </span>
          <input name="previous_organization" required placeholder="Text" />
        </label>
        <label>
          <span>
            Education Degree <b>*</b>
          </span>
          <input name="education_degree" required placeholder="Text" />
        </label>
        <label>
          <span>
            Education Institution <b>*</b>
          </span>
          <input name="education_institution" required placeholder="Text" />
        </label>
        <label className="career-field-full">
          <span>
            Upload CV <b>*</b>
          </span>
          <span className="career-cv-upload">
            <input
              name="cv"
              type="file"
              accept=".pdf,.doc,.docx"
              required
              onChange={(event) =>
                setFileName(event.target.files?.[0]?.name || "")
              }
            />
            <strong>{fileName || "Upload Resume"}</strong>
          </span>
        </label>
        <label className="career-field-full">
          <span>
            Cover Letter <b>*</b>
          </span>
          <textarea name="cover_letter" rows={5} required placeholder="Text" />
        </label>
        {state && state !== "Application received. Thank you." && <p className="career-application-state">{state}</p>}
        <button
          className="career-application-submit"
          disabled={state === "Submitting…"}
        >
          {state === "Submitting…" ? "Submitting…" : "Submit application"}
        </button>
      </form>
    </aside>
    {state === "Application received. Thank you." && (
      <SubmissionSuccessModal
        title="Application received."
        message="Thank you for applying. Our recruitment team will review your application and contact you if your experience matches the role."
        onClose={() => setState("")}
      />
    )}
    </>
  );
}
