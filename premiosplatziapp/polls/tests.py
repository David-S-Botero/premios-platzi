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

def create_choice(question, choice_text="some choice", votes=0):
    """
    Given a question this functions sets to that question a choice with the given "choice_text" and "votes".
    """
    question.choice_set.create(choice_text=choice_text, votes=votes)

class QuestionIndexViewTest(TestCase):

    def test_no_questions(self):
        """
        If no question exist, an appropiate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_questions_with_choices(self):
        """
        If there is any question published in the future, the index view shouldn't show it.
        """
        future_question = create_question(days=30)
        create_choice(future_question)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions_with_choices(self):
        """
        If there is any question published in the past with choices assigned the index view should display it.
        """
        past_question = create_question(days=-1)
        create_choice(past_question)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'],[past_question])

    def test_past_questions_without_choices(self):
        """
        If there is any question published in the past without choices assigned the index view shouldn't display it.
        """
        past_question = create_question(days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    #Expanding the testing coverage

    def test_future_question_and_past_question_with_choices(self):
        """
        Even if both past and future question exist and both have choices, only past questions are display.
        """
        past_question = create_question(question_text="Past question", days=-30)
        create_choice(past_question)
        future_question = create_question(question_text="Future question", days=30)
        create_choice(future_question)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

    def test_two_past_questions_with_choices(self):
        """
        The questions index page may display multiple questions.
        """
        past_question_1 = create_question(question_text="Past question 1", days=-32)
        create_choice(past_question_1)
        past_question_2 = create_question(question_text="Past question 2", days=-30)
        create_choice(past_question_2)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question_2, past_question_1])

    def test_two_past_questions_without_choices(self):
        """
        The questions index page may display no questions.
        """
        past_question_1 = create_question(question_text="Past question 1", days=-32)
        past_question_2 = create_question(question_text="Past question 2", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_two_future_questions_with_choices(self):
        """
        The questions index page may display no questions.
        """
        future_question_1 = create_question(question_text="Future question 1", days=32)
        create_choice(future_question_1)
        future_question_2 = create_question(question_text="Future question 2", days=30)
        create_choice(future_question_2)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_two_future_questions_without_choices(self):
        """
        The questions index page may display no questions.
        """
        future_question_1 = create_question(question_text="Future question 1", days=32)
        future_question_2 = create_question(question_text="Future question 2", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


class QuestionDetailViewTest(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 error not found.
        """
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question's text.
        """
        past_question = create_question(question_text="Past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTest(TestCase):

    def test_future_question(self):
        """
        The results view of a question with a pub_date in the future returns a 404 errror not found.
        """
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The results view of a question with a pub_date in the past displays the choices with their respective votes counting.
        """
        past_question = create_question(question_text="Past question", days=-30)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)