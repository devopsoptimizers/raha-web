import {API_URL} from "./api";

export type PageHeader={title:string;body:string;image?:string;payload?:Record<string,unknown>};

export async function loadPageHeader(key:string):Promise<PageHeader|undefined>{
  try{
    const response=await fetch(`${API_URL}/home/`,{cache:"no-store"});
    if(!response.ok)return;
    const body=await response.json(),data=body.data||body;
    return(data.content||[]).find((item:{block_type:string;key:string})=>item.block_type==="HEADER"&&item.key===key);
  }catch{return;}
}
