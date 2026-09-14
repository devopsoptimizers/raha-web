from django.db import migrations

def create_sections(apps,schema_editor):
    Block=apps.get_model("content","ContentBlock")
    sections=[("home-featured-projects","PROMOTION","Bespoke enclaves with finesse in architecture and design","",{"label":"Featured Projects"},20),("home-testimonials","PROMOTION","What customers say about us","",{"label":"Testimonials"},21)]
    for key,kind,title,body,payload,order in sections:
        Block.objects.update_or_create(key=key,defaults={"block_type":kind,"title":title,"body":body,"payload":payload,"display_order":order,"is_published":True,"is_active":True})

class Migration(migrations.Migration):
    dependencies=[("content","0004_landowner_page_content")]
    operations=[migrations.RunPython(create_sections,migrations.RunPython.noop)]
