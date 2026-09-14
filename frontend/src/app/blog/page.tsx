import Link from "next/link";
import {AnimatedHeading} from "@/components/animated-heading";import {Header} from "@/components/header";
import {Footer} from "@/components/footer";
import {API_URL} from "@/lib/api";

type BlogPost={id:string;title:string;slug:string;excerpt:string;featured_image:string;published_at:string};
type ContentBlock={block_type:string;key:string;title:string;body:string;image?:string;is_active:boolean;is_published:boolean};

export const metadata={title:"Blog"};
const date=(value:string)=>new Intl.DateTimeFormat("en-GB",{day:"2-digit",month:"long",year:"numeric"}).format(new Date(value));

export default async function Blog(){
  let posts:BlogPost[]=[];
  let header:ContentBlock|undefined;
  try{
    const[postsResponse,homeResponse]=await Promise.all([
      fetch(`${API_URL}/blogs/?page_size=100`,{cache:"no-store"}),
      fetch(`${API_URL}/home/`,{cache:"no-store"}),
    ]);
    if(postsResponse.ok){const body=await postsResponse.json();posts=body.data||body.results||[]}
    if(homeResponse.ok){const body=await homeResponse.json(),data=body.data||body;header=(data.content||[]).find((item:ContentBlock)=>item.block_type==="HEADER"&&item.key==="blog-header")}
  }catch{}
  return <><Header/><main className="blog-page"><section className="blog-banner"><div className="blog-banner-art" style={header?.image?{backgroundImage:`url(${header.image})`}:undefined}/><div className="shell"><p>{header?.body||"Ideas for a better way of living"}</p><AnimatedHeading as="h1">{header?.title||"Blog"}</AnimatedHeading></div></section><section className="blog-list"><div className="shell">{posts.length?<div className="blog-grid">{posts.map(post=><article key={post.id} className="blog-card"><Link href={`/blog/${post.slug}`} className="blog-card-image"><img src={post.featured_image} alt={post.title}/></Link><time dateTime={post.published_at}>{date(post.published_at)}</time><h2><Link href={`/blog/${post.slug}`}>{post.title}</Link></h2><p>{post.excerpt}</p><Link className="blog-explore" href={`/blog/${post.slug}`}>Explore</Link></article>)}</div>:<div className="empty"><h3>No published posts yet.</h3><p>Please check back soon.</p></div>}</div></section></main><Footer/></>;
}
