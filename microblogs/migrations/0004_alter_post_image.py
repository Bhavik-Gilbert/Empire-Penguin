# Generated by Django 4.1.3 on 2022-12-07 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microblogs', '0003_post_image_user_profile_pic_alter_post_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]