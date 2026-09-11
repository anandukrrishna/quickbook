from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts.models import User


class ReferralTreeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        def build_tree(current_user):
            referrals = current_user.referrals.all()

            return {
                "id": current_user.id,
                "username": current_user.username,
                "referral_code": current_user.referral_code,
                "children": [
                    build_tree(referral)
                    for referral in referrals
                ]
            }

        return Response(build_tree(user))


class ReferralRootView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        root_user = user

        while root_user.referred_by:
            root_user = root_user.referred_by

        return Response({
            "id": root_user.id,
            "username": root_user.username,
            "referral_code": root_user.referral_code
        })


class ReferralStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        def count_team(current_user):
            total = 0

            for referral in current_user.referrals.all():
                total += 1
                total += count_team(referral)

            return total

        left_user = user.referrals.filter(
            referral_position='LEFT'
        ).first()

        right_user = user.referrals.filter(
            referral_position='RIGHT'
        ).first()

        left_count = count_team(left_user) if left_user else 0
        right_count = count_team(right_user) if right_user else 0

        return Response({
            "user_id": user.id,
            "username": user.username,
            "left_team_count": left_count,
            "right_team_count": right_count
        })