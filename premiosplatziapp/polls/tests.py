from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
import datetime
from .models import Question

class QuestionModelTest(TestCase):
    
    def setUp(self) -> None:
        """
        Sets up the question to be tested with 
        """
        self.question = Question(question_text = "Quién es el mejor cd de platzi?")

    def test_was_published_recently_with_future_questions(self):
        """
        Was published recently returns false for question whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertFalse(self.question.was_publish_recently())

    def test_was_published_recently_with_present_questions(self):
        """
        Was published recently returns true for question whose pub_date is in the present.
        """
        time = timezone.now() - datetime.timedelta(hours=23)
        self.question.pub_date = time
        self.assertTrue(self.question.was_publish_recently())

    def test_was_published_recently_with_past_questions(self):
        """
        Was published recently returns false for question whose pub_date is in the past.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertFalse(self.question.was_publish_recently())


