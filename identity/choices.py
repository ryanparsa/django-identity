from django.db import models


class MembershipLevel(models.IntegerChoices):
    OWNER = 1, 'Owner'
    ADMIN = 2, 'Admin'
    MEMBER = 3, 'Member'
    REPORTER = 4, 'Reporter'
