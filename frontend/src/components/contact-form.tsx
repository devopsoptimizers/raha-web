"use client";
import {FormEvent,useRef,useState} from "react";
import {api} from "@/lib/api";
import {SubmissionConfirmModal} from "@/components/submission-confirm-modal";
import {SubmissionSuccessModal} from "@/components/submission-success-modal";
import {Captcha} from "@/components/captcha";

type Labels={name?:string;phone?:string;email?:string;userType?:string;client?:string;landowner?:string;message?:string;submit?:string};
export function ContactForm({companyName="Raha Holdings",labels={}}:{companyName?:string;labels?:Labels}){
  const[state,setState]=useState<"idle"|"busy"|"sent"|"error">("idle");
  const[confirming,setConfirming]=useState(false);
  const formRef=useRef<HTMLFormElement>(null);
  function submit(e:FormEvent<HTMLFormElement>){e.preventDefault();setConfirming(true)}
  async function confirmSubmit(){const form=formRef.current;if(!form)return;setState("busy");const data=Object.fromEntries(new FormData(form));try{await api("/contact-messages/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({full_name:data.full_name,phone:data.phone,email:data.email,user_type:data.user_type,subject:"Website contact",message:data.message,website:data.website,captcha_token:data.captcha_token})});form.reset();setConfirming(false);setState("sent")}catch{setConfirming(false);setState("error")}}
  return <><form ref={formRef} onSubmit={submit} className="contact-enquiry-form">
    <Field label={labels.name||"Full Name"} name="full_name" required placeholder={labels.name||"Full Name"}/>
    <Field label={labels.phone||"Contact Number"} name="phone" required placeholder="017XXXXXXXX" className="contact-half"/>
    <Field label={labels.email||"Email"} name="email" type="email" placeholder={labels.email||"Email"} className="contact-half"/>
    <fieldset><legend>{labels.userType||"User Type"} <b>*</b></legend><div><label><input type="radio" name="user_type" value="CLIENT" defaultChecked/><span>{labels.client||"Client"}</span></label><label><input type="radio" name="user_type" value="LANDOWNER"/><span>{labels.landowner||"Landowner"}</span></label></div></fieldset>
    <label><span>{labels.message||"Message"} <b>*</b></span><textarea name="message" rows={5} required placeholder={labels.message||"Text"}/></label>
    <Captcha/>
    <input className="form-honeypot" name="website" tabIndex={-1} autoComplete="off"/>
    {state==="error"&&<p className="contact-form-notice error">We couldn&apos;t send your message. Please check your details and try again.</p>}
    <button disabled={state==="busy"}>{state==="busy"?"Submitting…":labels.submit||"Submit"}</button>
  </form>{confirming&&<SubmissionConfirmModal title="Send your message?" message={`Are you sure you want to send this message to ${companyName}?`} busy={state==="busy"} onCancel={()=>setConfirming(false)} onConfirm={confirmSubmit}/>} {state==="sent"&&<SubmissionSuccessModal title="Thank you for contacting us." message={`A ${companyName} advisor will be in touch shortly.`} onClose={()=>setState("idle")}/>}</>
}
function Field({label,name,type="text",required=false,placeholder,className=""}:{label:string;name:string;type?:string;required?:boolean;placeholder?:string;className?:string}){return <label className={className}><span>{label} {required&&<b>*</b>}</span><input name={name} type={type} required={required} placeholder={placeholder} pattern={name==="phone"?"(?:\\+?88)?01[3-9]\\d{8}":undefined}/></label>}
