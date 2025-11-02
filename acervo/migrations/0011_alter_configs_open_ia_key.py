from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("acervo", "0010_configs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="configs",
            name="open_ia_key",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="Chave da OpenAI",
            ),
        ),
    ]
