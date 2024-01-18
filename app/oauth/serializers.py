from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator, MinLengthValidator
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken 
from organization.models import Organization, UserToOrganization, STATUS_CHECKING, ROLE_OWNER
from organization.validators import inn_check_api_validator
from .models import ChangePasswordUUID

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials"),
        "not_found_account": _("User not found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.SlugRelatedField(slug_field=self.username_field, queryset=User.objects.filter(is_active=True), write_only=True)
        self.fields['message'] = serializers.CharField(read_only=True)


    def validate(self, attrs):
        self.user = attrs[self.username_field]
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        self.user.send_reset_password()
        return {
            'message': _('Send message to email success')
        }


class ChangePasswordVerifySerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uuid'] = serializers.SlugRelatedField(slug_field='uuid', queryset=ChangePasswordUUID.objects.all(), write_only=True)
        self.fields['message'] = serializers.CharField(read_only=True)

    def validate(self, attrs):
        uuid: ChangePasswordUUID = attrs['uuid']
        uuid.validate()
        return {
            'message': _('UUID verified')
        }


class ChangePasswordPerformSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uuid'] = serializers.SlugRelatedField(slug_field='uuid', queryset=ChangePasswordUUID.objects.all(), write_only=True)
        self.fields['password1'] = serializers.CharField(write_only=True)
        self.fields['password2'] = serializers.CharField(write_only=True)
        self.fields['message'] = serializers.CharField(read_only=True)

    def validate(self, attrs):
        password1: str = attrs.pop('password1')
        password2: str = attrs.pop('password2')
        uuid: ChangePasswordUUID = attrs['uuid']
        uuid.validate()
        if not password1 == password2:
            raise exceptions.ValidationError({'password2': [_("Passwords must be equels")]}, "password1_not_equel_password2")
        attrs['password'] = password1
        return attrs
    
    def create(self, validated_data):
        uuid: ChangePasswordUUID = validated_data.pop('uuid')
        uuid.change_password(**validated_data)
        return {
            "message": _('Password changed')
        }
    

class CreateUserLegalSerializer(serializers.Serializer):
    inn = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    phone = serializers.CharField(write_only=True)
    message = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise exceptions.ValidationError({'email': [_('User with the given credentials already exists')]})
        return value
    
    def validate_inn(self, value):
        MaxLengthValidator(10, 'Неправильный ИНН')(value)
        MinLengthValidator(8, 'Неправильный ИНН')(value)
        return value

    def validate(self, attrs):
        inn: str = attrs['inn']
        email: str = attrs['email']
        org = inn_check_api_validator(inn)
        if UserToOrganization.objects.filter(org__inn=inn, role=ROLE_OWNER).exists():
            raise exceptions.ValidationError({'org': [_('This organization already using with an other user')]})
        return {
            'email': email,
            'phone': attrs['phone'],
            'org_api': org,
            'inn': inn,
        }
    
    def create(self, validated_data):
        inn: str = validated_data.get('inn')
        org: dict = validated_data.get('org_api')
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        user = User.objects.create_user(email=email, phone=phone)
        org = Organization.objects.create(
            inn=inn,
            address = org['a'],
            name = org['c'],
            ogrn = org['o'],
            kpp = org['p'],
        )
        UserToOrganization.objects.create(
            org=org, user=user, status=STATUS_CHECKING, role=ROLE_OWNER
        )
        token = RefreshToken(self.context['request']).for_user(user)
        return {
            'message': _('Invite created'),
            'access': str(token.access_token),
            'refresh': str(token),
        }
