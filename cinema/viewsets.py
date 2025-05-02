from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from cinema.models import Order
from cinema.serializers import OrderSerializer, OrderListSerializer
from cinema.pagination import OrderPagination


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


class OrderViewSet(ListAndCreateViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__movie_session__movie", "tickets__movie_session__cinema_hall"
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
