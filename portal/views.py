from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .filters import PostListSearch
from django.shortcuts import render
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'portal/PostList.html'
    context_object_name = 'PostList'
    ordering = '-date_in'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'portal/PostDetail.html'
    context_object_name = 'PostDetail'


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'portal/PostCreate.html'
    context_object_name = 'PostCreate'


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'portal/PostCreate.html'
    context_object_name = 'PostCreate'


class PostDelete(DeleteView):
    model = Post
    template_name = 'portal/PostDelete.html'
    success_url = reverse_lazy('PostList')


# Наш фильтр на страницу search/
def SearchPostList(request):
    filters = PostListSearch(request.GET, queryset=Post.objects.all())
    return render(request, 'portal/PostSearch.html', {'filter_list': filters})
