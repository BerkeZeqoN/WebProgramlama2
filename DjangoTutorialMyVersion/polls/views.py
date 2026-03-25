from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum

from .models import Choice, Question, Vote, Comment, Category, UserProfile

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        cat_id = self.request.GET.get('category', '')
        qs = Question.objects.filter(pub_date__lte=timezone.now(), is_published=True)
        if query:
            qs = qs.filter(question_text__icontains=query)
        if cat_id:
            qs = qs.filter(category_id=cat_id)
        return qs.order_by("-pub_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['trending_polls'] = Question.objects.filter(
            is_published=True, pub_date__lte=timezone.now()
        ).annotate(total_votes=Sum('choice__votes')).order_by('-total_votes')[:3]
        return context

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now(), is_published=True)

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.object
        total_votes = sum(choice.votes for choice in question.choice_set.all())
        context['total_votes'] = total_votes
        
        choices_with_percentage = []
        for choice in question.choice_set.all():
            percentage = (choice.votes / total_votes * 100) if total_votes > 0 else 0
            choices_with_percentage.append({
                'id': choice.id,
                'choice_text': choice.choice_text,
                'votes': choice.votes,
                'percentage': int(percentage)
            })
        context['choices_with_percentage'] = choices_with_percentage
        return context

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.end_date and question.end_date < timezone.now():
        messages.error(request, "Bu anketin süresi dolmuş ve oylamaya kapatılmıştır.")
        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))

    if Vote.objects.filter(user=request.user, question=question).exists():
        messages.error(request, "Bu ankete zaten oy verdiniz.")
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "Geçerli bir seçenek belirtmediniz.")
        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        Vote.objects.create(user=request.user, question=question, choice=selected_choice)
        messages.success(request, "Oyunuz başarıyla kaydedildi.")
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

@login_required
def add_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        text = request.POST.get("comment_text")
        if text:
            Comment.objects.create(user=request.user, question=question, text=text)
            messages.success(request, "Yorumunuz eklendi.")
        else:
            messages.error(request, "Yorum boş olamaz.")
    return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        avatar_url = request.POST.get("avatar_url")
        if avatar_url is not None:
            user_profile.avatar_url = avatar_url
            user_profile.save()
            messages.success(request, "Profil resminiz başarıyla güncellendi.")
            return HttpResponseRedirect(request.path)

    votes = Vote.objects.filter(user=request.user).select_related('question', 'choice').order_by('-id')
    comments = Comment.objects.filter(user=request.user).select_related('question').order_by('-created_at')
    return render(request, "polls/profile.html", {
        "user_votes": votes, 
        "user_comments": comments,
        "user_profile": user_profile
    })