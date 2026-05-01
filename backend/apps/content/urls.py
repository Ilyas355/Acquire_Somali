from django.urls import path

from .views import StoryCompleteView, StoryDetailView, StoryListView, StoryProgressUpdateView

urlpatterns = [
    path('stories/', StoryListView.as_view(), name='story-list'),
    path('stories/<int:pk>/', StoryDetailView.as_view(), name='story-detail'),
    path('stories/<int:pk>/progress/', StoryProgressUpdateView.as_view(), name='story-progress-update'),
    path('stories/<int:pk>/complete/', StoryCompleteView.as_view(), name='story-complete'),
]
