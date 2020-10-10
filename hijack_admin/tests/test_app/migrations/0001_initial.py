from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            'BasicModel',
            []
        ),
        migrations.CreateModel(
            'RelatedModel',
            [
                ("user", models.ForeignKey(settings.AUTH_USER_MODEL, related_name='related', on_delete=models.CASCADE))
            ]
        ),
    ]
