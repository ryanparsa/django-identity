import secrets

from django.conf import settings

MEMBERSHIP_INVITATION_TOKEN_LENGTH = getattr(settings, 'MEMBERSHIP_INVITATION_TOKEN_LENGTH', 32)


def membership_invitation_default():
    return secrets.token_hex(MEMBERSHIP_INVITATION_TOKEN_LENGTH)
