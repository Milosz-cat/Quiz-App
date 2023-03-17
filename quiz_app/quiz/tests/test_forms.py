from django.test import SimpleTestCase
from quiz.forms import QuizForm, QuestionForm, AnswerForm, Answer_Select_Form


class TestForms(SimpleTestCase):

    def test_quiz_from_valid_data(self):
        form = QuizForm(data={
            'name' : 'test',
            'description' : 'test description'
        })

        self.assertTrue(form.is_valid())

    def test_quiz_from_no_data(self):
        form = QuizForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

        
