from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

class LMSUSER(models.Model):
    id = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    name = models.CharField(max_length=1000,blank=True,null=True)
    mobile_no = models.CharField(max_length=1000,blank=True,null=True)
    email = models.CharField(max_length=1000,blank=True,null=True)
    yearly_income = models.IntegerField(default=0)
  
class LOGIN(models.Model):
    id = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    mobileno = models.CharField(max_length=1000,blank=True,null=True)
    password = models.CharField(max_length=1000,blank=True,null=True)
   

class COURSE(models.Model):
    id = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    COURSE_name  = models.CharField(max_length=1000,blank=True,null=True)
    COURSE_fee = models.DecimalField(max_digits=5, decimal_places=2)
   

class BATCH(models.Model):
    id = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    COURSE = models.ForeignKey(COURSE,on_delete=models.CASCADE,null=True)
    BATCH_name = models.CharField(max_length=1000,blank=True,null=True)
    start_date = models.CharField(max_length=1000,blank=True,null=True)
    end_date = models.CharField(max_length=1000,blank=True,null=True)

   
class STUDENT(models.Model):
    id = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    BATCH = models.ForeignKey(BATCH,on_delete=models.CASCADE,blank=True,null=True)

    start_date = models.CharField(max_length=1000,blank=True,null=True)
    end_date = models.CharField(max_length=1000,blank=True,null=True)
    COURSE_duration = models.IntegerField(default=0)
    COURSE = models.ForeignKey(COURSE,on_delete=models.CASCADE,blank=True,null=True)
    
    gender = models.CharField(max_length=1000,blank=True,null=True)
    name = models.CharField(max_length=1000,blank=True,null=True)
    father_name =  models.CharField(max_length=1000,blank=True,null=True)
    mother_name =  models.CharField(max_length=1000,blank=True,null=True)
    material_status =  models.CharField(max_length=1000,blank=True,null=True)
    mobile_no =  models.CharField(max_length=1000,blank=True,null=True)
    dob =  models.CharField(max_length=1000,blank=True,null=True)
    religion =  models.CharField(max_length=1000,blank=True,null=True)
    village =  models.CharField(max_length=1000,blank=True,null=True)
    state =  models.CharField(max_length=1000,blank=True,null=True)
    city =  models.CharField(max_length=1000,blank=True,null=True)
    pincode =  models.CharField(max_length=1000,blank=True,null=True)
    district =  models.CharField(max_length=1000,blank=True,null=True)
    address =  models.CharField(max_length=1000,blank=True,null=True)
    qualification =  models.CharField(max_length=1000,blank=True,null=True)
    category =  models.CharField(max_length=1000,blank=True,null=True)
   
    student_photo =  models.ImageField(upload_to="student_images",null=True,blank=True)
    student_sign =  models.ImageField(upload_to="student_signature",null=True,blank=True)
    student_document =  models.ImageField(upload_to="student_document",null=True,blank=True)
    active_student = models.BooleanField(default=False,blank=True,null=True)
    passout_student = models.BooleanField(default=False,blank=True,null=True)
    total_paid_amount = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
    
class FEEPAID(models.Model):
    id = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    student = models.ForeignKey(STUDENT,on_delete=models.CASCADE,null=True)
    date = models.CharField(max_length=1000,blank=True,null=True)
    payment_amount = models.IntegerField()
    due_amount = models.IntegerField()
    of_month = models.IntegerField()



   
class ASSETS(models.Model):
    id = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    user = models.ForeignKey(LMSUSER,on_delete=models.CASCADE,null=True)
    expence_daily = models.IntegerField(default=0)
    reason = models.CharField(max_length=100)
   


class STUDENTLEDGER(models.Model):
    id = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    student = models.ForeignKey(STUDENT,on_delete=models.CASCADE,null=True)
    payment_date = models.DateField(blank=True,null=True)
   
    payment_amount = models.IntegerField()
    due_amount = models.IntegerField()


class STAFF(models.Model):
    pass
class STAFFATTANDANCE(models.Model):
    pass
