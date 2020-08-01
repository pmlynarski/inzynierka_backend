from django.urls import reverse

from core.tests_utils import IAPITestCase


class MessageThreadIntegrationTests(IAPITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\n  -------------- Integracyjne testy panelu wiadomości -------------- \n ')

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test__creating_messages(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.post(reverse('thread-messages', kwargs={'id': 3}), data={'content': 'Testowy content'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('thread-messages', kwargs={'id': 1}), data={'content': 'Testowy content'})
        self.assertEqual(response.status_code, 406)
        response = self.client.post(reverse('thread-messages', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 406)

    def test__getting_messages(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.get(reverse('thread-messages', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('thread-messages', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 406)

