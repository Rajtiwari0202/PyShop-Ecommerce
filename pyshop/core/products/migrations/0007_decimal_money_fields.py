from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_review_created_at_alter_review_comment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
