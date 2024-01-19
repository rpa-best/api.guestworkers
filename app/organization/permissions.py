from .models import UserToOrganization, ROLE_CLIENT, ROLE_OWNER, ROLE_WORKER, STATUS_CHECKING


def has_permission(org_inn: str, user, roles: list[str]):
    kwargs = {
        "role__in": roles,
    }
    if org_inn:
        kwargs["org_id"] = org_inn
    if isinstance(user, str):
        kwargs["user__email"] = user
    elif isinstance(user, int):
        kwargs["user_id"] = user
    return UserToOrganization.objects.exclude(status=STATUS_CHECKING).filter(**kwargs)


def has_client_permission(org_inn, user):
    return has_permission(org_inn, user, [ROLE_CLIENT])


def has_worker_permission(org_inn, user):
    return has_permission(org_inn, user, [ROLE_WORKER])


def has_owner_permission(org_inn, user):
    return has_permission(org_inn, user, [ROLE_OWNER])
