from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("marketplace", "0005_seller_application_workflow")]

    operations = [
        migrations.AddField(
            model_name="product",
            name="price_is_from",
            field=models.BooleanField(
                default=False,
                help_text="Show the catalog price as a minimum when variants have different prices.",
            ),
        ),
    ]
