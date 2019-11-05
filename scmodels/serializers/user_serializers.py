from rest_framework import serializers
from api.models import User, UserOTP

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=3, max_length=16, required=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ('email', 'password')

class GetUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'email', 'account_type', 'fullname', 'gender', 'birthday', 'is_banned', 'is_activated', 'created_at')

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['uid'] = instance.uid.hex
    #     return ret

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'fullname', 'gender', 'birthday')

class UserResetPassSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    
    class Meta:
        model = UserOTP
        fields = ('uid', 'email', 'otp_code_reset_pass')
    
    def create(self, validated_data):
        user_otp = UserOTP.objects.update_or_create(email=validated_data.get('email', None),
                        defaults={'otp_code_reset_pass': validated_data.get('otp_code_reset_pass', None),
                        'uid': validated_data.get('uid', None)})
        return user_otp