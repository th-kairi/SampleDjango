# Generated by Django 4.0 on 2025-01-15 05:44

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('member_num', models.BigIntegerField(default=main.models.random_num, primary_key=True, serialize=False, verbose_name='会員番号')),
                ('name', models.CharField(max_length=20, verbose_name='氏名')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス')),
                ('is_password_encrypted', models.BooleanField(default=False, verbose_name='パスワード暗号化フラグ')),
                ('username', models.CharField(blank=True, max_length=20, null=True, verbose_name='ユーザー名')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'カスタムユーザー',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Medal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='勲章名')),
                ('image', models.ImageField(blank=True, null=True, upload_to='medals/', verbose_name='アイコン')),
                ('description', models.TextField(verbose_name='勲章の説明')),
                ('requirements', models.TextField(blank=True, max_length=400, null=True, verbose_name='授与条件')),
                ('eligible_for', models.TextField(blank=True, max_length=100, null=True, verbose_name='対象者')),
                ('awarding_method', models.TextField(blank=True, max_length=300, null=True, verbose_name='授与方法')),
            ],
            options={
                'verbose_name_plural': '勲章',
            },
        ),
        migrations.CreateModel(
            name='position',
            fields=[
                ('cd', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='コード')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('name_en', models.CharField(max_length=20, verbose_name='名称(EN)')),
                ('type', models.CharField(blank=True, choices=[('部署', '部署'), ('課', '課'), ('役職', '役職')], max_length=10, null=True)),
            ],
            options={
                'verbose_name_plural': '役職',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.customuser')),
                ('subscription_date', models.DateField(blank=True, null=True, verbose_name='加入日')),
                ('membership_status', models.CharField(choices=[('active', 'アクティブ'), ('inactive', '非アクティブ')], default='active', max_length=20, verbose_name='会員ステータス')),
                ('points', models.IntegerField(default=0, verbose_name='保有ポイント')),
            ],
            options={
                'verbose_name_plural': '会員',
            },
            bases=('main.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.customuser')),
                ('zip_code', models.CharField(blank=True, max_length=8, null=True, verbose_name='郵便番号')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='住所')),
                ('division', models.ForeignKey(blank=True, limit_choices_to={'type': '部署'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_in_division', to='main.position', verbose_name='部署')),
                ('position', models.ForeignKey(blank=True, limit_choices_to={'type': '役職'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_in_position', to='main.position', verbose_name='役職')),
                ('team', models.ForeignKey(blank=True, limit_choices_to={'type': '課'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_in_team', to='main.position', verbose_name='課')),
            ],
            options={
                'verbose_name_plural': '職員',
            },
            bases=('main.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MemberMedal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_date', models.DateField(verbose_name='取得日')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name='有効期限')),
                ('medal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.medal', verbose_name='勲章')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.member', verbose_name='会員')),
            ],
            options={
                'verbose_name_plural': '会員勲章',
                'unique_together': {('member', 'medal')},
            },
        ),
    ]
