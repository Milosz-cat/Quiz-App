from django.test import SimpleTestCase
from django.urls import reverse, resolve
from quiz import views



class TestUrls(SimpleTestCase):

    def test_create_quiz_url_resolves(self):
        url = reverse('create_quiz')
        self.assertEquals(resolve(url).func, views.create_quiz)
    
    def test_create_question_url_resolves(self):
        url = reverse('create_question', args=[1])
        self.assertEquals(resolve(url).func, views.create_question)
    
    def test_start_quiz_url_resolves(self):
        url = reverse('start_quiz', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.QuizDetailView)

    def test_question_url_resolves(self):
        url = reverse('question', args=[1])
        self.assertEquals(resolve(url).func, views.question)

    def test_summary_url_resolves(self):
        url = reverse('summary', args=[1])
        self.assertEquals(resolve(url).func, views.summary)