"use client";
import {useEffect,useRef,useState} from "react";

export type Campaign={id:string;title:string;body?:string;image?:string;cta_label?:string;cta_url?:string;updated_at:string};

const dismissalKey=(campaign:Campaign)=>`campaign-dismissed:${campaign.id}:${campaign.updated_at}`;

export function CampaignAnnouncement({campaigns}:{campaigns:Campaign[]}){
  const sectionRef=useRef<HTMLElement>(null);
  const campaign=campaigns[0];
  const[visible,setVisible]=useState(false),[dismissed,setDismissed]=useState(false);
  useEffect(()=>{
    if(!campaign)return;
    setDismissed(sessionStorage.getItem(dismissalKey(campaign))==="1");
    const section=sectionRef.current;if(!section)return;
    const observer=new IntersectionObserver(([entry])=>{if(entry.isIntersecting){window.setTimeout(()=>setVisible(true),180);observer.disconnect()}},{threshold:.25});
    observer.observe(section);return()=>observer.disconnect();
  },[campaign]);
  useEffect(()=>{const escape=(event:KeyboardEvent)=>{if(event.key==="Escape")close()};window.addEventListener("keydown",escape);return()=>window.removeEventListener("keydown",escape)},[campaign]);
  if(!campaign||dismissed)return null;
  function close(){sessionStorage.setItem(dismissalKey(campaign!),"1");setVisible(false);window.setTimeout(()=>setDismissed(true),350)}
  return <section ref={sectionRef} className={`campaign-section ${visible?"campaign-visible":""}`} aria-label="Campaign announcement" onClick={close}><article className={`campaign-card ${campaign.image?"":"campaign-without-image"} ${campaign.body?"":"campaign-without-body"}`} role="dialog" aria-modal="true" aria-labelledby={`campaign-title-${campaign.id}`} onClick={event=>event.stopPropagation()}>{campaign.image&&<div className="campaign-image">{campaign.cta_url?<a href={campaign.cta_url} aria-label={campaign.cta_label||campaign.title}><img src={campaign.image} alt=""/></a>:<img src={campaign.image} alt=""/>}</div>}<div className="campaign-content"><h2 id={`campaign-title-${campaign.id}`}>{campaign.title}</h2>{campaign.body&&<p>{campaign.body}</p>}{campaign.cta_label&&campaign.cta_url&&<a href={campaign.cta_url}>{campaign.cta_label}<b aria-hidden="true">→</b></a>}</div><button type="button" className="campaign-close" onClick={close} aria-label="Close campaign announcement"><span aria-hidden="true">×</span></button></article></section>;
}
