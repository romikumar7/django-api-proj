from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Genre(models.Model):
    genre = models.CharField(max_length=256)

    def __str__(self):
        return str(self.genre)

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    email = models.EmailField(max_length=256, unique=True)
    phoneNo = PhoneNumberField(blank=True, region='IN')
    facebookUserName = models.CharField(max_length=256, unique=True)
    image = models.ImageField(upload_to='images', null=True)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.name, self.surname)

    def delete(self, *args, **kwargs):
        # count the total books this author is used in
        if self.book_set.count() >  0:
            return "Can not delete this book"
        else:
            super(Author, self).delete(*args, **kwargs)

    class Meta:
        unique_together = ['name', 'surname']

    def __str__(self):
        return self.name + ' ' + self.surname

class Book(models.Model):
    title = models.CharField(max_length=256, unique=True)
    pageCount = models.IntegerField(default=0)
    releaseDate = models.DateField(auto_now=True)
    authors = models.ManyToManyField(Author, blank=False)
    genre = models.OneToOneField(Genre, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.title)
