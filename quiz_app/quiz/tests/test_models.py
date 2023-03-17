from django.test import TestCase
from quiz.models import Quiz, Question, Answer, LeaderBoard


class TestModels(TestCase):
    def setUp(self):
        self.quiz1 = Quiz.objects.create(
            name = "testname",
            description = "testdescription",
        )
        
    def test_quiz_is_assigned_is_confirmed_on_creation(self):
        self.assertEquals(self.quiz1.is_confirmed, False)

class QuestionModelTestCase(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(name='Test Quiz', description='A test quiz')
        self.question = Question.objects.create(quiz=self.quiz, text='Test question')

    def test_question_str(self):
        self.assertEqual(str(self.question), 'Test question')

class AnswerModelTestCase(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(name='Test Quiz', description='A test quiz')
        self.question = Question.objects.create(quiz=self.quiz, text='Test question')
        self.answer = Answer.objects.create(question=self.question, content='Test answer')

    def test_answer_str(self):
        self.assertEqual(str(self.answer), 'Test answer')