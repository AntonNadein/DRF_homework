from rest_framework.serializers import ValidationError


class VIdeoURLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # pattern = r'^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}([\/\w \.-]*)*\/?$'
        # reg = re.compile(pattern)
        # tmp_val = dict(value).get(self.field)
        # if bool(reg.match(tmp_val)) and not bool("youtube.com" in tmp_val):
        #     raise ValidationError('VIdeo URL is not ok')
        tmp_val = dict(value).get(self.field)
        if not bool("youtube.com" in tmp_val):
            raise ValidationError("VIdeo URL is not ok")
