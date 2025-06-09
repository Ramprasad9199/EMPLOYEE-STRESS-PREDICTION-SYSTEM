from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):

    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address= models.CharField(max_length=300)
    gender= models.CharField(max_length=30)

class Predicting_Employee_Stress(models.Model):

    employee_id= models.CharField(max_length=3000)
    department= models.CharField(max_length=3000)
    region= models.CharField(max_length=3000)
    education= models.CharField(max_length=3000)
    gender= models.CharField(max_length=3000)
    recruitment_channel= models.CharField(max_length=3000)
    Training_Time= models.CharField(max_length=3000)
    age= models.CharField(max_length=3000)
    Prformance_Rating= models.CharField(max_length=3000)
    Years_at_company= models.CharField(max_length=3000)
    Working_Hours= models.CharField(max_length=3000)
    Flexible_Timings= models.CharField(max_length=3000)
    Workload_level= models.CharField(max_length=3000)
    Monthly_Income= models.CharField(max_length=3000)
    Work_Satisfaction= models.CharField(max_length=3000)
    Percent_salary_hike= models.CharField(max_length=3000)
    companies_worked= models.CharField(max_length=3000)
    Marital_Status= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)


class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)
