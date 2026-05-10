import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question, Choice, Vote, Category, Comment

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_unpublished_question(self):
        Question.objects.create(
            question_text="Unpublished question.", 
            pub_date=timezone.now() - datetime.timedelta(days=1), 
            is_published=False
        )
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

class VoteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.question = create_question("Test Question", -1)
        self.choice1 = Choice.objects.create(question=self.question, choice_text="C1")
        self.choice2 = Choice.objects.create(question=self.question, choice_text="C2")

    def test_vote_requires_login(self):
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id})
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_duplicate_vote_prevented(self):
        self.client.login(username='testuser', password='password')
        self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id})
        self.assertEqual(Vote.objects.count(), 1)
        # Try again
        self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice2.id})
        self.assertEqual(Vote.objects.count(), 1)

class ExpirationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u2', password='p2')
        self.q = Question.objects.create(question_text="Expired", pub_date=timezone.now()-datetime.timedelta(days=2), end_date=timezone.now()-datetime.timedelta(days=1))
        self.c = Choice.objects.create(question=self.q, choice_text="C")

    def test_expired_poll_vote_fails(self):
        self.client.login(username='u2', password='p2')
        response = self.client.post(reverse('polls:vote', args=(self.q.id,)), {'choice': self.c.id})
        self.assertEqual(Vote.objects.count(), 0)
        self.assertEqual(response.status_code, 302)