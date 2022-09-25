from django.contrib.auth import get_user_model
from django.db import models


class Photo(models.Model):
    image = models.ImageField(null=False, blank=False, upload_to="avatars", verbose_name="Фото")
    caption = models.CharField(null=False, blank=False, max_length=120, verbose_name="Подпись")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, blank=False,
                               verbose_name='Пользователь',
                               related_name='author_photos')
    album = models.ManyToManyField('webapp.Album', blank=True, verbose_name="Альбом",
                                   related_name="album_photo")
    public = models.BooleanField(default=True, verbose_name="Публичность")
    favorites = models.ManyToManyField(get_user_model(), blank=True, related_name="favor_photos")


class Album(models.Model):
    name = models.CharField(null=False, blank=False, max_length=120, verbose_name="Название")
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name="Описание")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь",
                               related_name='author_albums')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    public = models.BooleanField(default=True, verbose_name="Публичность")
    favorites = models.ManyToManyField(get_user_model(), blank=True, related_name="favor_album")
