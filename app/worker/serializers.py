import datetime
import pandas as pd
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from organization.models import Organization, UserToOrganization, ROLE_WORKER, ROLE_CLIENT, ROLE_OWNER, STATUS_DONE
from organization.permissions import has_permission
from organization.serializers import OrganizationShortSerializer
from oauth.serializers import UserShortSerializer
from .models import WorkerDoc, DocType, UPLOAD_KWARGS, DEFAULT_DOC_TYPES, UPLOAD_KWARGS_PASSPORT

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
                'new': None,
                'user': {},
                'docs': []
            }
            passport = worker.get(UPLOAD_KWARGS_PASSPORT)
            if not passport:
                continue
            try:
                user = UserShortSerializer(User.objects.get(passport=passport)).data
            except User.DoesNotExist:
                user = {}
                for key, value, default in UPLOAD_KWARGS:
                    user[key] = worker.get(value)
            rworker["user"] = user
            for doc_type in DEFAULT_DOC_TYPES:
                value = worker.get(doc_type["name"])
                rworker['docs'].append(
                    {
                        "type": doc_type["slug"],
                        "name": doc_type["name"],
                        "expired_date": datetime.datetime.strptime(value, "%d.%m.%Y").date().strftime("%Y-%m-%d") if value else None
                    }
                )
            if not user.get("id"):
                rworker["new"] = True
            else:
                rworker["new"] = not UserToOrganization.objects.filter(org=org, user_id=user["id"]).exists()
            results.append(rworker)
        return {
            "org":org,
            "results": results
        }
    
    def create(self, validated_data):
        return validated_data


class UploadPerformWorkerDocSerializer(serializers.Serializer):
    type = serializers.SlugField()
    name = serializers.CharField()
    expired_date = serializers.DateField()


class UploadPerformWorkerSerializer(serializers.Serializer):
    docs = UploadPerformWorkerDocSerializer(many=True)
    user = UserShortSerializer()


class UploadPerformSerializer(serializers.Serializer):
    results = UploadPerformWorkerSerializer(many=True, write_only=True)
    inn = serializers.SlugRelatedField("inn", queryset=Organization.objects, write_only=True)
    message = serializers.CharField(read_only=True)

    def validate(self, attrs):
        if not has_permission(attrs["org"].inn, self.context["request"].user.id, [ROLE_OWNER, ROLE_CLIENT]):
            raise PermissionDenied({'inn': [_("Not permission to upload this organization")]})
        return attrs
    
    def create(self, validated_data):
        org: Organization = validated_data.get("inn")
        for worker in validated_data.get("results", []):
            try:
                user = User.objects.get(passport=worker["user"].get("passport"))
            except User.DoesNotExist:
                user = User.objects.create_user(
                    _send_email=False,
                    **worker["user"],
                )
            for doc in worker["docs"]:
                WorkerDoc.objects.update_or_create(
                    {
                        "type_id": doc.get("type"),
                        "user": user,
                        "expired_date": doc.get("expired_date")
                    }, user=user, type_id=doc.get("type")
                )
            UserToOrganization.objects.get_or_create(
            {
                "org": org,
                "user": user,
                "status": STATUS_DONE,
                "role": ROLE_WORKER,
            }, org=org, user=user
        )
        return {
            "message": _("Uploaded success")
        }