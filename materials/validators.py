from rest_framework.serializers import ValidationError


class VideoURLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not isinstance(value, str) or "youtube.com" not in value:
            raise ValidationError("Ссылка должна вести на youtube.com")
