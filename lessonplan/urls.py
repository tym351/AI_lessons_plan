from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate/', views.generate_lessonplan, name='generate_lessonplan'),
    path('edit/<int:pk>/', views.edit_lessonplan, name='edit_lessonplan'),
    # path('evaluate/<int:pk>/', views.evaluate_lessonplan, name='evaluate_lessonplan'),
    path('list/', views.list_lessonplans, name='list_lessonplans'),
    path('test_tongyi_key/', views.test_tongyi_key, name='test_tongyi_key'),
    path('delete/<int:pk>/', views.delete_lessonplan, name='delete_lessonplan'),
    path('detail/<int:pk>/', views.detail_lessonplan, name='detail_lessonplan'),
    path('reflect/<int:pk>/', views.reflect_lessonplan, name='reflect_lessonplan'),
]
