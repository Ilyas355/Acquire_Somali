from django.urls import path

from .views import SectionListView, SubtopicDetailView

urlpatterns = [
    path('sections/', SectionListView.as_view(), name='curriculum-sections'),
    path('subtopics/<int:pk>/', SubtopicDetailView.as_view(), name='curriculum-subtopic-detail'),
]
