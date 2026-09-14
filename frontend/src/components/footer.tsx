"use client";
import Link from "next/link";
import {useSiteSettings} from "./site-settings";

const socialNames=["facebook","linkedin","instagram","youtube"] as const;

export function Footer(){
  const s=useSiteSettings(),socials=s.social_links||{};
  const links=[[s.footer_link_1_label||"Projects",s.footer_link_1_url||"/properties"],[s.footer_link_2_label||"Blog",s.footer_link_2_url||"/blog"],[s.footer_link_3_label||"Careers",s.footer_link_3_url||"/careers"],[s.footer_link_4_label||"Customer portal",s.footer_link_4_url||"/login"]].filter(([label,url])=>label&&url);
  return <footer className="site-footer">
    <div className="shell footer-main">
      <div className="footer-brand"><img src={s.logo||"/images/brand/raha-one-color-white.png"} alt={s.company_name||"Raha Holdings"} className="footer-logo"/><p>{s.footer_content||s.default_seo_description||"Thoughtfully designed homes, trusted expertise, and personal guidance for every step of your property journey."}</p><div className="footer-socials">{socialNames.map(name=>socials[name]&&<a href={socials[name]} target="_blank" rel="noopener noreferrer" aria-label={name[0].toUpperCase()+name.slice(1)} key={name}><SocialIcon name={name}/></a>)}</div></div>
      <div className="footer-column"><h4>{s.footer_explore_title||"Explore"}</h4><div className="footer-links">{links.map(([label,url],index)=><Link href={url!} key={`footer-link-${index}`}>{label}<span aria-hidden="true">→</span></Link>)}</div></div>
      <div className="footer-column"><h4>{s.footer_contact_title||"Visit & contact"}</h4><div className="footer-contact">{s.office_address&&<p><small>Head office</small>{s.office_address}</p>}{s.hotline&&<a href={`tel:${s.hotline.replace(/[^+\d]/g,"")}`}><small>Phone</small>{s.hotline}</a>}{s.email&&<a href={`mailto:${s.email}`}><small>Email</small>{s.email}</a>}{s.business_hours&&<p><small>Office hours</small>{s.business_hours}</p>}</div></div>
    </div>
    <div className="footer-copy"><span>{s.footer_copyright_text||`© ${new Date().getFullYear()} ${s.company_name}. All rights reserved.`}</span><nav aria-label="Legal"><Link href="/about-us/privacy-policy">Privacy policy</Link><Link href="/contact-us">Contact</Link></nav></div>
  </footer>;
}

function SocialIcon({name}:{name:typeof socialNames[number]}){
  if(name==="facebook")return <svg viewBox="0 0 24 24"><path d="M14 8h3V4h-3c-3 0-5 2-5 5v3H6v4h3v8h4v-8h3l1-4h-4V9c0-.7.3-1 1-1Z"/></svg>;
  if(name==="linkedin")return <svg viewBox="0 0 24 24"><path d="M6 8.3H2V22h4V8.3ZM4 2a2.3 2.3 0 1 0 0 4.6A2.3 2.3 0 0 0 4 2ZM22 14.2c0-4.1-2.2-6-5.1-6-2.4 0-3.4 1.3-4 2.2V8.3H9V22h4v-6.8c0-1.8.3-3.6 2.6-3.6 2.3 0 2.3 2.1 2.3 3.7V22H22v-7.8Z"/></svg>;
  if(name==="instagram")return <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" className="social-dot"/></svg>;
  return <svg viewBox="0 0 24 24"><path d="M22 7.2a3 3 0 0 0-2.1-2.1C18 4.5 12 4.5 12 4.5s-6 0-7.9.6A3 3 0 0 0 2 7.2 31 31 0 0 0 1.5 12c0 1.6.1 3.2.5 4.8a3 3 0 0 0 2.1 2.1c1.9.6 7.9.6 7.9.6s6 0 7.9-.6a3 3 0 0 0 2.1-2.1c.4-1.6.5-3.2.5-4.8s-.1-3.2-.5-4.8ZM10 15.5v-7l6 3.5-6 3.5Z"/></svg>;
}
