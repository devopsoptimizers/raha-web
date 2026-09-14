"use client";
import { FormEvent, useEffect, useRef, useState } from "react";
import { API_URL } from "@/lib/api";
import { SubmissionConfirmModal } from "@/components/submission-confirm-modal";
import { SubmissionSuccessModal } from "@/components/submission-success-modal";
import { Captcha } from "@/components/captcha";
type Location = { id: string; name: string };

async function getLocations(path: string): Promise<Location[]> {
  const separator = path.includes("?") ? "&" : "?";
  const response = await fetch(`${API_URL}/${path}${separator}page_size=100`);
  if (!response.ok) throw new Error("Unable to load locations.");
  const body = await response.json();
  return body.data?.data || body.data || [];
}

export function LandownerForm() {
  const [state, setState] = useState("");
  const [divisions, setDivisions] = useState<Location[]>([]);
  const [districts, setDistricts] = useState<Location[]>([]);
  const [areas, setAreas] = useState<Location[]>([]);
  const [division, setDivision] = useState("");
  const [district, setDistrict] = useState("");
  const [confirming, setConfirming] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    getLocations("divisions").then(setDivisions).catch(() => setState("Unable to load locations."));
  }, []);

  useEffect(() => {
    if (!division) return;
    getLocations(`districts?division=${division}`)
      .then(setDistricts)
      .catch(() => setState("Unable to load districts."));
  }, [division]);

  useEffect(() => {
    if (!district) return;
    getLocations(`areas?district=${district}`)
      .then(setAreas)
      .catch(() => setState("Unable to load areas."));
  }, [district]);

  function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setConfirming(true);
  }

  async function confirmSubmit() {
    const form = formRef.current;
    if (!form) return;
    setState("Submitting…");
    const data = Object.fromEntries(new FormData(form));
    try {
      const response = await fetch(`${API_URL}/landowner-proposals/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...data,
          number_of_owners: Number(data.number_of_owners) || 1,
        }),
      });
      const body = await response.json().catch(() => ({}));
      if (!response.ok)
        throw new Error(body.message || "Please check the form and try again.");
      setState(
        "Thank you. Our land acquisition team will contact you shortly.",
      );
      setConfirming(false);
      form.reset();
      setDivision("");
      setDistrict("");
      setDistricts([]);
      setAreas([]);
    } catch (error) {
      setConfirming(false);
      setState(
        error instanceof Error
          ? error.message
          : "Unable to submit the proposal.",
      );
    }
  }
  return (
    <>
    <form ref={formRef} className="landowner-form" onSubmit={submit}>
      <h3>Land Information</h3>
      <div className="landowner-fields">
        <select
          name="division"
          required
          value={division}
          onChange={(event) => {
            setDivision(event.target.value);
            setDistrict("");
            setDistricts([]);
            setAreas([]);
          }}
        >
          <option value="" disabled>Select division*</option>
          {divisions.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
        </select>
        <select
          name="district"
          required
          value={district}
          disabled={!division}
          onChange={(event) => {
            setDistrict(event.target.value);
            setAreas([]);
          }}
        >
          <option value="" disabled>Select district*</option>
          {districts.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
        </select>
        <select name="area" required defaultValue="" disabled={!district}>
          <option value="" disabled>Select area*</option>
          {areas.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
        </select>
        <input name="locality" placeholder="Locality" />
        <input name="land_address" required placeholder="Address*" />
        <input
          name="land_size"
          type="number"
          min="0.01"
          step="0.01"
          required
          placeholder="Size of the land in Kathas*"
        />
        <input
          name="road_width"
          type="number"
          min="0"
          step="0.01"
          placeholder="Width of road in front (feet)"
        />
        <select name="ownership_type" required defaultValue="">
          <option value="" disabled>
            Select ownership category*
          </option>
          <option>Single ownership</option>
          <option>Joint ownership</option>
          <option>Inherited property</option>
          <option>Company owned</option>
        </select>
        <input
          name="number_of_owners"
          type="number"
          min="1"
          defaultValue="1"
          placeholder="Number of owners"
        />
        <input
          name="google_maps_url"
          type="url"
          placeholder="Google Maps link (optional)"
        />
        <textarea
          name="message"
          rows={1}
          placeholder="Attractive features / additional notes"
        />
      </div>
      <h3>Landowner Information</h3>
      <div className="landowner-fields owner-fields">
        <input
          name="owner_name"
          required
          placeholder="Name of the landowner*"
        />
        <input name="email" type="email" placeholder="Email ID" />
        <input
          name="phone"
          required
          placeholder="Contact number* (e.g. +8801...)"
        />
      </div>
      <input
        className="form-honeypot"
        name="website"
        tabIndex={-1}
        autoComplete="off"
      />
      <Captcha />
      <button type="submit">Submit</button>
      {state && state !== "Thank you. Our land acquisition team will contact you shortly." && (
        <p className="landowner-form-status" role="status">
          {state}
        </p>
      )}
    </form>
    {confirming && (
      <SubmissionConfirmModal
        title="Submit land proposal?"
        message="Are you sure you want to send your land information to our acquisition team?"
        busy={state === "Submitting…"}
        onCancel={() => setConfirming(false)}
        onConfirm={confirmSubmit}
      />
    )}
    {state === "Thank you. Our land acquisition team will contact you shortly." && (
      <SubmissionSuccessModal
        title="Land proposal submitted."
        message="Thank you. Our land acquisition team will contact you shortly."
        onClose={() => setState("")}
      />
    )}
    </>
  );
}
