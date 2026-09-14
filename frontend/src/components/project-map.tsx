export function ProjectMap({name,address,latitude,longitude,googleMapsUrl}:{name:string;address:string;latitude?:string|number|null;longitude?:string|number|null;googleMapsUrl?:string}){
  const query=latitude&&longitude?`${latitude},${longitude}`:address;
  const embedUrl=`https://www.google.com/maps?q=${encodeURIComponent(query)}&z=15&output=embed`;
  const directionsUrl=googleMapsUrl||`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`;
  return <div className="project-map-real"><iframe src={embedUrl} title={`${name} location on Google Maps`} loading="lazy" referrerPolicy="no-referrer-when-downgrade" allowFullScreen/><a href={directionsUrl} target="_blank" rel="noreferrer">View larger map ↗</a></div>;
}
