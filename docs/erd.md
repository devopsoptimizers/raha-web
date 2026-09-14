# Database ERD

```mermaid
erDiagram
  USER ||--o{ PROJECT : creates
  DIVISION ||--o{ DISTRICT : contains
  DISTRICT ||--o{ AREA : contains
  AREA ||--o{ PROJECT : locates
  PROJECT }o--o{ AMENITY : offers
  PROJECT ||--o{ APARTMENT_TYPE : defines
  PROJECT ||--o{ UNIT : contains
  APARTMENT_TYPE ||--o{ UNIT : classifies
  PROJECT ||--o{ GALLERY_ITEM : presents
  PROJECT ||--o{ CONSTRUCTION_PROGRESS : reports
  CONSTRUCTION_PROGRESS ||--o{ PROGRESS_IMAGE : illustrates
  PROJECT ||--o{ TESTIMONIAL : references
  BLOG_CATEGORY ||--o{ BLOG_POST : groups
  BLOG_POST }o--o{ TAG : tagged
  USER ||--o{ BLOG_POST : authors
  JOB ||--o{ JOB_APPLICATION : receives
  PROJECT ||--o{ INQUIRY : concerns
  APARTMENT_TYPE ||--o{ INQUIRY : interests
  USER ||--o{ INQUIRY : assigned
  INQUIRY ||--o{ INQUIRY_NOTE : records
  PROJECT ||--o{ MEETING_REQUEST : schedules
  DIVISION ||--o{ LANDOWNER_PROPOSAL : locates
  DISTRICT ||--o{ LANDOWNER_PROPOSAL : locates
  AREA ||--o{ LANDOWNER_PROPOSAL : locates
  LANDOWNER_PROPOSAL ||--o{ PROPOSAL_DOCUMENT : supports
  USER ||--o{ AUDIT_LOG : performs
```

Location foreign keys preserve canonical geography. Project-to-amenity is many-to-many so amenities are reusable. Inventory is tied to both its project and apartment type, with a database uniqueness rule across project/building/floor/unit. Deleting a project is soft; dependent media and inventory are protected from accidental disappearance through that boundary. Submission records retain nullable project/user references so historical leads survive staff or catalog changes. Supporting files are child rows, enabling multiple uploads without repeating proposal data.
