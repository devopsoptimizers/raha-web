"use client";
import Script from "next/script";
import {useEffect,useRef,useState} from "react";

declare global {
  interface Window { turnstile?: {render:(element:HTMLElement,options:Record<string,unknown>)=>string;reset:(widgetId?:string)=>void;remove:(widgetId:string)=>void} }
}

const siteKey=process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY;

export function Captcha({className=""}:{className?:string}){
  const container=useRef<HTMLDivElement>(null),widgetId=useRef<string|undefined>(undefined);
  const[token,setToken]=useState("");
  function render(){
    if(!siteKey||!container.current||!window.turnstile||widgetId.current)return;
    widgetId.current=window.turnstile.render(container.current,{sitekey:siteKey,theme:"light",size:"flexible",callback:(value:string)=>setToken(value),"expired-callback":()=>setToken(""),"error-callback":()=>setToken("")});
  }
  useEffect(()=>{
    const form=container.current?.closest("form");
    const reset=()=>{setToken("");if(widgetId.current)window.turnstile?.reset(widgetId.current)};
    form?.addEventListener("reset",reset);
    return()=>{form?.removeEventListener("reset",reset);if(widgetId.current)window.turnstile?.remove(widgetId.current)};
  },[]);
  if(!siteKey)return null;
  return <div className={`captcha-field ${className}`}><Script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" strategy="afterInteractive" onLoad={render}/><div ref={container}/><input type="hidden" name="captcha_token" value={token} readOnly required/><p>This site is protected by Cloudflare Turnstile.</p></div>;
}
