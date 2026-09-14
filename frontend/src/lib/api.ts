export const API_URL =
  typeof window === "undefined"
    ? process.env.INTERNAL_API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"
    : process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
export type Project = { id:string; name:string; slug:string; code:string; short_description:string; status:string; property_type:string; property_type_name?:string; area?:string; area_name:string; min_apartment_size:number|null; max_apartment_size:number|null; min_price:string|null; max_price:string|null; currency:string; expected_handover_date:string|null; featured_image:string; is_featured:boolean };
export type User = { id:string; email:string; username:string; first_name:string; last_name:string; phone:string; role:string };
export async function api<T>(path:string, options?:RequestInit):Promise<T>{const response=await fetch(`${API_URL}${path}`,options);const body=await response.json().catch(()=>({}));if(!response.ok)throw new Error(body.message||body.detail||"Something went wrong");return (body.data??body) as T}
export function money(value:string|null,currency="BDT"){if(!value)return "Price on request";const amount=Number(value);if(currency==="BDT"&&amount>=10_000_000)return `BDT ${(amount/10_000_000).toFixed(1)} Cr`;if(currency==="BDT"&&amount>=100_000)return `BDT ${(amount/100_000).toFixed(1)} Lac`;return new Intl.NumberFormat("en",{style:"currency",currency,maximumFractionDigits:0}).format(amount)}
