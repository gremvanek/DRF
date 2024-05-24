import re
from rest_framework.serializers import ValidationError

from course.models import Subscription


class TitleValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r"^[a-zA-Z0-9\.\-\ ]+$")
        tmp_val = dict(value).get(self.field)
        if not bool(reg.match(tmp_val)):
            raise ValidationError("Title is not ok")


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        links = value.get(self.field, [])
        for link in links:
            if not self.is_youtube_link(link):
                raise ValidationError("Only YouTube links are allowed")

    @staticmethod
    def is_youtube_link(link):
        youtube_regex = (
            r"(https?://)?(www\.)?"
            r"(youtube|youtu|youtube-nocookie)\.(com|be)/"
            r"(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
        )
        return re.match(youtube_regex, link)


class SubscriptionValidator:
    def __call__(self, attrs):
        user = attrs.get("user")
        course = attrs.get("course")
        owner = attrs.get("owner")
        if (
            user
            and course
            and owner
            and Subscription.objects.filter(
                user=user, course=course, owner=owner
            ).exists()
        ):
            raise ValidationError("Вы уже подписаны на этот курс")
