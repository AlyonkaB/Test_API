from django.urls import path, include

# from db.views import BusList, BusDetail
from db.views import BusViewSet, TripViewSet, FacilityViewSet, OrderViewSer
from rest_framework import routers

router = routers.DefaultRouter()
router.register("facilities", FacilityViewSet)
router.register("buses", BusViewSet)
router.register("trips", TripViewSet)
router.register("orders", OrderViewSer)

# bus_list = BusViewSet.as_view(actions={
#     "get": "list",
#     "post": "create",
# })
# bus_detail = BusViewSet.as_view(actions={
#     "get": "retrieve",
#     "put": "update",
#     "patch": "partial_update",
#     "delete": "destroy",
# })

urlpatterns = [
    # path("buses/", bus_list, name="bus-list"),
    # path("buses/<int:pk>/", bus_detail, name="bus-detail"),
    path("", include(router.urls)),
]

app_name = "db"
