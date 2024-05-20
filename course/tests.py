from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from course.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        """Создание и авторизация тестового пользователя"""
        self.user = User.objects.create(id=1, email='user@test.ru', password='12345')
        self.client.force_authenticate(user=self.user)
        """Создание тестовых курса и урока"""
        self.course = Course.objects.create(name='test_course', description='test_description')
        self.lesson = Lesson.objects.create(name='test_lesson', description='test_description',
                                            course=self.course, link='https://test.youtube.com/',
                                            owner=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {'name': 'Creating_test', 'description': 'Creating_test',
                'course': self.course.id, 'link': 'https://test.youtube.com/',
                'owner': self.user.id}
        response = self.client.post('/lessons/lesson/create/', data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(name=data['name']).exists())

    def test_retrieve_lesson(self):
        """Тестирование просмотра информации об уроке"""
        path = reverse('course:lesson_get', [self.lesson.id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_update_lesson(self):
        """Тестирование редактирования урока"""
        path = reverse('course:lesson_update', [self.lesson.id])
        data = {'name': 'Updating_test', 'description': 'Updating_test'}
        response = self.client.patch(path, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, data['name'])

    def test_delete_lesson(self):
        """Проверка на права доступа - создан пользователь с правами
           модератора (не владелец урока)"""
        moderator = User.objects.create(id=2, email='moderator@test.ru',
                                        password='12345', role='moderator')
        self.client.force_authenticate(user=moderator)

        path = reverse('course:lesson_delete', [self.lesson.id])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@sky.pro',
            password='test',
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name='test',
            description='test',
            owner=self.user
        )

    def test_create_subscription(self):
        data = {
            'user': self.user.id,
            'course': self.course.id,
        }

        response = self.client.post('/subscription/create/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'подписка добавлена'})

    def test_list_subscription(self):
        response = self.client.get(reverse('course:subscription_list'))
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)
        self.assertEqual(response.json(), {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_delete_subscription(self):
        data = {
            'user': self.user.id,
            'course': self.course.id,
        }

        response = self.client.post('/lessons/subscription/create/', data=data)

        self.assertEqual(
            response.json(),
            {'message': 'подписка добавлена'}
        )
        print(response.json())

        response = self.client.post('/lessons/subscription/create/', data=data)
        self.assertEqual(
            response.json(),
            {'message': 'подписка удалена'}
        )
        print(response.json())
