from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
    List of all users

    Returns information for all users.

    retrieve:
    Retrieve user profile

    Returns information for current user.

    update:
    Update user profile

    Changes information for current user.

    partial_update:
    Partial update user profile

    Changes partly information for current user.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
