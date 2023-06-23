# Generated by Django 4.2 on 2023-06-22 22:34

import api.validators
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='User id')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email address')),
                ('email_verified', models.BooleanField(default=False)),
                ('recovery_email', models.EmailField(blank=True, max_length=254, verbose_name='Recovery email')),
                ('phone', models.CharField(blank=True, max_length=17, verbose_name='Phone number')),
                ('recovery_phone', models.CharField(blank=True, max_length=17, verbose_name='Recovery phone number')),
                ('balance', models.DecimalField(decimal_places=4, default=0, max_digits=19, validators=[django.core.validators.MinValueValidator(0)])),
                ('last_ipv4', models.CharField(blank=True, default='0.0.0.0', max_length=55, validators=[django.core.validators.validate_ipv4_address], verbose_name='Last ipv4')),
                ('user_role', models.CharField(choices=[('deleted', 'Deleted'), ('suspended', 'Suspended'), ('guest', 'Guest'), ('normal', 'Normal'), ('mod', 'Moderator'), ('admin', 'Administrator')], default='normal', max_length=10, verbose_name='User role')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('bug_report_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('report_description', models.CharField(max_length=5000)),
                ('bug_report_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'BugReports',
                'db_table': 'bug_reports',
            },
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Hashtags',
                'db_table': 'hashtags',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text_content', models.CharField(max_length=40000)),
                ('file_url', models.URLField(blank=True, max_length=300, null=True)),
                ('post_type', models.CharField(choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video'), ('audio', 'Audio')], default='text', max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('hashtags', models.ManyToManyField(blank=True, related_name='posts', to='api.hashtag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Posts',
                'db_table': 'posts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserFeedback',
            fields=[
                ('feedback_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rating', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('review', models.CharField(max_length=750)),
                ('feedback_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'userfeedback',
            },
        ),
        migrations.CreateModel(
            name='UserNotificationPreferences',
            fields=[
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='notification_preferences', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_all_email', models.BooleanField(default=True)),
                ('is_all_push', models.BooleanField(default=True)),
                ('is_all_inapp', models.BooleanField(default=True)),
                ('is_comment_on_post_email', models.BooleanField(default=True)),
                ('is_comment_on_post_inapp', models.BooleanField(default=True)),
                ('is_comment_on_post_push', models.BooleanField(default=True)),
                ('is_new_follower_email', models.BooleanField(default=True)),
                ('is_new_follower_inapp', models.BooleanField(default=True)),
                ('is_new_follower_push', models.BooleanField(default=True)),
                ('is_following_new_post_email', models.BooleanField(default=True)),
                ('is_following_new_post_inapp', models.BooleanField(default=True)),
                ('is_following_new_post_push', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'UsersNotificationPreferences',
                'db_table': 'users_notification_preferences',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('transaction_status', models.CharField(max_length=50)),
                ('status_reason', models.CharField(max_length=100)),
                ('transaction_type', models.CharField(max_length=11)),
                ('price', models.DecimalField(decimal_places=4, max_digits=19)),
                ('payment_method', models.CharField(max_length=100)),
                ('transaction_date', models.DateTimeField()),
                ('last_updated', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Transactions',
                'db_table': 'transactions',
            },
        ),
        migrations.CreateModel(
            name='SubscribedHashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suscribees', to='api.hashtag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sucribed_hashtags', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'SubscribedHashtags',
                'db_table': 'subscribed_hashtags',
            },
        ),
        migrations.CreateModel(
            name='ReportedPost',
            fields=[
                ('report_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('report_reason', models.CharField(max_length=300)),
                ('reported_x_times', models.IntegerField(default=1)),
                ('first_report_time', models.DateTimeField(auto_now_add=True)),
                ('last_report_time', models.DateField(auto_now=True, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported', to='api.post')),
            ],
            options={
                'verbose_name_plural': 'ReportedPosts',
                'db_table': 'reported_posts',
            },
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'followings',
                'db_table': 'following',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Comment id')),
                ('text_content', models.CharField(max_length=10000)),
                ('file_url', models.URLField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Comments',
                'db_table': 'comments',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BookmarkedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmarked_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked', to='api.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'BookmarkedPosts',
                'db_table': 'bookmarked_posts',
            },
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ad id')),
                ('ad_name', models.CharField(max_length=50)),
                ('bid_price', models.DecimalField(decimal_places=4, default=1, max_digits=19, validators=[django.core.validators.MinValueValidator(1)])),
                ('text_content', models.CharField(max_length=1000)),
                ('ad_file_url', models.URLField(blank=True, max_length=300)),
                ('ad_url', models.URLField(blank=True, max_length=300)),
                ('expires_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('targ_age_start', models.SmallIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(125)])),
                ('targ_age_end', models.SmallIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(125)])),
                ('targ_gender', models.CharField(blank=True, choices=[('woman', 'Woman'), ('man', 'Man'), ('trans woman', 'Trans Woman'), ('trans man', 'Trans Man'), ('other', 'Other')], max_length=11)),
                ('targ_relationship', models.CharField(blank=True, choices=[('single', 'Single'), ('married', 'Married'), ('partnership', 'Partnership'), ('open', 'Open'), ('poly', 'Poly'), ('other', 'Other')], max_length=11)),
                ('targ_education', models.CharField(blank=True, choices=[('no education', 'No education'), ('elementary', 'Elementary'), ('high school', 'High school'), ('vocational', 'Vocational'), ('some college', 'Some college'), ('college graduate', 'College graduate'), ('master degree', "Master's degree"), ('doctoral degree', 'Doctoral degree')], max_length=16)),
                ('targ_job_industry', models.CharField(blank=True, max_length=100)),
                ('targ_job_role', models.CharField(blank=True, max_length=100)),
                ('targ_country', models.CharField(blank=True, max_length=100)),
                ('targ_city', models.CharField(blank=True, max_length=100)),
                ('targ_hashtags', models.ManyToManyField(blank=True, related_name='ads', to='api.hashtag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Ads',
                'db_table': 'ads',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_pic', models.ImageField(default='images/avatars/default-profile-pic.webp', upload_to='images/avatars/', validators=[api.validators.validate_image_file_size], verbose_name='Profile picture')),
                ('given_name', models.CharField(blank=True, max_length=35)),
                ('last_name', models.CharField(blank=True, max_length=35)),
                ('display_name', models.CharField(blank=True, max_length=70)),
                ('bio', models.CharField(blank=True, max_length=5000)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('woman', 'Woman'), ('man', 'Man'), ('trans woman', 'Trans Woman'), ('trans man', 'Trans Man'), ('other', 'Other')], max_length=11)),
                ('relationship', models.CharField(blank=True, choices=[('single', 'Single'), ('married', 'Married'), ('partnership', 'Partnership'), ('open', 'Open'), ('poly', 'Poly'), ('other', 'Other')], max_length=11)),
                ('language', models.CharField(blank=True, max_length=100)),
                ('job_company', models.CharField(blank=True, max_length=100)),
                ('job_industry', models.CharField(blank=True, max_length=100)),
                ('job_role', models.CharField(blank=True, max_length=100)),
                ('education', models.CharField(blank=True, choices=[('no education', 'No education'), ('elementary', 'Elementary'), ('high school', 'High school'), ('vocational', 'Vocational'), ('some college', 'Some college'), ('college graduate', 'College graduate'), ('master degree', "Master's degree"), ('doctoral degree', 'Doctoral degree')], max_length=16)),
                ('country', models.CharField(blank=True, choices=[('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BR', 'Brazil'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('CV', 'Cabo Verde'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CR', 'Costa Rica'), ('CI', "Côte d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('KP', "Democratic People's Republic of Korea"), ('CD', 'Democratic Republic of the Congo'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('SZ', 'Eswatini'), ('ET', 'Ethiopia'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GR', 'Greece'), ('GD', 'Grenada'), ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran (Islamic Republic of)'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MK', 'North Macedonia'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia (Federated States of)'), ('MD', 'Moldova (Republic of)'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('KP', "Korea (Democratic People's Republic of)"), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine, State of'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('QA', 'Qatar'), ('RO', 'Romania'), ('RU', 'Russia'), ('RW', 'Rwanda'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('KR', 'South Korea'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syria'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States of America'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('website', models.URLField(blank=True, max_length=300)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_modified_by', to=settings.AUTH_USER_MODEL)),
                ('relationship_with', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relationship_with', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UsersProfiles',
                'db_table': 'users_profiles',
            },
        ),
        migrations.AddConstraint(
            model_name='subscribedhashtag',
            constraint=models.UniqueConstraint(fields=('user', 'hashtag'), name='composite_pk_on_subscribed_hashtags'),
        ),
        migrations.AddConstraint(
            model_name='reportedpost',
            constraint=models.UniqueConstraint(fields=('post',), name='unique_reported_post'),
        ),
        migrations.AddConstraint(
            model_name='following',
            constraint=models.UniqueConstraint(fields=('follower', 'followee'), name='composite_pk_on_following'),
        ),
        migrations.AddConstraint(
            model_name='bookmarkedpost',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='composite_pk_on_bookmarked_posts'),
        ),
    ]
