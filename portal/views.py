from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Category, Author
from .filters import PostListSearch
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.contrib.auth.models import Group


class PostList(ListView):
    model = Post
    template_name = 'portal/PostList.html'
    context_object_name = 'PostList'
    ordering = '-date_in'
    paginate_by = 5


class PostDetail(DetailView):
    model = Post
    template_name = 'portal/PostDetail.html'
    context_object_name = 'PostDetail'


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'portal/PostCreate.html'
    context_object_name = 'PostCreate'
    raise_exception = True
    permission_required = ('portal.add_post',)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'portal/PostCreate.html'
    context_object_name = 'PostCreate'
    raise_exception = True
    permission_required = ('portal.change_post',)


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'portal/PostDelete.html'
    success_url = reverse_lazy('PostList')
    raise_exception = True
    permission_required = ('portal.delete_post',)


# Наш фильтр на страницу search/
def SearchPostList(request):
    filters = PostListSearch(request.GET, queryset=Post.objects.all())
    return render(request, 'portal/PostSearch.html', {'filter_list': filters})



class CategoryPostList(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'portal/CategoryPostList.html'
    context_object_name = 'CategoryPostList'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribe.add(user)
    massage = 'Вы успешно подписались на категорию'
    return render(request, 'portal/Subscribe.html', {'massage': massage, 'category': category})


def is_not_subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribe.remove(user)
    massage = 'Вы отписались от категории'
    return render(request, 'portal/Subscribe.html', {'massage': massage, 'category': category})


class SubscriptionsList(ListView):
    model = Category
    template_name = 'portal/SubscriptionsList.html'
    context_object_name = 'SubscriptionsList'


def userupdate(request):
    user = request.user
    group = Group.objects.get(name='autors')
    group.user_set.add(user)
    massage = 'Поздравляем теперь вы можете писать статьи!'
    return render(request, 'portal/userupdate.html', {'massage': massage})
