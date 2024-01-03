import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import MembershipLevel
from .managers import MemberManager, UserManager, OrganizationManager

from .utils import membership_invitation_default


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=False, editable=False, unique=True, db_index=True,
                            default=uuid.uuid4, verbose_name='UUID', help_text='Unique identifier')
    objects = UserManager()

    # if you dont need group, uncomment this
    # groups = None
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def is_member_of_organization(self, organization: 'Organization'):
        return self.memberships.filter(organization=organization)

    @property
    def organizations(self):
        return self.memberships.annotate()  # TODO


class Organization(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    icon = models.URLField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    objects = OrganizationManager()


class Member(models.Model):
    organization = models.ForeignKey(
        to='identity.Organization',
        on_delete=models.CASCADE,
        related_name='members',
    )

    user = models.ForeignKey(
        to='identity.User',
        on_delete=models.CASCADE,
        related_name='memberships',
    )

    is_accepted = models.BooleanField(
        default=False, db_index=True,
        help_text="Whether the user has accepted the invitation.",
    )

    invitation = models.TextField(
        default=membership_invitation_default,
        help_text="Invitation token",
        unique=True,
        db_index=True,
    )

    level = models.PositiveSmallIntegerField(
        choices=MembershipLevel.choices,
        default=MembershipLevel.MEMBER,
    )

    expiration = models.DateTimeField(null=True, blank=True)

    objects = MemberManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization', 'user'], name='unique_membership')
        ]

        permissions = [
            ('can_invite', 'Can invite members'),
            ('can_remove', 'Can remove members from organization'),
            ('can_change_level', 'Can change membership level'),
        ]
