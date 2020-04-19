from rest_framework.test import APIClient, APITestCase

from users.models import User


class IAPITestCase(APITestCase):
    counter = 1

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.test_user = User.objects.create(email='foo@foo.foo', first_name='Foo', last_name='Bar',
                                            password='1234567890', active=True)
        cls.test_inactive_user = User.objects.create(email='bar@bar.bar', first_name='Bar', last_name='Foo',
                                                     password='1234567890')
        cls.test_admin = User.objects.create_superuser(email='admin@admin.admin', first_name='Admin',
                                                       last_name='Tester',
                                                       password='1234567890')

    def setUp(self):
        print('\n  -------------- Test nr {}-------------- \n '.format(self.counter))

    @classmethod
    def tearDown(cls):
        cls.counter += 1
