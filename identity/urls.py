from rest_framework_nested import routers
from django.urls import path, include

from .views import OrganizationView, MemberView

router = routers.SimpleRouter()
router.register(r'organizations', OrganizationView)

organizations_router = routers.NestedSimpleRouter(router, r'organizations', lookup='organization')
organizations_router.register(r'members', MemberView, basename='organization-members')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(organizations_router.urls)),
]
