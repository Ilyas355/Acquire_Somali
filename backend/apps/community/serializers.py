from django.contrib.auth.models import User
from rest_framework import serializers

from apps.users.models import UserProfile

from .models import PartnerProfile, WeeklyChallenge


class PartnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerProfile
        fields = ['bio', 'rating', 'total_partners', 'is_heritage_speaker', 'availability', 'preferred_format']


class SuggestedPartnerSerializer(serializers.ModelSerializer):
    handle = serializers.CharField(source='profile.handle')
    avatar = serializers.URLField(source='profile.avatar')
    partner_profile = PartnerProfileSerializer(read_only=True)
    request_status = serializers.SerializerMethodField()
    match_percentage = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'handle', 'avatar', 'partner_profile', 'request_status', 'match_percentage']

    def get_request_status(self, obj):
        return self.context.get('request_status_map', {}).get(obj.id, 'none')

    def get_match_percentage(self, obj):
        requester_pp = self.context.get('requester_partner_profile')
        candidate_pp = getattr(obj, 'partner_profile', None)
        if not candidate_pp:
            return 0
        score = 0
        if candidate_pp.is_heritage_speaker != getattr(requester_pp, 'is_heritage_speaker', False):
            score += 40
        if requester_pp and candidate_pp.preferred_format and candidate_pp.preferred_format == requester_pp.preferred_format:
            score += 30
        if requester_pp and candidate_pp.availability and candidate_pp.availability == requester_pp.availability:
            score += 30
        return score


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    xp = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'handle', 'avatar', 'xp']

    def get_xp(self, obj):
        if hasattr(obj, 'weekly_xp'):
            return obj.weekly_xp
        return obj.total_xp


class WeeklyChallengeSerializer(serializers.ModelSerializer):
    reward_badge = serializers.CharField(source='reward_badge.title')

    class Meta:
        model = WeeklyChallenge
        fields = ['id', 'title', 'reward_badge', 'starts_at', 'ends_at']
