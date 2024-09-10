from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *
import datetime as dt
import re
import random as r

class signup_serializer(serializers.ModelSerializer):
    password = serializers.CharField()
    class Meta:
        model = LMSUSER
        fields = ["name", "mobile_no", "email", "password"]

    def validate_mobile_no(self, value):
        """ Validate mobile number format """
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Mobile number must be exactly 10 digits.")
        return value

    def validate_email(self, value):
        """ Validate email format """
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
            raise serializers.ValidationError("Invalid email address format.")
        return value

    def validate(self, data):
        """ Additional custom validations """
        if LMSUSER.objects.filter(mobile_no=data.get('mobile_no')).exists():
            raise serializers.ValidationError("A user with this mobile number already exists.")
        if LMSUSER.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return data

    def create(self, validated_data):
        
        # Create and save the user
        user = User(username=validated_data['mobile_no'])
        user.set_password(validated_data['password'])  # Ensure password is set correctly
        user.save()
        validated_data["yearly_income"] = 0
        del validated_data['password']
        # Call the parent create method to handle remaining logic
        return super().create(validated_data)

class centralized_login_serializer(ModelSerializer):
    class Meta:
        model = LOGIN
        fields = ["mobileno","password"]
        extra_kwargs = {'id': {'read_only': True},}

    def validate_mobileno(self, value):
        """ Validate mobile number format or existence """
        if not value:
            raise serializers.ValidationError("Mobile number is required.")
        return value

    def validate_password(self, value):
        """ Validate password presence """
        if not value:
            raise serializers.ValidationError("Password is required.")
        return value

    def create(self, validated_data):
    

       
           
        return super().create(validated_data)
           

       
class Batch_Serializer(ModelSerializer):
    class Meta:
        model = BATCH
        fields = "__all__"
        extra_kwargs = {'id': {'read_only': True}}

class Course_Serializer(ModelSerializer):
    class Meta:
        model = COURSE
        fields = "__all__"
        extra_kwargs = {'id': {'read_only': True},'user': {'read_only': True}}
    def create(self,validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)

class Assets_Serializer(ModelSerializer):
    class Meta:
        model = ASSETS
        fields = "__all__"
        extra_kwargs = {'id': {'read_only': True},'user': {'read_only': True},}


class Student_Serializer(ModelSerializer):
    class Meta:
        model = STUDENT
        fields = "__all__"
        extra_kwargs = {'id': {'read_only': True},'active_student': {'read_only': True},'passout_student': {'read_only': True},'start_date': {'read_only': True},'end_date': {'read_only': True},'BATCH': {'read_only': True},}

    def create(self,validated_data):
     
        validated_data['student_photo'] = self.context.get('request').FILES.get('student_photo')
        validated_data['student_sign'] = self.context.get('request').FILES.get('student_sign')
        validated_data['student_document'] = self.context.get('request').FILES.get('student_document')
  
        return super().create(validated_data)


class Student_Update_Serializer(ModelSerializer):
    paid_amount = serializers.CharField()
    due_amount = serializers.CharField()
   
    class Meta:
        model = STUDENT
        fields = ["BATCH","COURSE","paid_amount","due_amount"]
    
   

    def update(self, instance, validated_data):
        
        
        instance.COURSE_id = validated_data['COURSE']
        instance.BATCH_id = validated_data['BATCH']
        instance.total_paid_amount  = 0
        instance.total_paid_amount = instance.total_paid_amount + int(validated_data['paid_amount'])
        instance.save()
        fees_object = FEEPAID()
        fees_object.student = instance
        fees_object.payment_amount = int(validated_data['paid_amount'])
        
        fees_object.due_amount = int(validated_data['due_amount'])
        fees_object.of_month = 0
        fees_object.date = dt.date.today()
        fees_object.save()
        ledger_obj = STUDENTLEDGER()
        ledger_obj.student = instance
        ledger_obj.payment_date = dt.date.today()
        ledger_obj.payment_amount = int(validated_data['paid_amount'])
        ledger_obj.due_amount = int(validated_data['due_amount'])
        ledger_obj.save()
        l = LMSUSER.objects.get(mobile_no=self.context.get('request').user)
        l.yearly_income = int(l.yearly_income) + int(validated_data['paid_amount'])
        l.save()

        return instance
    



class Student_Monthly_Serializer(ModelSerializer):
    paid_amount = serializers.CharField()
    of_month = serializers.CharField()
   
    class Meta:
        model = STUDENT
        fields = ["paid_amount","of_month"]
    
    def validate(self, data):
        """
        Custom validation to ensure that no duplicate appointments are created.
        """
        
        appointment_id = self.instance.id if self.instance else None

        # Check if another appointment exists with the same mobile number, date, and time.
        conflicting_appointments = STUDENT.objects.filter(
            
            mobile_no=data['mobile_no'],
           
        ).exclude(id=appointment_id)

        if conflicting_appointments.exists():
            raise serializers.ValidationError(
                f"Student with the given number already exists."
            )
        
        return data

    def update(self, instance, validated_data):
        
        
       
        instance.total_paid_amount = instance.total_paid_amount + int(validated_data['paid_amount'])
        instance.save()
        fees_object = FEEPAID.objects.get(student=instance)
        
        fees_object.payment_amount = fees_object.payment_amount + int(validated_data['paid_amount'])
        
        fees_object.due_amount = fees_object.due_amount - int(validated_data['paid_amount'])
        fees_object.of_month = int(validated_data['of_month'])
        fees_object.date = dt.date.today()
        fees_object.save()
        ledger_obj = STUDENTLEDGER()
        ledger_obj.student = instance
        ledger_obj.payment_amount = int(validated_data['paid_amount'])
        ledger_obj.due_amount = int(instance.COURSE.COURSE_fee) - int(instance.total_paid_amount)
        ledger_obj.payment_date = dt.date.today()
        ledger_obj.save()
        l = LMSUSER.objects.get(mobile_no=instance.mobile_no)
        l.yearly_income = l.yearly_income + validated_data['paid_amount']
        l.save()
        return instance
    







