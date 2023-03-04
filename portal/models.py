from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        pos = self.post_set.aggregate(postRat=Sum('rating'))
        posR = 0
        posR += pos.get('postRat')

        com = self.authorUser.comment_set.aggregate(comSum=Sum('rating'))
        comR = 0
        comR += com.get('comSum')

        self.rating = posR + comR
        self.save()

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_in = models.DateTimeField(auto_now_add=True)
    TYPE_CATEGORY = [
        ('NW', 'Новость'),
        ('AR', 'Статья')
    ]
    type_category = models.CharField(max_length=2, choices=TYPE_CATEGORY, default='NW')
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} Категория: {self.category}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_in = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'

