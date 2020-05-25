import json

from django.urls import reverse

from core.tests_utils import IAPITestCase
from posts.serializers import CommentSerializer, PostSerializer


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
        response = self.client.get(reverse('post-post_details', kwargs={'pk': 1}))
        self.assertEqual(json.loads(response.content), {'id': 1, 'content': 'Testing post',
                                                        'owner': {'id': 1, 'email': 'foo@foo.foo', 'first_name': 'Foo',
                                                                  'last_name': 'Bar', 'is_admin': False,
                                                                  'is_lecturer': False, 'image': None},
                                                        'group': {'id': 1, 'name': 'Test Group'}, 'image': None,
                                                        'file': None})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('post-post_details', kwargs={'pk': 77}))
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


class PostSerializerUnitTest(IAPITestCase):
    context = {
        'host': 'localhost:8000'
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\n  -------------- Jednostkowe testy serializera postów -------------- \n ')

    @classmethod
    def setUpClassData(cls):
        super().setUpTestData()

    def test_unit_get_owner(self):
        serializer = PostSerializer(self.test_post)
        self.assertEqual(serializer.get_owner(self.test_post),
                         {'id': 1, 'email': 'foo@foo.foo', 'first_name': 'Foo', 'last_name': 'Bar', 'is_admin': False,
                          'is_lecturer': False, 'image': None})

    def test_unit_get_image(self):
        self.test_post.image = 'media/80667875_440098716867149_4273943207747780608_n.jpg'
        serializer = PostSerializer(self.test_post, context=self.context)
        self.assertEqual(serializer.get_image(self.test_post),
                         'http://localhost:8000/media/80667875_440098716867149_4273943207747780608_n.jpg')
        self.test_post.image = None
        self.assertEqual(serializer.get_image(self.test_post), None)

    def test_unit_get_file(self):
        self.test_post.file = 'media/80667875_440098716867149_4273943207747780608_n.jpg'
        serializer = PostSerializer(self.test_post, context=self.context)
        self.assertEqual(serializer.get_file(self.test_post),
                         'http://localhost:8000/media/80667875_440098716867149_4273943207747780608_n.jpg')
        self.test_post.file = None
        self.assertEqual(serializer.get_file(self.test_post), None)

    def test_unit_get_group(self):
        serializer = PostSerializer(self.test_post, context=self.context)
        self.assertEqual(serializer.get_group(self.test_post), {'id': 1, 'name': 'Test Group'})

    def test_unit_get_owner_of_comment(self):
        serializer = CommentSerializer(self.test_comment, context=self.context)
        self.assertEqual(serializer.get_owner(self.test_comment),
                         {'id': 3, 'email': 'foo@lecturer.bar', 'first_name': 'Lecturer', 'last_name': 'Tester',
                          'is_admin': False, 'is_lecturer': True, 'image': None})
