from django.urls import path

from webapp.views import IndexView, CreatePhoto, PhotoView, UpdatePhoto, DeletePhoto, AlbumView, CreateAlbum, \
    UpdateAlbum, DeleteAlbum, FavoritesAlbum, FavoritesPhoto

app_name = "webapp"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('photo/<int:pk>/', PhotoView.as_view(), name="photo_view"),
    path('photo/add/', CreatePhoto.as_view(), name="create_photo"),
    path('photo/<int:pk>/update/', UpdatePhoto.as_view(), name="update_photo"),
    path('photo/<int:pk>/delete/', DeletePhoto.as_view(), name="delete_photo"),
    path('photo/<int:pk>/favorite', FavoritesPhoto.as_view(), name="favorites_photo"),
    path('albums/<int:pk>/', AlbumView.as_view(), name="album_view"),
    path('albums/add/', CreateAlbum.as_view(), name="create_album"),
    path('albums/<int:pk>/update/', UpdateAlbum.as_view(), name="update_album"),
    path('albums/<int:pk>/delete/', DeleteAlbum.as_view(), name="delete_album"),
    path('albums/<int:pk>/favorite', FavoritesAlbum.as_view(), name="favorites_album"),
]
