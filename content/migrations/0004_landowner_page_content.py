from django.db import migrations


def create_landowner_content(apps, schema_editor):
    ContentBlock = apps.get_model("content", "ContentBlock")
    blocks = [
        ("landowner-hero", "HEADER", "Landowner", "", {"label": "Partner with Raha Holdings"}, 110),
        (
            "landowner-introduction",
            "LANDOWNER",
            "Build something enduring with us",
            "Raha Holdings partners with landowners to create considered developments founded on transparency, design quality, and shared long-term value.",
            {
                "label": "Landowners",
                "benefits_title": "Why choose Raha Holdings?",
                "benefits": [
                    "Faster project execution through careful planning and proven construction expertise",
                    "Elegant, contemporary architecture with intelligently designed spaces",
                    "Rigorous quality control and benchmark materials",
                    "Elevated living standards with thoughtfully selected amenities",
                    "Responsive customer care and dedicated after-sales support",
                    "Long-term value across promising locations in Dhaka",
                ],
            },
            111,
        ),
        ("landowner-form-section", "CTA", "Meet the Professionals", "", {"label": "Start a conversation"}, 112),
    ]
    for key, block_type, title, body, payload, order in blocks:
        ContentBlock.objects.update_or_create(
            key=key,
            defaults={"block_type": block_type, "title": title, "body": body, "payload": payload, "display_order": order, "is_published": True, "is_active": True},
        )


class Migration(migrations.Migration):
    dependencies = [("content", "0003_careers_page_content")]
    operations = [migrations.RunPython(create_landowner_content, migrations.RunPython.noop)]
