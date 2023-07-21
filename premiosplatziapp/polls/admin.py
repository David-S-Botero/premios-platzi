from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    
    model = Choice #Model to display inline
    
    extra = 3 #How many choices per question


class QuestionAdmin(admin.ModelAdmin):
    #Fields order in the admin
    fields=["pub_date", "question_text"]
    #Inline classes to be displayed
    inlines = [ChoiceInline]

    list_display = ("question_text", "pub_date", "was_publish_recently")

    list_filter = ["pub_date"]

    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)