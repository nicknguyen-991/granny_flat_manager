from django.db import migrations


STANDARD_STAGES = [
    ('site_prep', 1, 5),
    ('slab', 2, 7),
    ('frame', 3, 10),
    ('lockup', 4, 14),
    ('fitout', 5, 21),
    ('handover', 6, 3),
]


def seed_stages(apps, schema_editor):
    ProjectStage = apps.get_model('construction', 'ProjectStage')
    for name, order, days in STANDARD_STAGES:
        ProjectStage.objects.get_or_create(
            stage_name=name,
            defaults={
                'sequence_order': order,
                'typical_duration_days': days,
            },
        )


def unseed_stages(apps, schema_editor):
    ProjectStage = apps.get_model('construction', 'ProjectStage')
    ProjectStage.objects.filter(
        stage_name__in=[name for name, _, _ in STANDARD_STAGES]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(seed_stages, unseed_stages),
    ]
