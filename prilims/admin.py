from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(ScoreCard)
class ScoreCardAdmin( admin.ModelAdmin ):

    list_display = [ 'username' , 'score' ]
    list_display_links = list_display[:]
    #list_filter = ['score']

    def get_queryset(self, request):
        query = super(ScoreCardAdmin, self).get_queryset(request)
        filtered_query = query.order_by('-score')
        return filtered_query


# @admin.register(Questions)
# class QuestionAdmin( admin.ModelAdmin ):
#
#     list_display = [ 'question' , 'choice1' , 'choice2' , 'choice3' , 'choice4' ,'correct_answer']
#     #list_display_links = list_display[:]

@admin.register(Questions)
class QuestioAdmain( admin.ModelAdmin ):

    list_display = ['question' , 'choice1', 'choice2' , 'choice3', 'choice4', 'correct_answer'  ]

