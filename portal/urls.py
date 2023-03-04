from django.urls import path
from .views import PostList, PostDetail

urlpatterns = [
    path('', PostList.as_view(), name='PostList'),
    path('<int:pk>/', PostDetail.as_view(), name='PostDetail')

]