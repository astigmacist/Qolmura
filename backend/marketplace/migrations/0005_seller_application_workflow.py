import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("marketplace", "0004_sellerapplication"),
    ]

    operations = [
        migrations.AddField(
            model_name="sellerapplication",
            name="email",
            field=models.EmailField(default="", max_length=254, verbose_name="Email"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="sellerapplication",
            name="brand_name",
            field=models.CharField(blank=True, max_length=160, verbose_name="Шеберхана / бренд"),
        ),
        migrations.AddField(
            model_name="sellerapplication",
            name="experience_years",
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Тәжірибе, жыл"),
        ),
        migrations.AddField(
            model_name="sellerapplication",
            name="estimated_product_count",
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Дайын бұйым саны"),
        ),
        migrations.AddField(
            model_name="sellerapplication",
            name="assigned_to",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"is_staff": True},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="assigned_seller_applications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Жауапты менеджер",
            ),
        ),
        migrations.AddField(
            model_name="sellerapplication",
            name="internal_notes",
            field=models.TextField(blank=True, verbose_name="Ішкі ескертпе"),
        ),
        migrations.AddField(
            model_name="sellerapplication",
            name="processed_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Өңделген уақыты"),
        ),
        migrations.AlterField(
            model_name="sellerapplication",
            name="phone",
            field=models.CharField(default="", max_length=32, verbose_name="Телефон"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="sellerapplication",
            name="city",
            field=models.CharField(default="", max_length=100, verbose_name="Қала"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="sellerapplication",
            name="craft",
            field=models.CharField(default="", max_length=200, verbose_name="Қолөнер түрі"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="sellerapplication",
            name="status",
            field=models.CharField(
                choices=[
                    ("new", "Жаңа"),
                    ("in_review", "Қаралуда"),
                    ("contacted", "Байланысқа шықты"),
                    ("approved", "Қабылданды"),
                    ("rejected", "Бас тартылды"),
                ],
                db_index=True,
                default="new",
                max_length=16,
            ),
        ),
    ]
