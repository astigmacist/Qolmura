from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("marketplace", "0002_product_cover_url")]

    operations = [
        migrations.AddField(model_name="product", name="materials_kk", field=models.CharField(blank=True, max_length=240)),
        migrations.AddField(model_name="product", name="materials_ru", field=models.CharField(blank=True, max_length=240)),
        migrations.AddField(model_name="product", name="dimensions_kk", field=models.CharField(blank=True, max_length=180)),
        migrations.AddField(model_name="product", name="dimensions_ru", field=models.CharField(blank=True, max_length=180)),
        migrations.AddField(model_name="product", name="care_kk", field=models.TextField(blank=True)),
        migrations.AddField(model_name="product", name="care_ru", field=models.TextField(blank=True)),
        migrations.AddField(model_name="product", name="production_time_days", field=models.PositiveSmallIntegerField(default=3)),
        migrations.AddField(model_name="product", name="is_demo", field=models.BooleanField(db_index=True, default=False)),
    ]
