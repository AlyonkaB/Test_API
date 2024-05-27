from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from db.models import Bus, Facility
from db.serializers import BusListSerializer, BusDetailSerializer

BUS_URL = reverse("db:bus-list")


def detail_url(x_id: int):
    return reverse("db:bus-detail", args=(x_id,))


def sample_bus(**params) -> Bus:
    defaults = {"info": "AA12345AA",
                "num_seat": 50}
    defaults.update(params)
    return Bus.objects.create(**defaults)


class UnauthenticatedBusApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_require(self) -> None:
        res = self.client.get(BUS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBusApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password_1234"
        )
        self.client.force_authenticate(self.user)

    def test_bus_lists(self) -> None:
        sample_bus()

        bus_with_facility = sample_bus()
        facility_1 = Facility.objects.create(name="Wifi")
        facility_2 = Facility.objects.create(name="TV")

        bus_with_facility.facility.add(facility_1, facility_2)

        res = self.client.get(BUS_URL)

        buses = Bus.objects.all()
        serializer = BusListSerializer(buses, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_bus_filter_facility(self) -> None:
        bus_with_facility_1 = sample_bus(info="AA1234QW")
        bus_with_facility_2 = sample_bus(info="LL1234KL")

        facility_1 = Facility.objects.create(name="Wifi")
        facility_2 = Facility.objects.create(name="TV")

        bus_with_facility_1.facility.add(facility_1)
        bus_with_facility_2.facility.add(facility_2)

        res = self.client.get(
            BUS_URL,
            {"facility": f"{facility_1.id}, {facility_2.id}"}
        )

        serializer_with_facility_1 = BusListSerializer(bus_with_facility_1)
        serializer_with_facility_2 = BusListSerializer(bus_with_facility_2)

        self.assertIn(serializer_with_facility_1.data, res.data)
        self.assertIn(serializer_with_facility_2.data, res.data)


    def test_retrieve_bus_detail(self):
        bus = sample_bus()
        bus.facility.add(Facility.objects.create(name="WC"))
        url = detail_url(bus.id)
        res = self.client.get(url)
        serializer = BusDetailSerializer(bus)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_bus_forbidden(self):
        payload = {
            "info": "AA12345AA",
            "num_seat": 50}
        res = self.client.post(BUS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
