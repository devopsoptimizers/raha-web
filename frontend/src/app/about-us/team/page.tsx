import {Footer} from "@/components/footer";
import {AnimatedHeading} from "@/components/animated-heading";import {Header} from "@/components/header";
import {ManagedPageHeader} from "@/components/managed-page-header";
import {API_URL} from "@/lib/api";

export const metadata={title:"Our Team"};
type Member={id:string;full_name:string;designation:string;biography:string;profile_image:string};
async function loadTeam():Promise<Member[]>{try{const response=await fetch(`${API_URL}/home/`,{cache:"no-store"}),body=await response.json();return(body.data||body).team_members||[]}catch{return[]}}
export default async function TeamPage(){const leaders=await loadTeam();return <><Header/><main className="inner-page team-page"><ManagedPageHeader contentKey="team-header" className="inner-page-hero" defaultLabel="About Raha Holdings" defaultTitle="Our Team"/><section className="team-directory"><div className="shell"><p className="ref-kicker">Leadership</p><AnimatedHeading>Management Team</AnimatedHeading>{leaders.length?<div className="team-directory-grid">{leaders.map(person=><article key={person.id}><div className="team-directory-photo"><img src={person.profile_image} alt={person.full_name}/></div><div className="team-directory-copy"><p>{person.designation}</p><h3>{person.full_name}</h3><span>{person.biography}</span></div></article>)}</div>:<div className="empty"><h3>Team profiles are being prepared.</h3></div>}</div></section></main><Footer/></>}
