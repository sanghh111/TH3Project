# Generated by Django 4.0.2 on 2022-04-22 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TMDT', '0005_alter_product_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='price',
            new_name='total_price',
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]