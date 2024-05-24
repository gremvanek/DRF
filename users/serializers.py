from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer
from course.serializers import CourseSerializer, LessonSerializer
from users.models import User, Payment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


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

    # /////////////////////////////////////////
    # Добавим стерилизаторы для связанных моделей (если они есть)
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    # /////////////////////////////////////////

    url_for_pay = SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        # //////////////////////
        fields = (
            "is_paid",
            "date_of_payment",
            "payment_sum",
            "payment_method",
            "url_for_pay",
            "session",
            "course",
            "lesson",
            "user",
        )

    @staticmethod
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        session = obj.retrieve_payment_session()
        if session.payment_status == "paid" and session.status == "complete":
            obj.is_paid = True
            obj.save()
        self.check_object_permissions(self.request, obj)
        return obj


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
