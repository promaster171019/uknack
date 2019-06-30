import urllib
import requests
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from PIL import Image
from io import BytesIO, FileIO
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from .models import KnackUser
from .serializers import AuthTokenSerializer


def associate_by_email(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = KnackUser.objects.get(email=email)
    except:
        pass
    return kwargs


# User details pipeline
def user_details(strategy, details, response, user=None, *args, **kwargs):

    serializer_class = AuthTokenSerializer
    """Update user details using data from provider."""
    if user:
        email, password = '', ''
        password = response['access_token']
        email = response['email']
        data = {'email': email, 'password': password}
        print(email)
        print(password)
        if kwargs['backend'].name == 'facebook':
            try:
                knack_user = KnackUser.objects.get(email=data['email'])
            except ObjectDoesNotExist:
                knack_user = KnackUser.objects.create_user(data['email'], data['password'])

            url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(requests.get(url).content)
            img_temp.flush()

            # FileIO(io)
            knack_user.picture.save('profile_pic_{}.jpg'.format(user.pk), File(img_temp))
            print(knack_user.id)
            serializer = serializer_class(data=data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
