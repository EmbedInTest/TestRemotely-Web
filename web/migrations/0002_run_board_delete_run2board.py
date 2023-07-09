# Generated by Django 4.1.7 on 2023-03-29 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='runs', to='web.board'),
        ),
        migrations.DeleteModel(
            name='Run2Board',
        ),
    ]
