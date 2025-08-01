from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=250)
    phone_number = models.BigIntegerField()
    start_time = models.DateTimeField(blank=True, null=True)
    company = models.CharField(max_length=250)
    type = models.CharField(max_length=50)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    medium = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.name
    
class BgImage(models.Model):
    image = models.ImageField(upload_to='backgrounds/')
    type = models.CharField(max_length=500)

class Questions(models.Model):
    question = models.CharField(max_length=250)
    medium = models.CharField(max_length=100)
    if_view = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.question

class Choices(models.Model):
    question = models.ForeignKey(
        Questions, related_name= "choices", # Reverse access name for choices of a question
        on_delete=models.CASCADE
    )
    choice = models.CharField(max_length=250)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.choice

class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choices, on_delete=models.CASCADE)
    date = models.DateField()
    exam_start_datetime = models.DateTimeField()
    exam_end_datetime = models.DateTimeField()

class QuizzExam(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200)
    user_phone = models.BigIntegerField()
    question_id = models.IntegerField()
    question_name = models.CharField(max_length=250)
    selected_choice = models.CharField(max_length=200)
    correct_choice = models.CharField(max_length=200)
    is_answer_correct = models.BooleanField(default=False)
    choice_selected_time = models.DateTimeField()

class Results(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    user_phone = models.BigIntegerField()
    user_company = models.CharField(max_length=200)
    user_type = models.CharField(max_length=200)
    user_district = models.CharField(max_length=200)
    user_state = models.CharField(max_length=200)
    exam_start_datetime = models.DateTimeField()
    exam_end_datetime = models.DateTimeField()
    duration = models.IntegerField()
    no_of_questions_attended = models.IntegerField()
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    percentage = models.FloatField()

class States(models.Model):
    state_name = models.CharField(max_length=150)

class Districts(models.Model):
    state_name = models.ForeignKey(States, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=250)
