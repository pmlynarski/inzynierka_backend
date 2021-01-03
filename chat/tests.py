import json

from django.urls import reverse

from chat.models import Thread
from core.tests_utils import IAPITestCase


class MessageThreadIntegrationTests(IAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\n  -------------- Integracyjne testy panelu wiadomości -------------- \n ')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_creating_or_getting_thread_valid(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.get(reverse('thread-messages', kwargs={'id': self.test_admin.id}))
        self.assertEqual(response.status_code, 200)

    def test_creating_or_getting_thread_invalid(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.get(reverse('thread-messages', kwargs={'id': self.test_user.id}))
        self.assertEqual(response.status_code, 406)

    def test_fetching_threads_list(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.get(reverse('thread-messages-list'))
        self.assertEqual(json.loads(response.content)['count'], 0)
