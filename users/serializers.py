from django.contrib.auth import get_user_model
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer
from course.serializers import CourseSerializer, LessonSerializer
from users.models import User, Payment


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone', 'city', 'avatar', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


# class PaymentCreateSerializer(ModelSerializer):
#     lesson = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Lesson.objects.all(),
#         allow_null=True,
#         required=False,
#     )
#     user = serializers.SlugRelatedField(slug_field="email", queryset=User.objects.all())
#
#     date_of_payment
#
#     class Meta:
#         model = Payment
#         fields = (
#             "session",
#             "course",
#             "lesson",
#             "user",
#             "payment_sum",
#             "payment_method"
#


class PaymentRetrieveSerializer(ModelSerializer):
    """Serializer for retrieving a Payment"""

    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    url_for_pay = SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "is_paid",
            "payment_date",
            "payment_sum",
            "payment_method",
            "url_for_pay",
            "session_id",
            "course",
            "lesson",
            "user",
        )

    def get_url_for_pay(self, obj):
        return obj.link if obj.link else ""


class UserProfileSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar", "payments"]


class UserPasswordSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
