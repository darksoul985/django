# Generated by Django 4.0.4 on 2022-08-21 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='обновлен')),
                ('is_active', models.BooleanField(default=True, verbose_name='активен')),
                ('status', models.CharField(choices=[('FM', 'формируется'), ('STP', 'отправлен в обработку'), ('PD', 'оплачен'), ('PRD', 'обрабатывается'), ('RDY', 'готов к выдаче'), ('CNC', 'отменен')], default='FM', max_length=3, verbose_name='статус заказа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
                'ordering': ('-created',),
            },
        ),
    ]
