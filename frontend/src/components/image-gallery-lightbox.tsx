"use client";

import {useCallback,useEffect,useState} from "react";

export type GalleryImage={id:string;src:string;title:string};

export function ImageGalleryLightbox({images}:{images:GalleryImage[]}){
  const [active,setActive]=useState<number|null>(null);
  const close=useCallback(()=>setActive(null),[]);
  const move=useCallback((step:number)=>setActive(current=>current===null?null:(current+step+images.length)%images.length),[images.length]);

  useEffect(()=>{
    if(active===null)return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const keyboard=(event:KeyboardEvent)=>{if(event.key==="Escape")close();if(event.key==="ArrowLeft")move(-1);if(event.key==="ArrowRight")move(1)};
    window.addEventListener("keydown",keyboard);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",keyboard)};
  },[active,close,move]);

  return <><div className="gallery-albums">{images.map((image,index)=><button type="button" key={image.id} onClick={()=>setActive(index)} aria-label={`Open ${image.title}`}><img src={image.src} alt={image.title}/><div><small>{String(index+1).padStart(2,"0")}</small><h3>{image.title}</h3><span>View Album →</span></div></button>)}</div>{active!==null&&<div className="gallery-lightbox" role="dialog" aria-modal="true" aria-label={`${images[active].title} image viewer`} onClick={close}><div className="gallery-lightbox-bar"><span>{active+1} / {images.length}</span><button type="button" onClick={close} aria-label="Close gallery">×</button></div><button type="button" className="gallery-lightbox-prev" onClick={event=>{event.stopPropagation();move(-1)}} aria-label="Previous image">‹</button><figure onClick={event=>event.stopPropagation()}><img src={images[active].src} alt={images[active].title}/><figcaption>{images[active].title}</figcaption></figure><button type="button" className="gallery-lightbox-next" onClick={event=>{event.stopPropagation();move(1)}} aria-label="Next image">›</button></div>}</>;
}
