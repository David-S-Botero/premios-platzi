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

def create_question(question_text = "Some text", days=0, hours=0, minutes=0, seconds=0):
    """
    Create a question with the given "question_text" and published the
    given number of days, hours, minutes and seconds offset to now (negative for questions published in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days, hours=hours, seconds=seconds, minutes=minutes)
    return Question.objects.create(question_text = question_text,pub_date = time)

class QuestionIndexViewTest(TestCase):

    def test_no_questions(self):
        """
        If no question exist, an appropiate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_questions(self):
        """
        If there is any question published in the future, the index view shouldn't show it.
        """
        future_question = create_question(days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(container=response.context['latest_question_list'], member=future_question)

    def test_past_questions(self):
        """
        If there is any question published in the past the index view should display it.
        """
        past_question = create_question(days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(container=response.context['latest_question_list'],member=past_question)

    #Expanding the testing coverage

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are display.
        """
        past_question = create_question(question_text="Past question", days=-30)
        future_question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        past_question_1 = create_question(question_text="Past question 1", days=-32)
        past_question_2 = create_question(question_text="Past question 2", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question_2, past_question_1])

    def test_two_future_questions(self):
        """
        The questions index page may display no questions.
        """
        future_question_1 = create_question(question_text="Future question 1", days=32)
        future_question_2 = create_question(question_text="Future question 2", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
