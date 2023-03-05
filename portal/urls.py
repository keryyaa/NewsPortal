from django.urls import path
from .views import PostList, PostDetail, SearchPostList, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', PostList.as_view(), name='PostList'),
    path('<int:pk>/', PostDetail.as_view(), name='PostDetail'),
    path('search/', SearchPostList, name='PostListSearch'),
    path('create/', PostCreate.as_view(), name='PostCreate'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='PostUpdate'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='PostDelete'),

]
