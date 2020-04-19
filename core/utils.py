from rest_framework.test import APIClient, APITestCase

from groups.models import Group, PendingMember
from posts.models import Post, Comment
from users.models import User


class IAPITestCase(APITestCase):
    counter = 1

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.test_user = User.objects.create_user(email='foo@foo.foo', first_name='Foo', last_name='Bar',
                                                 password='1234567890', is_active=True)
        cls.test_inactive_user = User.objects.create_user(email='bar@bar.bar', first_name='Bar', last_name='Foo',
                                                          password='1234567890')

        cls.test_lecturer = User.objects.create_lecturer_user(email='foo@lecturer.bar', first_name='Lecturer',
                                                              last_name='Tester', password='anyPassword')

        cls.test_admin = User.objects.create_superuser(email='admin@admin.admin', first_name='Admin',
                                                       last_name='Tester',
                                                       password='1234567890')

        cls.test_moderator = User.objects.create_user(email='bar@foo.bar', first_name='Foo', last_name='Bar',
                                                      password='1234567890', is_active=True)

        cls.test_group = Group.objects.create(name="Test Group", owner=cls.test_lecturer, moderator=cls.test_moderator)
        cls.test_group.members.add(cls.test_user)

        cls.test_post = Post.objects.create(owner=cls.test_user, content="Testing post", group=cls.test_group)

        cls.test_comment = Comment.objects.create(owner=cls.test_lecturer, post=cls.test_post)

        cls.user_to_pending = User.objects.create_user(email='mail@mail.mail', first_name='fsafsa',
                                                       last_name='sadsadsa', password='asdsadsa', is_active=True)

        cls.test_pending_user = PendingMember.objects.create(user=cls.test_user, group=cls.test_group)

    def setUp(self):
        print('\n  -------------- Test nr {}-------------- \n '.format(self.counter))

    @classmethod
    def tearDown(cls):
        cls.counter += 1
