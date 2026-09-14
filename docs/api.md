# API catalogue

All domain routes use `/api/v1/`. Authentication: `auth/login`, `auth/token/refresh`, `auth/logout`, `auth/forgot-password`, `auth/reset-password`, `auth/me`, `auth/change-password`. Platform: `health`, plus OpenAPI at `/api/schema/`, Swagger at `/api/docs/`, and ReDoc at `/api/redoc/`.

Every paginated list response includes `count`, absolute `next` and `previous` links (or `null` at either boundary), the result array in `data`, and detailed page information in `meta`.

CRUD resources: `projects`, `divisions`, `districts`, `areas`, `amenities`, `apartment-types`, `units`, `gallery`, `progress`, `sliders`, `content-blocks`, `team-members`, `testimonials`, `blogs`, `blog-categories`, `blog-tags`, `jobs`, `job-applications`, `inquiries`, `meeting-requests`, `landowner-proposals`, `contact-messages`, `feedback`, and `suggestions`.

Special routes: `home/`; `projects/featured/`; `projects/slug/{slug}/`; project `status`, `amenities`, `apartment-types`, `units`, `gallery`, `floor-plans`, and `progress` actions; unit `availability`; gallery/slider `reorder`; blog/job `slug`; blog `related`; job `apply`; inquiry/meeting/landowner `status` and `assign`; inquiry `notes`; newsletter `subscribe`, `verify`, `unsubscribe`, and `subscribers`; settings `public` and staff detail/update.

List endpoints support page/page_size. Project filters include status, type, geography, bedroom count, price/size ranges, handover date, and featured status. Use `search` and `ordering` where documented by the generated schema.
