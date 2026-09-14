"use client";

import {FormEvent,useEffect,useRef,useState} from "react";
import {api} from "@/lib/api";
import {Captcha} from "@/components/captcha";

type Step="closed"|"form"|"thanks"|"viewer";

export function BrochureDownload({projectId,projectName,brochureUrl}:{projectId:string;projectName:string;brochureUrl?:string|null}){
  const[step,setStep]=useState<Step>("closed");
  const[busy,setBusy]=useState(false);
  const[error,setError]=useState("");
  const formRef=useRef<HTMLFormElement>(null);
  const viewerUrl=brochureUrl?`/api/brochure?src=${encodeURIComponent(brochureUrl)}`:"";
  const downloadUrl=brochureUrl?`${viewerUrl}&download=1`:"";

  useEffect(()=>{
    if(step==="closed")return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const onKeyDown=(event:KeyboardEvent)=>{if(event.key==="Escape")setStep("closed")};
    window.addEventListener("keydown",onKeyDown);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",onKeyDown)};
  },[step]);

  async function submit(event:FormEvent<HTMLFormElement>){
    event.preventDefault();
    setBusy(true);setError("");
    const data=Object.fromEntries(new FormData(event.currentTarget));
    try{
      await api("/inquiries/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
        full_name:data.full_name,email:data.email,phone:data.phone,project:projectId,
        message:`Brochure requested for ${projectName}`,
        lead_source:"Website - Brochure Download",preferred_contact_method:"PHONE",
        website:data.website,captcha_token:data.captcha_token,
      })});
      formRef.current?.reset();setStep("thanks");
    }catch(cause){setError(cause instanceof Error?cause.message:"We could not submit your request. Please try again.")}
    finally{setBusy(false)}
  }

  return <>
    <button className="bio-brochure bio-brochure-download" type="button" onClick={()=>setStep("form")}>Download Brochure <span aria-hidden="true">↓</span></button>

    {step==="form"&&<div className="brochure-modal-backdrop" role="presentation" onMouseDown={(event)=>{if(event.target===event.currentTarget)setStep("closed")}}>
      <section className="brochure-form-modal" role="dialog" aria-modal="true" aria-labelledby="brochure-form-title">
        <button className="brochure-modal-close" type="button" aria-label="Close brochure form" onClick={()=>setStep("closed")}>×</button>
        <p>Project Brochure</p>
        <h2 id="brochure-form-title">Fill up the information</h2>
        <span>{brochureUrl?`Enter your details to view and download the ${projectName} brochure.`:`Enter your details and our property consultant will send you the ${projectName} brochure.`}</span>
        <form ref={formRef} onSubmit={submit}>
          <label><span>Full Name <b>*</b></span><input name="full_name" autoComplete="name" required/></label>
          <label><span>Email Address <b>*</b></span><input name="email" type="email" autoComplete="email" required/></label>
          <label><span>Phone Number <b>*</b></span><input name="phone" type="tel" autoComplete="tel" placeholder="017XXXXXXXX" pattern="(?:\+?88)?01[3-9]\d{8}" required/></label>
          <Captcha/>
          <input className="form-honeypot" name="website" tabIndex={-1} autoComplete="off"/>
          {error&&<div className="brochure-form-error" role="alert">{error}</div>}
          <button className="brochure-submit" disabled={busy}>{busy?"Submitting…":"View Brochure"}<span aria-hidden="true">→</span></button>
        </form>
      </section>
    </div>}

    {step==="thanks"&&<div className="brochure-modal-backdrop brochure-thanks-backdrop">
      <section className="brochure-thanks" role="dialog" aria-modal="true" aria-labelledby="brochure-thanks-title">
        <button className="brochure-modal-close" type="button" aria-label="Close confirmation" onClick={()=>setStep("closed")}>×</button>
        <div className="brochure-thanks-mark" aria-hidden="true">✓</div>
        <p>Dear Sir/Madam,</p>
        <h2 id="brochure-thanks-title">Thank you for your interest.</h2>
        <span>{brochureUrl?"Our property consultant will contact you shortly. You can view or download the project brochure now.":"Our property consultant will contact you shortly and provide the project brochure."}</span>
        {brochureUrl?<button className="brochure-submit" type="button" onClick={()=>setStep("viewer")}>Open Brochure <span aria-hidden="true">→</span></button>:<button className="brochure-submit" type="button" onClick={()=>setStep("closed")}>Close <span aria-hidden="true">×</span></button>}
      </section>
    </div>}

    {step==="viewer"&&brochureUrl&&<section className="newsletter-pdf-modal brochure-pdf-viewer" role="dialog" aria-modal="true" aria-label={`${projectName} brochure`}>
      <header><span>{projectName} — Brochure</span><div><a href={viewerUrl} target="_blank" rel="noreferrer">Open New Tab</a><a href={downloadUrl} target="_blank" rel="noreferrer">Download PDF</a><button type="button" aria-label="Close brochure viewer" onClick={()=>setStep("closed")}>×</button></div></header>
      <iframe src={`${viewerUrl}#toolbar=1&navpanes=0&view=FitH`} title={`${projectName} brochure PDF`}/>
    </section>}
  </>;
}
