"use client";
import {FormEvent,useRef,useState} from "react";
import {api} from "@/lib/api";
import {SubmissionConfirmModal} from "@/components/submission-confirm-modal";
import {SubmissionSuccessModal} from "@/components/submission-success-modal";
import {Captcha} from "@/components/captcha";

export function ProjectInquiryForm({projectId,projectName,image,title,description}:{projectId:string;projectName:string;image:string;title?:string;description?:string}){
  const [state,setState]=useState<"idle"|"busy"|"sent"|"error">("idle");
  const [confirming,setConfirming]=useState(false);
  const formRef=useRef<HTMLFormElement>(null);
  async function submit(event:FormEvent<HTMLFormElement>){
    event.preventDefault();setConfirming(true);
  }
  async function confirmSubmit(){
    const form=formRef.current;if(!form)return;setState("busy");
    const data=Object.fromEntries(new FormData(form)),userType=String(data.user_type||"Client");
    try{
      await api("/inquiries/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({full_name:data.full_name,phone:data.phone,email:data.email,project:projectId,message:data.message,lead_source:`Website - ${userType}`,preferred_contact_method:"PHONE",website:data.website,captcha_token:data.captcha_token})});
      form.reset();setConfirming(false);setState("sent");
    }catch{setConfirming(false);setState("error");}
  }
  return <><section className="property-inquiry"><div className="shell property-inquiry-card"><div className="property-inquiry-intro"><h2>{title||"Ask About the property"}</h2><p>{description||`We will schedule a call to discuss your requirements and help you explore whether ${projectName} is the right home for you.`}</p><div><img src={image} alt={`${projectName} property consultation`}/><span><b>Talk to a property advisor</b><small>Personal guidance from enquiry to handover.</small></span></div></div><form ref={formRef} onSubmit={submit}><label className="inquiry-full"><span>Full Name <b>*</b></span><input name="full_name" required placeholder="Full Name"/></label><label><span>Contact Number <b>*</b></span><input name="phone" type="tel" required placeholder="017XXXXXXXX" pattern="(?:\+?88)?01[3-9]\d{8}"/></label><label><span>Email</span><input name="email" type="email" placeholder="Email"/></label><fieldset className="inquiry-full"><legend>User Type <b>*</b></legend><label><input type="radio" name="user_type" value="Client" defaultChecked/><span>Client</span></label><label><input type="radio" name="user_type" value="Landowner"/><span>Landowner</span></label></fieldset><label className="inquiry-full"><span>Message <b>*</b></span><textarea name="message" required rows={5} placeholder="Tell us what you would like to know"/></label><Captcha className="inquiry-full"/><input className="form-honeypot" name="website" tabIndex={-1} autoComplete="off"/><button className="inquiry-full" disabled={state==="busy"}>{state==="busy"?"Submitting…":"Submit"}</button>{state==="error"&&<p className="inquiry-notice inquiry-error inquiry-full" role="alert">We couldn&apos;t submit your enquiry. Please check the details and try again.</p>}</form></div></section>{confirming&&<SubmissionConfirmModal title="Submit property enquiry?" message={`Are you sure you want to send your enquiry about ${projectName}?`} busy={state==="busy"} onCancel={()=>setConfirming(false)} onConfirm={confirmSubmit}/>} {state==="sent"&&<SubmissionSuccessModal title="Property enquiry submitted." message="Thank you. A property advisor will contact you shortly." onClose={()=>setState("idle")}/>}</>;
}
