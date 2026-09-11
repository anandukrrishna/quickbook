from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    referred_by_code = serializers.CharField(
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'referral_code',
            'referred_by_code',
            'referral_position',
        ]

        read_only_fields = ['id', 'referral_code','referral_position',]

    def create(self, validated_data):
        password = validated_data.pop('password')

        referred_by_code = validated_data.pop(
            'referred_by_code',
            None
        )

        user = User(**validated_data)
        user.set_password(password)

        if referred_by_code:
            try:
                referrer = User.objects.get(
                    referral_code=referred_by_code
                )

                left_user_exists = User.objects.filter(
                    referred_by=referrer,
                    referral_position='LEFT'
                ).exists()

                right_user_exists = User.objects.filter(
                    referred_by=referrer,
                    referral_position='RIGHT'
                ).exists()

                user.referred_by = referrer

                if not left_user_exists:
                    user.referral_position = 'LEFT'

                elif not right_user_exists:
                    user.referral_position = 'RIGHT'

                else:
                    raise serializers.ValidationError({
                        'referred_by_code':
                        'This referral user already has both positions filled.'
                    })

            except User.DoesNotExist:
                raise serializers.ValidationError({
                    'referred_by_code': 'Invalid referral code.'
                })

        user.save()

        return user