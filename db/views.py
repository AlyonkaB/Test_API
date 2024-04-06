# from django.http import Http404

# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets

from db.models import Bus, Trip, Facility, Order
from db.serializers import (BusSerializer,
                            TripSerializer,
                            TripListSerializer,
                            BusListSerializer,
                            FacilitySerializer,
                            BusDetailSerializer, TripDetailSerializer, OrderSerializer
                            )


# _____________func.base view_______@api_view______________________________________

# @api_view(["GET", "POST"])
# def bus_list(request):
#     if request.method == "GET":
#         buses = Bus.objects.all()
#         serializer = BusSerializer(buses, many=True)
#         return JsonResponse(serializer.data, status=200, safe=False)
#     if request.method == "POST":
#         serializer = BusSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

# ____________class base view__________APIView__________________________________________
# class ModelList(APIView):
#     def get(self, request):
#         buses = Bus.objects.all()
#         serializer = BusSerializer(buses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = BusSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
#
# class ModelDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Bus.objects.get(pk=pk)
#         except Bus.DoesNotExist:
#             raise Http404
#
#     def get(self,request, pk):
#         bus = self.get_object(pk)
#         serializer = BusSerializer(bus)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         bus = self.get_object(pk)
#         serializer = BusSerializer(bus, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(request.data, status=status.HTTP_201_CREATED)
#
#     def delete(self, request, pk):
#         bus = self.get_object(pk)
#         bus.delete()
#         return Response(request.data, status=status.HTTP_200_OK)


# _________GENERIC API View, MIXIN_______________________________________________

# class BusList(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class BusDetail(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# ___________________generic VIEW______________________________________________

# class BusList(generics.ListCreateAPIView):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#
#
# class BusDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer

# ______________________ViewSets________GenericViewSet________________________________________


# class BusViewSet(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet,
# ):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer

# ___________________________ModelViewSet_________________________________________
class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("facility")
        return queryset
    def get_serializer_class(self):
        if self.action == "list":
            return BusListSerializer
        if self.action == "retrieve":
            return BusDetailSerializer
        return BusSerializer


class TripViewSet(viewsets.ModelViewSet):
    # queryset = Trip.objects.all().select_related("bus")  або перевизначаємо метод get_queryset
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("bus")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TripDetailSerializer
        if self.action == "list":
            return TripListSerializer
        return TripSerializer


class OrderViewSer(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)