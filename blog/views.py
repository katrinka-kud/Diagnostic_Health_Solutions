from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(ListView):
    """Для отображения списков опубликованных постов"""
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogCreateView(CreateView):
    """Для создания нового поста"""
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        """Обрабатывает корректную форму и сохраняет новый пост"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogDetailView(DetailView):
    """Для отображения деталей поста"""
    model = Blog

    def get_object(self, queryset=None):
        """Увеличивает количество просмотров поста каждый раз, когда его просматривают"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    """Для обновления существующего поста"""
    model = Blog
    form_class = BlogForm

    def form_valid(self, form):
        """Обрабатывает корректную форму и обновляет пост"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        """Определяет URL для редиректа после успешного обновления поста"""
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    """Для удаления поста"""
    model = Blog
    success_url = reverse_lazy('blog:blog_list')


def status_published(request, pk):
    """Изменяет статус публикации поста. Редирект на домашнюю страницу после изменения статуса"""
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True

    blog_item.save()

    return redirect(reverse('main:home'))
