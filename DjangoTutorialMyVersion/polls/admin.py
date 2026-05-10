from django.contrib import admin

from .models import Question, Choice, Category, Vote, Comment, UserProfile


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text", "category", "is_published", "image_url"]}),
        ("Date information", {"fields": ["pub_date", "end_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "category", "pub_date", "end_date", "was_published_recently", "is_published"]
    list_filter = ["pub_date", "category", "is_published"]
    search_fields = ["question_text"]
    date_hierarchy = "pub_date"


class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'choice']
    list_filter = ['question']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'created_at']
    search_fields = ['text']
    list_filter = ['created_at', 'question']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Category)
admin.site.register(Choice)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile)