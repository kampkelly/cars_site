from fixtures.all_cars_fixtures import get_all_cars_query, get_all_cars_query_response
from tests.Base import BaseTestCasea


class TestQueryCars(BaseTestCase):
    def test_query_all_cars(self):
        all_cars = self.client.execute(get_all_cars_query)
        self.assertEquals(all_cars, get_all_cars_query_response)
