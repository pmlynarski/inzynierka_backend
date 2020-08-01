import random
from unittest import TestCase

from rest_framework.permissions import IsAuthenticated

from core.permissions import IsOwnerOrIsMember, IsOwner, IsOwnerOrIsModerator, set_basic_permissions, \
    IsLecturerOrIsAdmin
from core.responses import response406, response200, response404


class PermissionSetTestCase(TestCase):
    counter = 1

    @classmethod
    def setUpClass(cls):
        print('\n----------------Tests of set_basic_permissions method-----------------\n')
        cls.action_types = [
            {'class': IsOwnerOrIsMember,
             'values': ['groups_posts_list', 'create_post', 'get_post', 'create_comment', 'get_comment']},
            {'class': IsOwner, 'values': ['update_post', 'update_comment']},
            {'class': IsOwnerOrIsModerator, 'values': ['delete_post', 'delete_comment']},
            {'class': IsLecturerOrIsAdmin, 'values': ['cokolwiek']}
        ]

    def setUp(self):
        print('\n  -------------- Test nr {}-------------- \n '.format(self.counter))

    @classmethod
    def tearDown(cls):
        cls.counter += 1

    def test_owner_or_member_permissions(self):
        check = set_basic_permissions(random.choice(self.action_types[0]['values']), self.action_types)
        self.assertEqual(check, [IsAuthenticated, IsOwnerOrIsMember])

    def test_owner_permissions(self):
        check = set_basic_permissions(random.choice(self.action_types[1]['values']), self.action_types)
        self.assertEqual(check, [IsAuthenticated, IsOwner])

    def test_owner_or_moderator_permissions(self):
        check = set_basic_permissions(random.choice(self.action_types[2]['values']), self.action_types)
        self.assertEqual(check, [IsAuthenticated, IsOwnerOrIsModerator])

    def test_admin_or_lecturer_permissions(self):
        check = set_basic_permissions(random.choice(self.action_types[3]['values']), self.action_types)
        self.assertEqual(check, [IsAuthenticated, IsLecturerOrIsAdmin])


class CustomResponsesTestCase(TestCase):
    counter = 1

    def setUp(self):
        print('\n  -------------- Test nr {}-------------- \n '.format(self.counter))

    @classmethod
    def tearDown(cls):
        cls.counter += 1

    @classmethod
    def setUpClass(cls):
        print('\n----------------------Tests of responses methods----------------------\n')

    def test_response406_method(self):
        result = response406({})
        self.assertEqual(result.status_code, 406)
        self.assertEqual(result.data, {})

    def test_response200_method(self):
        result = response200({})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, {})

    def test_response404_method(self):
        result = response404('Test')
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.data, {'message': 'Test nie znaleziono'})
