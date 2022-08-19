from authapp.models import ShopUserProfile
from django.utils import timezone
from datetime import datetime
from social_core.exceptions import AuthForbidden
import requests
from typing import OrderedDict
from urllib.parse import urlunparse, urlencode


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    #  api_url = f"https://api.vk.com/method/users.get?fields=bdate,sex,about,photo_max_orig&access_token={response['access_token']}&v=5.131"
    # api_url = https://api.vk.com/method/users.get?fields=bdate%2Csex%2Cabout%2Cphoto_max_orig&access_token=vk1.a.ZqttlnMKLAkhIMV8gjlgIovR_4Wx0SMPn4jfn3x1id1SbhgpNUkhukJaqT62rewyt5iSwLiq54wUA8W00ZclCB1s0bDhjA4TrCPg1-NCtfd-sloKixkX_LZk0K3ZdnE7dJ1oJUXzZ7CVGfX01UDfL2vjbRTHj83p6rryqI3fSZ3-kXcpcDASQ8hlfrZVU6kx&v=5.131

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_max_orig')),
                                                access_token=response['access_token'],
                                                v='5.131')),
                          None
                          ))

    print(f'api_url={api_url}')
    resp = requests.get(api_url)
    print(f'resp = {resp.json()}')

    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex']:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    # if 'bdate' in data and data['bdate']:
    #     bdate = datetime.strptime(data['bdate'], '%d%m%Y').date()
    #     age = timezone.now().date().year - bdate.year
    #     if age < 18:
    #         user.delete()
    #         raise AuthForbidden('socail_core.backends.vk.VKOAuth2')

    if data['photo_max_orig']:
        photo = requests.get(data['photo_max_orig'])
        if photo.status_code == 200:
            photo_name = f'users_avatars/{user.pk}.jpg'
            with open(f'media/{photo_name}', 'wb') as avatar:
                avatar.write(photo.content)
                user.avatar = photo_name

    user.save()
