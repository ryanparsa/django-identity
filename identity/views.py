from django.utils.module_loading import import_string
from rest_framework import permissions, response, status, viewsets

from .models import Organization, Member
from .serializer import OrganizationSerializer, MemberSerializer


class MemberView(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_queryset(self):
        return self.queryset.filter(organization=self.kwargs['organization_pk'])


class OrganizationView(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
