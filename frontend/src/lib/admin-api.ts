import {API_URL} from "./api";

let refreshRequest:Promise<string|null>|null=null;

export function clearAuth(){
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}

async function refreshAccessToken(){
  if(refreshRequest)return refreshRequest;
  refreshRequest=(async()=>{
    const refresh=localStorage.getItem("refresh_token");
    if(!refresh)return null;
    try{
      const response=await fetch(`${API_URL}/auth/token/refresh/`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({refresh})});
      if(!response.ok)return null;
      const body=await response.json(),tokens=body.data||body;
      if(!tokens.access)return null;
      localStorage.setItem("access_token",tokens.access);
      if(tokens.refresh)localStorage.setItem("refresh_token",tokens.refresh);
      return tokens.access as string;
    }catch{return null}
  })();
  try{return await refreshRequest}finally{refreshRequest=null}
}

export async function adminFetch(path:string,options:RequestInit={}){
  const run=(access:string|null)=>fetch(`${API_URL}${path}`,{...options,headers:{...(options.headers||{}),...(access?{Authorization:`Bearer ${access}`}:{})}});
  let response=await run(localStorage.getItem("access_token"));
  if(response.status!==401)return response;
  const access=await refreshAccessToken();
  if(access)response=await run(access);
  if(response.status===401){clearAuth();window.dispatchEvent(new Event("auth:expired"))}
  return response;
}

export async function logoutSession(){
  const refresh=localStorage.getItem("refresh_token");
  try{if(refresh)await adminFetch("/auth/logout/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({refresh})})}catch{}finally{clearAuth()}
}

export async function adminData<T>(path:string){const response=await adminFetch(path);if(!response.ok)throw new Error("Request failed");const body=await response.json();return {items:(body.data||body.results||[])as T[],count:body.count??body.meta?.total_records??(body.data||[]).length}}
