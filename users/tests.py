import json

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserAppIntegrationTest(APITestCase):
    counter = 1

    @classmethod
    def setUpClass(cls):
        super(UserAppIntegrationTest, cls).setUpClass()
        print('\n  -------------- Integracyjne testy panelu użytkownika -------------- \n ')

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

        cls.basic_data = {'password': 'testPassword',
                          'first_name': 'FooBar',
                          'last_name': 'BarrFoo'}

    def setUp(self):
        print('\n  -------------- Test nr {}-------------- \n '.format(self.counter))

    @classmethod
    def tearDown(cls):
        cls.counter += 1

    def test_register_endpoint_proper_data(self):
        data = {
            'email': 'testEmail@email.com',
            **self.basic_data
        }
        response = self.client.post(reverse('user-register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'email': 'testEmail@email.com',
                                                        'first_name': 'FooBar',
                                                        'id': 4,
                                                        'is_admin': False,
                                                        'is_lecturer': False,
                                                        'last_name': 'BarrFoo'})

    def test_register_endpoint_invalid_data(self):
        data = {
            'email': 'wrong_email',
            **self.basic_data
        }
        response = self.client.post(reverse('user-register'), data=data)
        self.assertEqual(response.status_code, 406)
        self.assertEqual(json.loads(response.content), {'email': ['Podaj poprawny adres e-mail.']})

    def test_update_profile_valid_data(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.put(reverse('user-update'), data=self.basic_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content),
                         {'id': 1, 'email': 'foo@foo.foo', 'first_name': 'FooBar', 'last_name': 'BarrFoo',
                          'is_admin': False, 'is_lecturer': False})

    def test_update_profile_invalid_data(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.put(reverse('user-update'), data={**self.basic_data, 'email': ''})
        self.assertEqual(response.status_code, 406)
        self.assertEqual(json.loads(response.content), {'email': ['To pole nie może być puste.']})

    def test_update_profile_unauthorized(self):
        response = self.client.put(reverse('user-update'), data={**self.basic_data, 'email': ''})
        self.assertEqual(response.status_code, 401)

    def test_accept_user_valid(self):
        self.client.force_authenticate(self.test_admin)
        response = self.client.post(reverse('user-accept_user', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'message': 'Pomyślnie aktywowano użytkownika'})

    def test_accept_user_no_permission(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.post(reverse('user-accept_user', kwargs={'id': '2'}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content), {'detail': 'Musisz być administratorem by wykonać tą akcję'})

    def test_unaccepted_users_valid(self):
        self.client.force_authenticate(self.test_admin)
        response = self.client.get(reverse('user-unaccepted_users'))
        self.assertEqual(len(json.loads(response.content)), 1)
        self.assertEqual(response.status_code, 200)

    def test_unaccepted_users_empty_list(self):
        self.test_inactive_user.delete()
        self.client.force_authenticate(self.test_admin)
        response = self.client.get(reverse('user-unaccepted_users'))
        self.assertEqual(response.status_code, 404)

    def test_unaccepted_users_no_access(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.get(reverse('user-unaccepted_users'))
        self.assertEqual(response.status_code, 403)
