from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.forms import PhotoForm
from webapp.models import Photo


class IndexView(ListView):
    model = Photo
    template_name = "photo/index.html"
    context_object_name = "photo"
    ordering = "-updated_at"
    paginate_by = 3

    def get_queryset(self):
        return Photo.objects.filter(public=1).order_by("-created_at")


class PhotoView(DetailView):
    template_name = "photo/photo_view.html"
    model = Photo


class CreatePhoto(LoginRequiredMixin, CreateView):
    form_class = PhotoForm
    template_name = "photo/create.html"

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:photo_view', kwargs={'pk': self.object.pk})


class UpdatePhoto(PermissionRequiredMixin, UpdateView):
    form_class = PhotoForm
    template_name = "photo/update.html"
    model = Photo

    def get_success_url(self):
        return reverse('webapp:photo_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return self.request.user.has_perm("webapp.update_photo") or \
               self.request.user == self.get_object().author


class DeletePhoto(PermissionRequiredMixin, DeleteView):
    model = Photo
    template_name = "photo/delete.html"
    success_url = reverse_lazy('webapp:index')
    permission_required = "webapp.delete_photo"

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class FavoritesPhoto(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        photo = get_object_or_404(Photo, pk=pk)
        user = self.request.user
        if photo.favorites.filter(id=user.pk):
            photo.favorites.remove(user.pk)
        else:
            photo.favorites.add(user.pk)
        param = {'user': user.pk, 'pk': photo.pk}
        return JsonResponse(param)
