from django.contrib import admin

from .models import Partner, PartnerProfile, PartnerRequest, UserPresence, WeeklyChallenge


@admin.register(PartnerRequest)
class PartnerRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['sender__username', 'receiver__username']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'partner', 'sessions_count', 'connected_at']
    search_fields = ['user__username', 'partner__username']


@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'total_partners', 'is_heritage_speaker']
    search_fields = ['user__username']


@admin.register(WeeklyChallenge)
class WeeklyChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'starts_at', 'ends_at']


@admin.register(UserPresence)
class UserPresenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_online', 'last_active']
    list_filter = ['is_online']
    search_fields = ['user__username']
