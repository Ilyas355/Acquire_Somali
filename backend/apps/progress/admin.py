from django.contrib import admin

from .models import QuizAttempt, UserSectionProgress, UserSubtopicProgress, VocabReview


@admin.register(UserSectionProgress)
class UserSectionProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'section', 'is_unlocked', 'is_completed', 'subtopics_completed']
    list_filter = ['is_unlocked', 'is_completed']
    search_fields = ['user__username']


@admin.register(UserSubtopicProgress)
class UserSubtopicProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'subtopic', 'current_step', 'is_completed', 'phrases_completed']
    list_filter = ['current_step', 'is_completed']
    search_fields = ['user__username']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'is_correct', 'xp_awarded', 'attempted_at']
    list_filter = ['is_correct']
    search_fields = ['user__username']


@admin.register(VocabReview)
class VocabReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'phrase', 'next_review', 'interval', 'repetitions']
    search_fields = ['user__username']
