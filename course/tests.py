from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from course.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        """Создание и авторизация тестового пользователя"""
        self.user = User.objects.create(id=1, email="user@test.ru")
        self.client.force_authenticate(user=self.user)
        """Создание тестовых курса и урока"""
        self.course = Course.objects.create(
            name="test_course", description="test_description"
        )
        self.lesson = Lesson.objects.create(
            name="test_lesson",
            description="test_description",
            course=self.course,
            video_url="https://test.youtube.com/",
            owner=self.user,
        )

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {
            "name": "creating1test",
            "description": "Creating_test",
            "course": self.course.id,
            "video_url": "https://test.youtube.com/",
            "owner": self.user.id,
        }
        response = self.client.post(reverse("course:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(name=data["name"]).exists())

    def test_retrieve_lesson(self):
        """Тестирование просмотра информации об уроке"""
        path = reverse("course:lesson_get", kwargs={"pk": self.lesson.pk})

        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.lesson.name)

    def test_retrieve_nonexistent_lesson(self):
        """Тестирование запроса несуществующего урока"""
        nonexistent_lesson_id = 9999  # ID, которого нет в базе данных
        path = reverse('course:lesson_get', args=[nonexistent_lesson_id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_lesson(self):
        """Тестирование редактирования урока"""
        path = reverse("course:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {"name": "updating1test", "description": "Updating_test"}
        response = self.client.patch(path, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, data["name"])

    def test_delete_lesson(self):
        """Проверка на права доступа - создан пользователь с правами
        модератора (не владелец урока)"""
        moderator = User.objects.create(
            id=2, email="moderator@test.ru", password="12345", role="moderator"
        )
        self.client.force_authenticate(user=moderator)

        path = reverse("course:lesson_delete", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(path)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test1@test.sky.pro",
            password="123test",
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name="test",
            description="test",
        )

    def test_create_subscription(self):
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }

        url = reverse(
            "course:subscription_create"
        )  # Обратите внимание на использование reverse
        response = self.client.post(url, data=data, format="json")

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка типа ответа
        self.assertEqual(response.headers["Content-Type"], "application/json")

        # Печать JSON-ответа для отладки
        print(response.json())
        self.assertEqual(response.json(), {"message": "подписка добавлена"})


    def test_list_subscription(self):
        response = self.client.get(reverse("course:subscription_list"))
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)
        self.assertEqual(
            response.json(), {"count": 0, "next": None, "previous": None, "results": []}
        )

    def test_delete_subscription(self):
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        # Создание подписки
        response = self.client.post(reverse("course:subscription_create"), data=data)
        self.assertEqual(response.json(), {"message": "подписка добавлена"})
        print(response.json())

        # Удаление подписки
        response = self.client.delete(reverse("course:subscription_delete"), data=data)
        self.assertEqual(response.json(), {"message": "подписка удалена"})
        print(response.json())

