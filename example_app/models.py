from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    born = models.DateField()

    def __str__(self):
        return self.last_name

class Book(models.Model):
    main_author = models.ForeignKey(Author, related_name='booklist', blank=True, null=True, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=150)
    published = models.DateField()
    num_pages = models.IntegerField()
    out_of_print = models.BooleanField(default=False)

    def get_authors(self):
        return ', '.join((str(a) for a in self.authors.all()))
    get_authors.short_description = 'authors'

    def __str__(self):
        return self.title
