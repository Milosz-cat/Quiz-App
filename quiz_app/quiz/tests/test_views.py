# from django.test import TestCase, Client
# from django.urls import reverse
# from quiz import models
# from quiz import views



# class TestViews(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.url = reverse('some_view')  # zastąp some_view nazwą widoku, który używa @login_required
#         self.user = User.objects.create_user(username='testuser', password='testpass')


#     def test_create_quiz_GET(self):
#         client = Client()
#         client.login()
        
#         response = client.get(reverse('create_quiz'))

#         self.assertEquals(response.status_code, 302) # 200 is OK, 302 to redirect to login
#         self.assertTemplateUsed(response, 'quiz/create_quiz.html')