from core.utils import IAPITestCase


class GroupAppIntegrationTests(IAPITestCase):
    counter = 1

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\n  -------------- Integracyjne testy panelu grup -------------- \n ')
