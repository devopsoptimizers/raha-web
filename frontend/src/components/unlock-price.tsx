"use client";

import {FormEvent,useEffect,useRef,useState} from "react";
import {Captcha} from "@/components/captcha";
import {useSiteSettings} from "@/components/site-settings";
import {api} from "@/lib/api";

export function UnlockPrice({projectId,projectName}:{projectId:string;projectName:string}){
  const site=useSiteSettings();
  const[step,setStep]=useState<"closed"|"form"|"thanks">("closed");
  const[busy,setBusy]=useState(false);
  const[error,setError]=useState("");
  const formRef=useRef<HTMLFormElement>(null);
  const number=(site.hotline||"+8801700000000").replace(/\D/g,"");
  const message=`Hello Raha, I submitted a price request for ${projectName}. Please share the current price and availability.`;
  const configured=site.social_links?.whatsapp||"";
  let whatsappUrl=`https://wa.me/${number}?text=${encodeURIComponent(message)}`;
  if(configured){
    try{const url=new URL(configured);url.searchParams.set("text",message);whatsappUrl=url.toString()}catch{}
  }

  useEffect(()=>{
    if(step==="closed")return;
    const previous=document.body.style.overflow;document.body.style.overflow="hidden";
    const close=(event:KeyboardEvent)=>{if(event.key==="Escape")setStep("closed")};
    window.addEventListener("keydown",close);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",close)};
  },[step]);

  async function submit(event:FormEvent<HTMLFormElement>){
    event.preventDefault();setBusy(true);setError("");
    const data=Object.fromEntries(new FormData(event.currentTarget));
    try{
      await api("/inquiries/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
        full_name:data.full_name,email:data.email,phone:data.phone,project:projectId,
        message:`Price and availability requested for ${projectName}`,
        lead_source:"Website - Unlock Price",preferred_contact_method:"WHATSAPP",
        website:data.website,captcha_token:data.captcha_token,
      })});
      formRef.current?.reset();setStep("thanks");
    }catch(cause){setError(cause instanceof Error?cause.message:"We could not submit your request. Please try again.")}
    finally{setBusy(false)}
  }

  return <>
    <button className="bio-brochure bio-price-unlock" type="button" onClick={()=>setStep("form")}>Unlock Price <span aria-hidden="true">→</span></button>
    {step==="form"&&<div className="brochure-modal-backdrop" role="presentation" onMouseDown={(event)=>{if(event.target===event.currentTarget)setStep("closed")}}>
      <section className="brochure-form-modal" role="dialog" aria-modal="true" aria-labelledby="price-form-title">
        <button className="brochure-modal-close" type="button" aria-label="Close price form" onClick={()=>setStep("closed")}>×</button>
        <p>Private Price Request</p><h2 id="price-form-title">Unlock the price</h2>
        <span>Share your details to receive the current price and availability for {projectName}.</span>
        <form ref={formRef} onSubmit={submit}>
          <label><span>Full Name <b>*</b></span><input name="full_name" autoComplete="name" required/></label>
          <label><span>Email Address <b>*</b></span><input name="email" type="email" autoComplete="email" required/></label>
          <label><span>Phone Number <b>*</b></span><input name="phone" type="tel" autoComplete="tel" placeholder="017XXXXXXXX" pattern="(?:\+?88)?01[3-9]\d{8}" required/></label>
          <Captcha/><input className="form-honeypot" name="website" tabIndex={-1} autoComplete="off"/>
          {error&&<div className="brochure-form-error" role="alert">{error}</div>}
          <button className="brochure-submit" disabled={busy}>{busy?"Submitting…":"Unlock Price"}<span aria-hidden="true">→</span></button>
        </form>
      </section>
    </div>}
    {step==="thanks"&&<div className="brochure-modal-backdrop brochure-thanks-backdrop">
      <section className="brochure-thanks" role="dialog" aria-modal="true" aria-labelledby="price-thanks-title">
        <button className="brochure-modal-close" type="button" aria-label="Close confirmation" onClick={()=>setStep("closed")}>×</button>
        <div className="brochure-thanks-mark" aria-hidden="true">✓</div><p>Dear Sir/Madam,</p>
        <h2 id="price-thanks-title">Thank you for your interest.</h2>
        <span>Our property consultant will contact you shortly. You can also continue this price request on WhatsApp.</span>
        <a className="brochure-submit price-whatsapp-action" href={whatsappUrl} target="_blank" rel="noreferrer" onClick={()=>setStep("closed")}>Continue on WhatsApp <span aria-hidden="true">↗</span></a>
      </section>
    </div>}
  </>;
}
