import datetime
import pandas as pd
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from organization.models import Organization, UserToOrganization, ROLE_CLIENT, ROLE_OWNER
from organization.permissions import has_permission
from organization.serializers import OrganizationShortSerializer
from oauth.serializers import UserShortSerializer
from .models import DocType, UPLOAD_KWARGS, DEFAULT_DOC_TYPES, UPLOAD_KWARGS_PASSPORT

User = get_user_model()


def genereate_upload_instance():
    data = []
    user = {}
    for _, key, value in UPLOAD_KWARGS:
        user[key] = value
    for doc_type in DocType.objects.filter(main=True):
        user[doc_type.name] = "01.01.2024"
    data.append(user)


class UploadCheckSerializer(serializers.Serializer):
    inn = serializers.SlugRelatedField("inn", queryset=Organization.objects, write_only=True)
    xlsx = serializers.FileField(validators=[FileExtensionValidator(["xlsx"])], write_only=True)
    results = serializers.ListField(read_only=True)
    org = OrganizationShortSerializer(read_only=True)

    def validate(self, attrs):
        org: Organization = attrs.get("inn")
        if not has_permission(org.inn, self.context["request"].user.id, [ROLE_CLIENT, ROLE_OWNER]):
            raise PermissionDenied({'inn': [_("Not permission to upload this organization")]})
        xlsx = attrs.get("xlsx")
        worker_data = pd.read_excel(xlsx.read()).to_dict(orient="records")
        results = []
        for worker in worker_data:
            rworker = {
                'docs': []
            }
            passport = worker.get(UPLOAD_KWARGS_PASSPORT)
            print(passport, "passport")
            if not passport:
                continue
            try:
                user = UserShortSerializer(User.objects.get(passport=passport)).data
            except User.DoesNotExist:
                user = {}
                for key, value, defult in UPLOAD_KWARGS:
                    user[key] = worker.get(value)
            rworker["user"] = user
            for doc_type in DEFAULT_DOC_TYPES:
                value = worker.get(doc_type["name"])
                rworker['docs'].append(
                    {
                        "type": doc_type["slug"],
                        "expired_date": datetime.datetime.strptime(value, "%d.%m.%Y") if value else None
                    }
                )
            if not user.get("id"):
                rworker["new"] = False
            else:
                rworker["new"] = not UserToOrganization.objects.filter(org=org, user_id=user["id"]).exists()
            results.append(rworker)
        return {
            "org":org,
            "results": results
        }
    
    def create(self, validated_data):
        return validated_data
