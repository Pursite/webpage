from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.product_create_serializer import ProductCreateSerializer


class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductCreateSerializer
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Permission Denied"}, status=403)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
