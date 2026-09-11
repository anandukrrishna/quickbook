from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

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

        read_only_fields = [
            'id',
            'referral_code',
            'referral_position',
        ]


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


                placement_user = self.find_available_position(
                    referrer
                )


                user.referred_by = placement_user


                left_exists = User.objects.filter(
                    referred_by=placement_user,
                    referral_position='LEFT'
                ).exists()


                if not left_exists:

                    user.referral_position = 'LEFT'

                else:

                    user.referral_position = 'RIGHT'


            except User.DoesNotExist:

                raise serializers.ValidationError({
                    'referred_by_code':
                    'Invalid referral code.'
                })


        user.save()

        return user


    def find_available_position(self, referrer):

        queue = [referrer]


        while queue:

            current_user = queue.pop(0)


            left_user = User.objects.filter(
                referred_by=current_user,
                referral_position='LEFT'
            ).first()


            right_user = User.objects.filter(
                referred_by=current_user,
                referral_position='RIGHT'
            ).first()


            if not left_user or not right_user:

                return current_user


            queue.append(left_user)

            queue.append(right_user)