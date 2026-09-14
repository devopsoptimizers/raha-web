"use client";

import {useRouter, useSearchParams} from "next/navigation";
import type {ChangeEvent, FormEvent} from "react";

export function ProjectFilters({locations,propertyTypes}:{locations:string[];propertyTypes:string[]}){
  const router=useRouter();
  const params=useSearchParams();

  function updateFilter(event:ChangeEvent<HTMLSelectElement>){
    const next=new URLSearchParams(params.toString());
    if(event.target.value)next.set(event.target.name,event.target.value);
    else next.delete(event.target.name);
    router.push(`/properties${next.size?`?${next.toString()}`:""}`);
  }

  function search(event:FormEvent<HTMLFormElement>){
    event.preventDefault();
    const data=new FormData(event.currentTarget);
    const next=new URLSearchParams(params.toString());
    const value=String(data.get("search")||"").trim();
    if(value)next.set("search",value);else next.delete("search");
    router.push(`/properties${next.size?`?${next.toString()}`:""}`);
  }

  return <form className="projects-filter" onSubmit={search}>
    <select name="status" value={params.get("status")||""} onChange={updateFilter} aria-label="Project status"><option value="">All</option><option value="ONGOING">Ongoing</option><option value="UPCOMING">Upcoming</option><option value="HANDED_OVER">Handed Over</option><option value="READY">Ready</option></select>
    <select name="property_type" value={params.get("property_type")||""} onChange={updateFilter} aria-label="Property type"><option value="">Type</option>{propertyTypes.map(type=><option key={type} value={type}>{type}</option>)}</select>
    <select name="location" value={params.get("location")||""} onChange={updateFilter} aria-label="Location"><option value="">Location</option>{locations.map(location=><option key={location}>{location}</option>)}</select>
    <select name="size" value={params.get("size")||""} onChange={updateFilter} aria-label="Apartment size range"><option value="">Select Size Range</option><option value="0-1500">Up to 1,500 sq ft</option><option value="1500-2500">1,500–2,500 sq ft</option><option value="2500-3500">2,500–3,500 sq ft</option><option value="3500-0">3,500+ sq ft</option></select>
    <div className="projects-search"><input name="search" defaultValue={params.get("search")||""} placeholder="Search Project Name" aria-label="Search project name"/><button aria-label="Search projects">Search</button></div>
  </form>;
}
