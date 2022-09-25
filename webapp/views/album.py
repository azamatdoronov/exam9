from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import AlbumForm
from webapp.models import Album


class AlbumView(DetailView):
    template_name = "albums/album_view.html"
    model = Album


class CreateAlbum(LoginRequiredMixin, CreateView):
    form_class = AlbumForm
    template_name = "albums/create.html"

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:album_view", kwargs={"pk": self.object.pk})


class UpdateAlbum(PermissionRequiredMixin, UpdateView):
    form_class = AlbumForm
    template_name = "albums/update.html"
    model = Album
    permission_required = 'webapp:update_album'

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        get_object_or_404(Album, pk=pk)
        user = self.request.user
        form.instance.author = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:album_view", kwargs={"pk": self.object.pk})


class DeleteAlbum(PermissionRequiredMixin, DeleteView):
    model = Album
    template_name = "albums/delete.html"
    success_url = reverse_lazy('webapp:index')
    permission_required = "webapp.delete_album"

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class FavoritesAlbum(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        album = get_object_or_404(Album, pk=pk)
        user = self.request.user
        if album.favorites.filter(id=user.pk):
            album.favorites.remove(user.pk)
        else:
            album.favorites.add(user.pk)
        param = {'user': user.pk, 'pk': album.pk}
        return JsonResponse(param)
