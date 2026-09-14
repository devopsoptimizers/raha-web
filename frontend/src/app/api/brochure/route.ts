import {NextRequest,NextResponse} from "next/server";
import {API_URL} from "@/lib/api";

export async function GET(request:NextRequest){
  const source=request.nextUrl.searchParams.get("src");
  if(!source)return NextResponse.json({message:"Missing brochure URL."},{status:400});

  let brochureUrl:URL,apiUrl:URL;
  try{brochureUrl=new URL(source);apiUrl=new URL(API_URL)}catch{return NextResponse.json({message:"Invalid brochure URL."},{status:400})}
  if(!["http:","https:"].includes(brochureUrl.protocol)||!brochureUrl.pathname.startsWith("/media/projects/brochures/"))return NextResponse.json({message:"Brochure URL is not allowed."},{status:403});

  const internalUrl=new URL(`${brochureUrl.pathname}${brochureUrl.search}`,apiUrl.origin);
  const response=await fetch(internalUrl,{cache:"no-store"});
  if(!response.ok||!response.body)return NextResponse.json({message:"Brochure could not be loaded."},{status:response.status||502});

  const filename=decodeURIComponent(brochureUrl.pathname.split("/").pop()||"project-brochure.pdf").replace(/["\r\n]/g,"");
  const disposition=request.nextUrl.searchParams.get("download")==="1"?"attachment":"inline";
  return new NextResponse(response.body,{headers:{
    "Content-Type":"application/pdf",
    "Content-Disposition":`${disposition}; filename="${filename}"`,
    "Cache-Control":"private, no-store",
  }});
}
