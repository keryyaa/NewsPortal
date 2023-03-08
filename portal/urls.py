from django.urls import path
from portal import views

urlpatterns = [
    path('', views.PostList.as_view(), name='PostList'),
    path('<int:pk>/', views.PostDetail.as_view(), name='PostDetail'),
    path('search/', views.SearchPostList, name='PostListSearch'),
    path('create/', views.PostCreate.as_view(), name='PostCreate'),
    path('<int:pk>/update/', views.PostUpdate.as_view(), name='PostUpdate'),
    path('<int:pk>/delete/', views.PostDelete.as_view(), name='PostDelete'),
    path('category/<int:pk>/', views.CategoryPostList.as_view(), name='CategoryPostList'),
    path('category/<int:pk>/subscribe', views.subscribe, name='subscribe_user'),
    path('category/<int:pk>/is_not_subscribe', views.is_not_subscribe, name='is_not_subscribe'),
    path('subscriptions/', views.SubscriptionsList.as_view(), name='SubscriptionsList'),
    path('userupdate/', views.userupdate, name='userupdate'),

]
