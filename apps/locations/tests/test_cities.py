import pytest

from apps.locations.models import City

pytestmark = pytest.mark.django_db


@pytest.fixture
def cities():
    City.objects.create(name="Луцьк", slug="lutsk", is_default=True, order=1)
    City.objects.create(name="Львів", slug="lviv", order=2)
    City.objects.create(name="Одеса", slug="odesa", order=3, is_active=False)


def test_list_returns_active_only(client, cities):
    names = [c["name"] for c in client.get("/api/cities/").json()]
    assert names == ["Луцьк", "Львів"]


def test_detail_by_slug(client, cities):
    assert client.get("/api/cities/lutsk/").json()["is_default"] is True


def test_only_one_default(cities):
    lviv = City.objects.get(slug="lviv")
    lviv.is_default = True
    lviv.save()
    assert City.objects.filter(is_default=True).count() == 1
