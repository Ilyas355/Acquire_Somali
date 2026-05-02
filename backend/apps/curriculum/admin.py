from django.contrib import admin

from .models import (
    CommonMistake,
    GrammarNote,
    KeyPattern,
    Phrase,
    QuizQuestion,
    Section,
    Subtopic,
    SurvivalLine,
)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_tag', 'xp_reward', 'order']
    ordering = ['order']
    search_fields = ['title']


@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section']
    ordering = ['section__order', 'order']
    search_fields = ['title']


@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ['somali', 'english', 'subtopic', 'order']
    list_filter = ['subtopic__section']
    search_fields = ['somali', 'english']


@admin.register(GrammarNote)
class GrammarNoteAdmin(admin.ModelAdmin):
    list_display = ['phrase', 'note']


@admin.register(KeyPattern)
class KeyPatternAdmin(admin.ModelAdmin):
    list_display = ['somali_pattern', 'english_pattern', 'subtopic', 'order']
    list_filter = ['subtopic']


@admin.register(CommonMistake)
class CommonMistakeAdmin(admin.ModelAdmin):
    list_display = ['wrong', 'correct', 'subtopic']
    list_filter = ['subtopic']


@admin.register(SurvivalLine)
class SurvivalLineAdmin(admin.ModelAdmin):
    list_display = ['somali', 'subtopic', 'order']
    list_filter = ['subtopic']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'layer', 'phrase']
    list_filter = ['layer']
    search_fields = ['question_text']
