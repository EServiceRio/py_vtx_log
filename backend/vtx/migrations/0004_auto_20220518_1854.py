# Generated by Django 3.2.13 on 2022-05-18 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vtx', '0003_auto_20210816_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodesetup',
            name='alertTemp2',
            field=models.DecimalField(decimal_places=1, default=70.0, max_digits=12, verbose_name='Alert Temperatura'),
        ),
        migrations.AddField(
            model_name='nodesetup',
            name='alertVibraX2',
            field=models.DecimalField(decimal_places=3, default=15.0, max_digits=12, verbose_name='Alert eixo x'),
        ),
        migrations.AddField(
            model_name='nodesetup',
            name='alertVibraZ2',
            field=models.DecimalField(decimal_places=3, default=15.0, max_digits=12, verbose_name='Alert eixo z'),
        ),
        migrations.AlterField(
            model_name='hist',
            name='alertTemp',
            field=models.DecimalField(decimal_places=1, default=60.0, max_digits=12, verbose_name='Alert Temperatura'),
        ),
        migrations.AlterField(
            model_name='hist',
            name='alertVibraX',
            field=models.DecimalField(decimal_places=3, default=5.0, max_digits=12, verbose_name='Alert eixo x'),
        ),
        migrations.AlterField(
            model_name='hist',
            name='alertVibraZ',
            field=models.DecimalField(decimal_places=3, default=5.0, max_digits=12, verbose_name='Alert eixo z'),
        ),
        migrations.AlterField(
            model_name='hist',
            name='temp',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=12, verbose_name='Temperatura'),
        ),
        migrations.AlterField(
            model_name='hist',
            name='vibraX',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=12, verbose_name='eixo x'),
        ),
        migrations.AlterField(
            model_name='hist',
            name='vibraZ',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=12, verbose_name='eixo z'),
        ),
        migrations.AlterField(
            model_name='node',
            name='temp',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=12, verbose_name='Temperatura'),
        ),
        migrations.AlterField(
            model_name='node',
            name='vibraX',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=12, verbose_name='eixo x'),
        ),
        migrations.AlterField(
            model_name='node',
            name='vibraZ',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=12, verbose_name='eixo z'),
        ),
        migrations.AlterField(
            model_name='nodesetup',
            name='alertTemp',
            field=models.DecimalField(decimal_places=1, default=50.0, max_digits=12, verbose_name='Alert Temperatura'),
        ),
        migrations.AlterField(
            model_name='nodesetup',
            name='alertVibraX',
            field=models.DecimalField(decimal_places=3, default=5.0, max_digits=12, verbose_name='Alert eixo x'),
        ),
        migrations.AlterField(
            model_name='nodesetup',
            name='alertVibraZ',
            field=models.DecimalField(decimal_places=3, default=5.0, max_digits=12, verbose_name='Alert eixo z'),
        ),
    ]
