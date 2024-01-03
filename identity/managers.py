import datetime

from django.db import models

from django.utils import timezone

from django.contrib.auth.models import UserManager as BaseUserManager


class UserQuerySet(models.QuerySet):
    pass


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    pass


class OrganizationQuerySet(models.QuerySet):
    pass


class OrganizationManager(models.Manager.from_queryset(OrganizationQuerySet)):
    pass


class MemberQuerySet(models.QuerySet):
    def expired(self, date: datetime.date = None):
        if date is None:
            date = timezone.now().today()
        return self.filter(expiration__lte=date)


class MemberManager(models.Manager.from_queryset(MemberQuerySet)):
    pass
