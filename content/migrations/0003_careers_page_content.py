from django.db import migrations


def create_careers_content(apps, schema_editor):
    ContentBlock = apps.get_model("content", "ContentBlock")
    blocks = [
        ("careers-hero", "HEADER", "Career", "", {"label": "Build your future with us"}, 100),
        (
            "careers-introduction",
            "PROMOTION",
            "Why Join Us?",
            "We believe exceptional places are created by exceptional people. At Raha Holdings, you will work in a dynamic, collaborative environment where thoughtful ideas, professional growth, and meaningful contributions are valued.\n\nJoin a diverse team committed to quality, integrity, and better urban living. You will have the opportunity to build a career around your strengths while shaping homes and communities that make a lasting difference.",
            {"label": "Our people"},
            101,
        ),
        (
            "careers-application-panel",
            "CTA",
            "Submit your application",
            "",
            {"label": "Apply now", "image_label": "Join the team", "image_title": "Do meaningful work with great people."},
            102,
        ),
    ]
    for key, block_type, title, body, payload, order in blocks:
        ContentBlock.objects.update_or_create(
            key=key,
            defaults={
                "block_type": block_type,
                "title": title,
                "body": body,
                "payload": payload,
                "display_order": order,
                "is_published": True,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [("content", "0002_slider_video_url_slider_google_maps_url")]
    operations = [migrations.RunPython(create_careers_content, migrations.RunPython.noop)]
