import {notFound} from "next/navigation";
import {AnimatedHeading} from "@/components/animated-heading";
import {Header} from "@/components/header";
import {Footer} from "@/components/footer";
import {API_URL} from "@/lib/api";

type BlogPost={title:string;excerpt:string;content?:string;featured_image?:string;published_at?:string};
const date=(value:string)=>new Intl.DateTimeFormat("en-GB",{day:"2-digit",month:"long",year:"numeric"}).format(new Date(value));

export default async function Post({params}:{params:Promise<{slug:string}>}){
  const{slug}=await params;
  let post:BlogPost|undefined;
  try{
    const response=await fetch(`${API_URL}/blogs/slug/${slug}/`,{cache:"no-store"});
    if(response.ok){const body=await response.json();post=body.data||body}
  }catch{}
  if(!post)return notFound();
  return <><Header/><article><div className={`blog-post-hero ${post.featured_image?"has-image":""}`} style={post.featured_image?{backgroundImage:`url(${post.featured_image})`}:undefined}><div className="blog-post-hero-shade"/><div className="shell max-w-4xl"><p className="eyebrow text-gold-light">Blog</p><AnimatedHeading as="h1" className="mt-5 font-serif text-6xl leading-tight">{post.title}</AnimatedHeading>{post.published_at&&<time className="blog-post-date" dateTime={post.published_at}>{date(post.published_at)}</time>}</div></div><div className="shell max-w-3xl py-20"><p className="whitespace-pre-line text-lg leading-9 text-stone">{post.content||post.excerpt}</p></div></article><Footer/></>;
}
