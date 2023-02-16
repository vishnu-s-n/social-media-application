from django.urls import path
from post import views
urlpatterns = [
    path('', views.index, name="index"),
    path('newpost/', views.NewPost, name="newpost"),
    path('<uuid:post_id>/', views.PostDetails, name="postdetails"),
    path('<uuid:post_id>/like/',views.Like, name="like"),
    path('<uuid:post_id>/favourite/',views.favourite, name="favourite")


]
