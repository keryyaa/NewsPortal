from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'portal/PostList.html'
    context_object_name = 'PostList'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'portal/DetailPost.html'
    context_object_name = 'PostDetail'


class PostCreate(CreateView):
    model = Post


class PostUpdate(UpdateView):
    model = Post


class PostDelete(DeleteView):
    model = Post