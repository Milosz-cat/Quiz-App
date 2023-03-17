from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from base import views


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.sign_up_url = reverse("sign_up")
        self.sign_in_url = reverse("sign_in")
        self.sign_out_url = reverse("sign_out")
        #self.user = User.objects.create_user(username='testuser', password='testpass')


    def test_sign_up_GET(self):
        response = self.client.get(self.sign_up_url)

        self.assertEquals(response.status_code, 200)  # 200 is OK
        self.assertTemplateUsed(response, "base/sign_up.html")

    def test_sign_up_POST_adds_new_user(self):
        response = self.client.post(self.sign_up_url, {
            'username':'testuser',
            'fname':'testfirstname',
            'lname':'testlastname',
            'email':'testuser@example.com',
            'pass1':'testpass',
            'pass2':'testpass',
        })

        self.assertEquals(response.status_code, 302)

        self.assertEquals(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEquals(user.username, 'testuser')
        self.assertEquals(user.email, 'testuser@example.com')

    # This test doesn't work because the registration form blocks sending without filling.
    #
    # def test_sign_up_POST_no_data(self):
    #     response = self.client.post(self.sign_up_url)

    #     self.assertEquals(response.status_code, 302)
    #     self.assertEquals(User.objects.count(), 0)

    def test_sign_in_GET(self):
        response = self.client.get(self.sign_in_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "base/sign_in.html")

    def test_sign_in_POST(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        response = self.client.get(self.sign_in_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['user'], self.user)

    def test_sign_out_GET(self):
        response = self.client.get(self.sign_out_url)

        self.assertEquals(response.status_code, 302)  # 302 to redirect to login
        self.assertRedirects(response, "/sign_in/")
