from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from lib.pagination import StandardPagePagination
from product.models import Product
from product.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardPagePagination

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username')

        if username:
            qs = qs.filter(user__username=username)
        return qs

    def list(self, request, *args, **kwargs):
        pk = request.query_params.get("pk")
        if pk:
            obj = get_object_or_404(self.get_queryset(), pk=pk)
            serializer = self.get_serializer(obj)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        pk = request.query_params.get("pk")
        product = get_object_or_404(Product, pk=pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    def perform_create(self, serializer):
        username = self.request.query_params.get('username')
        if not username:
            raise ValidationError({"error": "username is required"})

        user = User.objects.get(username=username)
        serializer.save(user=user)