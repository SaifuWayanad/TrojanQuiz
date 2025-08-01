from django.contrib import admin
from home import models
import csv
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect
from django.utils.html import format_html


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question','if_view']

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'start_time','company', 'type', 'district', 'state', 'ip_address']

class BgImageAdmin(admin.ModelAdmin):
    list_display = ['image','type']

class ChoicesAdmin(admin.ModelAdmin):
    list_display = ['question','choice', 'is_answer']

class QuizzExamAdmin(admin.ModelAdmin):
    list_display = [ 'user_name', 'user_phone', 'question_id', 'question_name', 'selected_choice', 'correct_choice',
                    'is_answer_correct', 'choice_selected_time']

def export_all_results(modeladmin, request, queryset):
    # Check if queryset is empty, which means no specific items were selected
    if not queryset:
        queryset = models.Results.objects.all()
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="results.csv"'

    writer = csv.writer(response)
    writer.writerow(['User', 'User Name', 'IP Address', 'User Phone', 'User Company', 'User Type', 
                     'User District', 'User State', 'Exam Start Datetime', 'Exam End Datetime', 
                     'Duration', 'No of Questions Attended', 'Correct Answers', 'Wrong Answers', 'Percentage'])

    for result in queryset:
        writer.writerow([result.user, result.user_name, result.ip_address, result.user_phone, result.user_company, 
                         result.user_type, result.user_district, result.user_state, result.exam_start_datetime, 
                         result.exam_end_datetime, result.duration, result.no_of_questions_attended, 
                         result.correct_answers, result.wrong_answers, result.percentage])

    return response

export_all_results.short_description = "Export All Results"

class ResultsAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_name', 'ip_address', 'user_phone', 'user_company', 'user_type', 'user_district', 
                    'user_state', 'exam_start_datetime', 'exam_end_datetime', 'duration', 'no_of_questions_attended',
                    'correct_answers', 'wrong_answers', 'percentage']
    actions = [export_all_results]
   
admin.site.register(models.Questions, QuestionAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.BgImage, BgImageAdmin)
admin.site.register(models.Choices, ChoicesAdmin)
admin.site.register(models.QuizzExam, QuizzExamAdmin)
admin.site.register(models.Results, ResultsAdmin)

# admin.site.register(models.Questions)
# admin.site.register(models.Choices)
# admin.site.register(models.User)
# admin.site.register(models.Exam)
# admin.site.register(models.QuizzExam)
# admin.site.register(models.Results)
admin.site.register(models.States)
admin.site.register(models.Districts)
# admin.site.register(models.BgImage)
