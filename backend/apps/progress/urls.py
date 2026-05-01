from django.urls import path

from .views import HomeScreenView, QuizSubmitView, SubtopicProgressUpdateView, VocabDueView

urlpatterns = [
    path('home/', HomeScreenView.as_view(), name='progress-home'),
    path('subtopic/<int:pk>/update/', SubtopicProgressUpdateView.as_view(), name='progress-subtopic-update'),
    path('quiz/submit/', QuizSubmitView.as_view(), name='progress-quiz-submit'),
    path('vocab/due/', VocabDueView.as_view(), name='progress-vocab-due'),
]
