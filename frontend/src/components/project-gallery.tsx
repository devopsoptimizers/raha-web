"use client";
import {useEffect,useState} from "react";

export function ProjectGallery({images,name}:{images:string[];name:string}){
  const[index,setIndex]=useState(0),[open,setOpen]=useState(false);
  const select=(next:number)=>setIndex((next+images.length)%images.length);

  useEffect(()=>{
    if(!open)return;
    const previousOverflow=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const onKeyDown=(event:KeyboardEvent)=>{
      if(event.key==="Escape")setOpen(false);
      if(event.key==="ArrowLeft")setIndex(current=>(current-1+images.length)%images.length);
      if(event.key==="ArrowRight")setIndex(current=>(current+1)%images.length);
    };
    window.addEventListener("keydown",onKeyDown);
    return()=>{document.body.style.overflow=previousOverflow;window.removeEventListener("keydown",onKeyDown)};
  },[open,images.length]);

  if(!images.length)return <div className="project-gallery project-gallery-empty"/>;
  return <div className="project-gallery">
    <div className="project-gallery-main">
      {images.map((image,i)=><button type="button" key={`${image}-${i}`} className={`project-gallery-open ${i===index?"active":""}`} onClick={()=>{setIndex(i);setOpen(true)}} aria-label={`Open ${name} image ${i+1} in full screen`}><img src={image} alt={`${name} view ${i+1}`}/><span>View gallery</span></button>)}
      {images.length>1&&<><button type="button" className="gallery-arrow gallery-prev" onClick={()=>select(index-1)} aria-label="Previous project image">‹</button><button type="button" className="gallery-arrow gallery-next" onClick={()=>select(index+1)} aria-label="Next project image">›</button><span className="gallery-count">{String(index+1).padStart(2,"0")} / {String(images.length).padStart(2,"0")}</span></>}
    </div>
    {images.length>1&&<div className="project-gallery-thumbs">{images.map((image,i)=><button type="button" className={i===index?"active":""} onClick={()=>select(i)} key={`${image}-thumb-${i}`} aria-label={`Show image ${i+1}`}><img src={image} alt=""/></button>)}</div>}
    {open&&<div className="project-gallery-lightbox" role="dialog" aria-modal="true" aria-label={`${name} image gallery`} onClick={()=>setOpen(false)}>
      <div className="project-gallery-lightbox-bar"><span>{name}</span><b>{index+1} / {images.length}</b><button type="button" onClick={()=>setOpen(false)} aria-label="Close gallery">×</button></div>
      {images.length>1&&<button type="button" className="project-gallery-lightbox-prev" onClick={event=>{event.stopPropagation();select(index-1)}} aria-label="Previous image">‹</button>}
      <figure onClick={event=>event.stopPropagation()}><img src={images[index]} alt={`${name} view ${index+1}`}/></figure>
      {images.length>1&&<button type="button" className="project-gallery-lightbox-next" onClick={event=>{event.stopPropagation();select(index+1)}} aria-label="Next image">›</button>}
      {images.length>1&&<div className="project-gallery-lightbox-thumbs" onClick={event=>event.stopPropagation()}>{images.map((image,i)=><button type="button" className={i===index?"active":""} onClick={()=>select(i)} key={`${image}-lightbox-${i}`} aria-label={`Show image ${i+1}`}><img src={image} alt=""/></button>)}</div>}
    </div>}
  </div>;
}
