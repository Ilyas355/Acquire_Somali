from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    handle = models.CharField(max_length=50, unique=True)
    avatar = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_diaspora = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    total_xp = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True, db_index=True)
    daily_reminder_time = models.TimeField(null=True, blank=True)
    audio_autoplay = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=True)
    transliteration = models.BooleanField(default=False)

    def __str__(self):
        return f"@{self.handle} ({self.user.username})"


class Level(models.Model):
    name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    description = models.TextField()
    xp_required = models.PositiveIntegerField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.name} — {self.subtitle}"


class UserLevel(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='level')
    current_level = models.ForeignKey(
        Level, on_delete=models.PROTECT, related_name='user_levels')
    xp_into_level = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} — {self.current_level.name}"


class Achievement(models.Model):
    key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    icon = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'achievement']

    def __str__(self):
        return f"{self.user.username} — {self.achievement.title}"
