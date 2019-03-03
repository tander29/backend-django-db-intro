from django.db import models

# The built-in User model already has secure handling for things like
# username, password, email address, and so on.
from django.contrib.auth.models import User

# Your models go here!


class Permissions(models.Model):
    title = models.CharField(max_length=30)


class Roles(models.Model):
    title = models.CharField(max_length=30)
    permissions = models.ManyToManyField(Permissions)


class Users(models.Model):
    user_name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    role = models.ManyToManyField(Roles)

    def __str__(self):
        return self.user_name


class Profile(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    body = models.TextField()
    # avatar = models.ImageField()
    # why is avatar listed as VARCHAR on cms.png wouldn't an image make sense?
    avatar = models.CharField(max_length=45)


class Tags(models.Model):
    body = models.CharField(max_length=50)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)


class Categories(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE)


class Pages(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    is_published = models.BooleanField()
    is_flagged = models.BooleanField()
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    title = models.CharField(max_length=50)
    body = models.TextField()
    contributors = models.ManyToManyField(
        Users, through='Contributors', related_name='stuff')


class Contributors(models.Model):
    page_id = models.ForeignKey(
        Pages, on_delete=models.CASCADE, related_name='really')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
