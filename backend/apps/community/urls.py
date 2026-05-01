from django.urls import path

from .views import LeaderboardView, PartnerRequestView, SuggestedPartnersView

urlpatterns = [
    path('partners/suggested/', SuggestedPartnersView.as_view(), name='community-partners-suggested'),
    path('partners/request/<int:pk>/', PartnerRequestView.as_view(), name='community-partners-request'),
    path('leaderboard/', LeaderboardView.as_view(), name='community-leaderboard'),
]
