from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class LoginTest(APITestCase):

    def registration(self, username, password):
        res = self.client.post('/user/registration/', data={"username": username,
                                               "password": password})
        self.assertTrue(status.is_success(res.status_code))
        return self.login(username, password)

    def login(self, username, password):
        res = self.client.post('/user/get_token/', data={"username": username,
                                               "password": password})
        self.assertTrue(status.is_success(res.status_code))
        token = 'Token ' + res.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='')


class TestUser(LoginTest):

    def tearDown(self):
        get_user_model().objects.all().delete()

    def test_registration(self):
        User = get_user_model()
        password, username = User.objects.make_random_password(length=3), 'Test'
        res = self.client.post('/user/registration/',
                               data={'password': password, 'username': username})
        self.assertTrue(status.is_client_error(res.status_code))
        self.assertTrue([e for e in res.data['non_field_errors'] if e.code == 'password_too_short'])

        password = User.objects.make_random_password(length=12),
        res = self.client.post('/user/registration/', data={'password': password, 'username': username})
        self.assertTrue(status.is_success(res.status_code))

    def test_validation(self):
        User = get_user_model()
        password, username = User.objects.make_random_password(length=12), 'Test'
        phone = User.objects.make_random_password(length=12)
        res = self.client.post('/user/registration/',
                               data={'password': password, 'username': username,'phone': phone})
        self.assertTrue(status.is_client_error(res.status_code))
        self.assertTrue(res.data['phone'][0].code == 'invalid')

        phone = '89094363312'
        res = self.client.post('/user/registration/', data={'password': password, 'username': username,
                                               'phone': phone})

        self.assertTrue(status.is_success(res.status_code))


    def test_perm(self):
        User = get_user_model()
        password, username = User.objects.make_random_password(length=12), 'Test'
        res = self.client.post('/user/registration/', data={'password': password, 'username': username})
        id_ = res.data["id"]
        res = self.client.get(f'/user/{id_}/')
        self.assertTrue(res.status_code == status.HTTP_401_UNAUTHORIZED)

        self.login(username, password)
        res = self.client.get(f'/user/{id_}/')
        self.assertTrue(status.is_success(res.status_code))

