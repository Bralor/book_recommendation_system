from django.db import models

# Create your models here.
class Collection(models.Model):
    id = models.IntegerField(primary_key=True)
    isbn = models.TextField(db_column='ISBN', blank=True, null=True)  # Field name made lowercase.
    book_title = models.TextField(db_column='Book-Title', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    book_author = models.TextField(db_column='Book-Author', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    year_of_publication = models.TextField(db_column='Year-Of-Publication', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    publisher = models.TextField(db_column='Publisher', blank=True, null=True)  # Field name made lowercase.
    image_url_s = models.TextField(db_column='Image-URL-S', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    image_url_m = models.TextField(db_column='Image-URL-M', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    image_url_l = models.TextField(db_column='Image-URL-L', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    user_id = models.TextField(db_column='User-ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    book_rating = models.TextField(db_column='Book-Rating', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'collection'
