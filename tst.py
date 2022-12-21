from web.models import UserExtra
from django.contrib.auth.models import User

UserExtra.objects.create(User.objects.get(username = 'root'), )

