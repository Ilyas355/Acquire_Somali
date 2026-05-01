from datetime import timedelta

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import UserProfile

from .models import Partner, PartnerProfile, PartnerRequest, WeeklyChallenge
from .serializers import LeaderboardEntrySerializer, SuggestedPartnerSerializer, WeeklyChallengeSerializer


class SuggestedPartnersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        existing_partner_ids = Partner.objects.filter(
            user=request.user
        ).values_list('partner_id', flat=True)

        rejected_by_me = PartnerRequest.objects.filter(
            sender=request.user, status=PartnerRequest.Status.REJECTED
        ).values_list('receiver_id', flat=True)

        rejected_me = PartnerRequest.objects.filter(
            receiver=request.user, status=PartnerRequest.Status.REJECTED
        ).values_list('sender_id', flat=True)

        candidates = (
            User.objects
            .filter(partner_profile__isnull=False)
            .exclude(pk=request.user.pk)
            .exclude(pk__in=existing_partner_ids)
            .exclude(pk__in=rejected_by_me)
            .exclude(pk__in=rejected_me)
            .select_related('profile', 'partner_profile')
        )

        outgoing = set(PartnerRequest.objects.filter(
            sender=request.user, status=PartnerRequest.Status.PENDING,
        ).values_list('receiver_id', flat=True))

        incoming = set(PartnerRequest.objects.filter(
            receiver=request.user, status=PartnerRequest.Status.PENDING,
        ).values_list('sender_id', flat=True))

        try:
            requester_partner_profile = request.user.partner_profile
        except PartnerProfile.DoesNotExist:
            requester_partner_profile = None

        serializer = SuggestedPartnerSerializer(
            candidates,
            many=True,
            context={
                'request': request,
                'request_status_map': {
                    **{uid: 'pending' for uid in outgoing},
                    **{uid: 'received' for uid in incoming},
                },
                'requester_partner_profile': requester_partner_profile,
            },
        )
        return Response(serializer.data)


class PartnerRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        receiver = get_object_or_404(User, pk=pk)

        if receiver == request.user:
            return Response({'error': 'Cannot send a request to yourself.'}, status=400)

        if Partner.objects.filter(user=request.user, partner=receiver).exists():
            return Response({'status': 'already_partners'}, status=400)

        existing = PartnerRequest.objects.filter(
            sender=request.user, receiver=receiver
        ).first()

        if existing:
            if existing.status == PartnerRequest.Status.REJECTED:
                return Response({'status': 'rejected'}, status=400)
            return Response({'status': existing.status})

        with transaction.atomic():
            mutual = PartnerRequest.objects.filter(
                sender=receiver,
                receiver=request.user,
                status=PartnerRequest.Status.PENDING,
            ).first()

            if mutual:
                mutual.status = PartnerRequest.Status.ACCEPTED
                mutual.save(update_fields=['status'])
                Partner.objects.get_or_create(user=request.user, partner=receiver)
                Partner.objects.get_or_create(user=receiver, partner=request.user)
                return Response({'status': 'accepted'})

            partner_request = PartnerRequest.objects.create(
                sender=request.user,
                receiver=receiver,
                status=PartnerRequest.Status.PENDING,
            )

        return Response({'status': partner_request.status})


class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tab = request.query_params.get('tab', 'all_time')
        now = timezone.now()

        if tab == 'this_week':
            week_start = (now - timedelta(days=now.weekday())).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            profiles = (
                UserProfile.objects
                .select_related('user')
                .annotate(
                    weekly_xp=Coalesce(
                        Sum(
                            'user__quiz_attempts__xp_awarded',
                            filter=Q(user__quiz_attempts__attempted_at__gte=week_start),
                        ),
                        0,
                    )
                )
                .order_by('-weekly_xp')[:50]
            )
        elif tab == 'partners':
            partner_ids = Partner.objects.filter(
                user=request.user
            ).values_list('partner_id', flat=True)
            profiles = (
                UserProfile.objects
                .filter(user_id__in=partner_ids)
                .select_related('user')
                .order_by('-total_xp')[:50]
            )
        else:
            profiles = (
                UserProfile.objects
                .select_related('user')
                .order_by('-total_xp')[:50]
            )

        current_challenge = (
            WeeklyChallenge.objects
            .filter(starts_at__lte=now, ends_at__gte=now)
            .select_related('reward_badge')
            .first()
        )

        return Response({
            'tab': tab,
            'leaderboard': LeaderboardEntrySerializer(profiles, many=True).data,
            'current_challenge': WeeklyChallengeSerializer(current_challenge).data if current_challenge else None,
        })
