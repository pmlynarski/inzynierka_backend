import json

from django.urls import reverse

from core.tests_utils import IAPITestCase


class PostsAppIntegrationTests(IAPITestCase):
    counter = 1
    base_data = {}
    return_data = {}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\n  -------------- Integracyjne testy panelu postów -------------- \n ')

    @classmethod
    def setUpClassData(cls):
        super().setUpTestData()
        cls.base_data = {
            'name': 'TestName'
        }

    def test_groups_posts_list(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.get(reverse('post-group_post_list', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('post-group_post_list', kwargs={'id': 9}))
        self.assertEqual(response.status_code, 404)

    def test_user_posts_list(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.get(reverse('post-user_post_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.post(reverse('post-create_post', kwargs={'id': 1}), {'content': 'Testowy content'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('post-create_post', kwargs={'id': 99}), {'content': 'Testowy content'})
        self.assertEqual(response.status_code, 404)

    def test_get_post(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.get(reverse('post-post_details', kwargs={'id': 1}))
        self.assertEqual(json.loads(response.content)['content'], 'Testing post')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('post-post_details', kwargs={'id': 77}))
        self.assertEqual(response.status_code, 404)

    def test_update_post(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.put(reverse('post-post_update', kwargs={'id': 2}), data={'content': 'changed content'})
        self.assertEqual(json.loads(response.content).get('content'), 'changed content')
        self.assertEqual(response.status_code, 200)
        response = self.client.put(reverse('post-post_update', kwargs={'id': 99}), data={'content': 'changed content'})
        self.assertEqual(response.status_code, 404)

    def test_delete_post(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.delete(reverse('post-post_delete', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 200)

    def test_add_comment(self):
        self.client.force_authenticate(self.test_user)
        response = self.client.post(reverse('post-create_comment', kwargs={'id': 1}),
                                    data={'content': 'Test comment'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('post-create_comment', kwargs={'id': 88}),
                                    data={'content': 'Test comment'})
        self.assertEqual(response.status_code, 404)

    def test_update_comment(self):
        content = 'edited content'
        self.client.force_authenticate(self.test_lecturer)
        response = self.client.put(reverse('post-comment_update', kwargs={'id': 1}),
                                   data={'content': content})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content).get('content'), content)
        response = self.client.put(reverse('post-comment_update', kwargs={'id': 99}),
                                   data={'content': content})
        self.assertEqual(response.status_code, 404)

    def test_delete_comment(self):
        self.client.force_authenticate(self.test_lecturer)
        response = self.client.delete(reverse('post-comment_delete', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(reverse('post-comment_delete', kwargs={'id': 99}))
        self.assertEqual(response.status_code, 404)

