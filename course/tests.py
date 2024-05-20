from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(id=1, email='user@test.ru', password='12345')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='modified_test_course', description='modified_test_description')
        self.lesson = Lesson.objects.create(title='modified_test_lesson', description='modified_test_description',
                                            course=self.course, link='https://test.youtube.com/',
                                            owner=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {'title': 'Creating_modified_test', 'description': 'Creating_modified_test',
                'course': self.course.id, 'link': 'https://test.youtube.com/',
                'owner': self.user.id}
        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title=data['title']).exists())

    def test_retrieve_lesson(self):
        """Тестирование просмотра информации об уроке"""
        path = reverse('learning:modified_lesson_get', [self.lesson.id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        """Тестирование редактирования урока"""
        path = reverse('learning:modified_lesson_update', [self.lesson.id])
        data = {'title': 'Updating_modified_test', 'description': 'Updating_modified_test'}
        response = self.client.patch(path, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, data['title'])

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        moderator = User.objects.create(id=2, email='moderator@test.ru',
                                        password='12345', role='moderator')
        self.client.force_authenticate(user=moderator)

        path = reverse('learning:modified_lesson_delete', [self.lesson.id])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
