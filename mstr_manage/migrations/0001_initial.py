# Generated by Django 3.0.2 on 2020-01-04 07:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=32)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('image', models.FileField(blank=True, help_text='ロゴなど。アップロード可能な形式はpng or jpg', null=True, upload_to='customers', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg'])])),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=32)),
                ('alias', models.CharField(blank=True, help_text='正式名称以外に必要な場合に記入', max_length=16, null=True, verbose_name='短縮名')),
                ('area', models.CharField(choices=[('north', 'north'), ('middle', 'middle'), ('south', 'south')], default='0', help_text='主な販売地域', max_length=16, verbose_name='販売エリア')),
            ],
        ),
        migrations.CreateModel(
            name='Product_per_Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wholesale_price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='卸値')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mstr_manage.Customer', verbose_name='得意先')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mstr_manage.Product', verbose_name='商品')),
            ],
        ),
        migrations.CreateModel(
            name='Deliv_dest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('name', models.CharField(max_length=32)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mstr_manage.Customer', verbose_name='得意先')),
            ],
        ),
        migrations.AddConstraint(
            model_name='product_per_customer',
            constraint=models.UniqueConstraint(fields=('customer', 'product'), name='unique_product'),
        ),
        migrations.AddConstraint(
            model_name='deliv_dest',
            constraint=models.UniqueConstraint(fields=('customer', 'code'), name='unique_deliv_dest'),
        ),
    ]