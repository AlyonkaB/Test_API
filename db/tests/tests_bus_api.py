from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


BUS_URL = reverse("db:bus-list")


class UnauthenticatedBusApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_require(self) -> None:
        res = self.client.get(BUS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
