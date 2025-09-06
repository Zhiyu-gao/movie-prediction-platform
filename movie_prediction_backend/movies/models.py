# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MovieGenreClassificationFinal(models.Model):
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.
    year = models.CharField(db_column='Year', max_length=255, blank=True, null=True)  # Field name made lowercase.
    director = models.CharField(db_column='Director', max_length=255, blank=True, null=True)  # Field name made lowercase.
    duration = models.CharField(db_column='Duration', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rating = models.CharField(db_column='Rating', max_length=255, blank=True, null=True)  # Field name made lowercase.
    votes = models.CharField(db_column='Votes', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=255, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=255, blank=True, null=True)  # Field name made lowercase.
    budget_usd = models.CharField(db_column='Budget_USD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    boxoffice_usd = models.CharField(db_column='BoxOffice_USD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    genre = models.CharField(db_column='Genre', max_length=255, blank=True, null=True)  # Field name made lowercase.
    production_company = models.CharField(db_column='Production_Company', max_length=255, blank=True, null=True)  # Field name made lowercase.
    content_rating = models.CharField(db_column='Content_Rating', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lead_actor = models.CharField(db_column='Lead_Actor', max_length=255, blank=True, null=True)  # Field name made lowercase.
    num_awards = models.CharField(db_column='Num_Awards', max_length=255, blank=True, null=True)  # Field name made lowercase.
    critic_reviews = models.CharField(db_column='Critic_Reviews', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'movie_genre_classification_final'