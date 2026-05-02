from django.contrib import admin

from .models import Achievement, Level, UserAchievement, UserLevel, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'handle', 'total_xp', 'current_streak', 'is_diaspora']
    search_fields = ['user__username', 'handle']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'subtitle', 'xp_required', 'order']
    ordering = ['order']


@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_level', 'xp_into_level']
    search_fields = ['user__username']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['key', 'title']
    search_fields = ['key', 'title']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    search_fields = ['user__username']
