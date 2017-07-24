from django.utils import timezone


class Error(object):
    def __init__(self, field, msg):
        self.field = field
        self.message = msg
        self.created_at = timezone.now()

    def __str__(self):
        return '{}\t{}\t{}'.format(self.created_at, self.field, self.message)
