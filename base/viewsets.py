from rest_framework import mixins, viewsets


class ListAndCreateViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ListCreateAndRetrieveViewSet(
    mixins.RetrieveModelMixin,
    ListAndCreateViewSet,
):
    pass
