from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('contents/new', views.create_content),
    path('contents/create', views.create),
    path('contents/<int:content_id>', views.content), 
    path('contents/edit/<int:content_id>', views.edit), 
    path('contents/update/<int:content_id>', views.update),
    path('add_comment/<int:content_id>', views.post_comment),
    path('delete/<int:content_id>/<int:comment_id>', views.delete_comment),
    # path('total_views/<int:content_id>', views.total_views),
    path("like/<int:content_id>", views.likes),
    path("unlike/<int:content_id>", views.unlike),
    path('logout', views.logout),
    path('<int:content_id>/delete', views.delete),
    path('cancle', views.cancle),
]
