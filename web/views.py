from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView,ListAPIView,DestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import NotFound
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate # type: ignore
from django.db import transaction
from rest_framework.serializers import ValidationError
from django.core.mail import send_mail
from rest_framework import status
from .serializer import *
from rest_framework.authtoken.models import Token
class AdminLogin(CreateAPIView,RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = signup_serializer

    def post(self, request):
     
        try:
            # Converting request data into Python native datatype
            serializer_objects = self.serializer_class(data=request.data)
            
            # Validate the serializer data
            if serializer_objects.is_valid():
                # Save the user data to the database
                serializer_objects.save()

                # Returning the status and info as response
                return Response({
                    'success': True,
                    'status_code': status.HTTP_201_CREATED,
                    'error': {
                        'code': 'The request was successful',
                        'message': 'User_created'
                    },
                    'data': {
                        'user': serializer_objects.validated_data.get('user_name'),
                     
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                # Handling validation errors
                return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'error': {
                        'code': 'The request was unsuccessful',
                        'message': serializer_objects.errors
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch any unexpected errors and log them
            return Response({
                'success': False,
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'error': {
                    'code': 'Internal Server Error',
                    'message': str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Login(APIView):
    
    serializer_class = centralized_login_serializer
    permission_classes = [AllowAny]


    def post(self, request):
        '''Handle user login and return appropriate response'''
        serializer = self.serializer_class(data=request.data, context={"request": request})

        if serializer.is_valid():
            try:
                result = serializer.create(serializer.validated_data)
                
                # If login is successful
                user = auth.authenticate(username=serializer.data.get('mobileno'), password=serializer.data.get('password'))
                if user:
                    auth.login(request, user)
                    try:
                        token = Token.objects.get(user=user)
                    except Exception:
                        token = Token.objects.create(user=user)
               
                

                    return Response({
                        'success': True,
                        'status_code': status.HTTP_200_OK,
                        'error': {
                            'code': 'The request was successful',
                            'message': "login successful!",
                        },
                        'data': {
                            'token': str(token),
                            'user': str(request.user),
                        
                        }
                    })

                
            

            except ValidationError as e:
                return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'error': {
                        'code': 'The request was unsuccessful',
                        'message': str(e),
                    },
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'error': {
                'code': 'The request was unsuccessful',
                'message': 'Invalid input data',
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)





class Batch(CreateAPIView,UpdateAPIView,ListAPIView,DestroyAPIView):
    serializer_class = Batch_Serializer
    permission_classes = [IsAuthenticated]



    def Post(self,request):
        data = request.data
        serializer = self.serializer_class(data=request.data, context={"request": request})

        if serializer.is_valid():
            try:
                serializer_data = serializer.create(serializer.validated_data)
                
               
               
                

                response_data = {
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'error': {
                        'code': 'The request was successful',
                        'message': "Batch Created!",
                    },
                    'data': serializer_data.data
                }

                
            

            except ValidationError as e:
                return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'error': {
                        'code': 'The request was unsuccessful',
                        'message': str(e),
                    },
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'error': {
                'code': 'The request was unsuccessful',
                'message': 'Invalid input data',
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request):
        # Extract query parameters
        batch_id = request.query_params.get('id')
       

        if not batch_id:
            return Response({
                'status': False,
                'error': 'batch_id is required.'
            }, status=400)

        # Check for existing BATCH to prevent duplicates
        existing_Batch = BATCH.objects.filter(
            COURSE_id=request.data.get('COURSE'),
            BATCH_name=request.data.get('BATCH_name'),
            start_date=request.data.get('start_date'),
            end_date=request.data.get('end_date')
            
        ).exclude(id=batch_id)

        if existing_Batch.exists():
            return Response({
                'status': False,
                'error': f"Batch already exists."
            }, status=409)

        # Fetch the existing appointment instance
        try:
            batch = BATCH.objects.get(id=batch_id, COURSE__user=request.user)
        except BATCH.DoesNotExist:
            raise NotFound('Batch not found.')

        # Prepare the data to be updated
        data = request.data.copy()
       

        # Use the serializer to validate and update the instance
        serializer = self.serializer_class(batch, data=data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': "Batch updated successfully."
            }, status=200)
        else:
            return Response({
                'status': False,
                'errors': serializer.errors
            }, status=400)
        
    def delete(self, request):
        Batch_id = request.query_params.get('id')

        # Check if the appointment ID is provided
        if not Batch_id:
            return Response({
                "status": False,
                "code": 400,
                "message": "batch_id is required."
            }, status=400)

        try:
            # Ensure the batch exists and belongs to the authenticated user
            batch = BATCH.objects.get(id=Batch_id, COURSE__user=request.user)

            # Delete the appointment
            batch.delete()

            return Response({
                "status": True,
                "code": 200,
                "message": "batch successfully deleted.",
                "batch_deleted_id": batch.id
            }, status=200)

        except BATCH.DoesNotExist:
            # If the appointment does not exist or doesn't belong to the user
            return Response({
                "status": False,
                "code": 404,
                "message": f"batch with ID {Batch_id} does not exist.",
            }, status=404)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                "status": False,
                "code": 500,
                "message": f"An error occurred: {str(e)}",
            }, status=500)


    def list(self,request):
        query_set = BATCH.objects.filter(COURSE__user=request.user).order_by('-id')
        serializer_obj = self.serializer_class(query_set, many=True)
        
        return Response({
            "status": True,
            "data": serializer_obj.data,
        })

    




        
class Course(CreateAPIView,UpdateAPIView,ListAPIView,DestroyAPIView):
    serializer_class = Course_Serializer
    permission_classes = [IsAuthenticated]



    def Post(self,request):
        data = request.data
        serializer = self.serializer_class(data=request.data, context={"request": request})

        if serializer.is_valid():
            try:
                serializer_data = serializer.create(serializer.validated_data)
                
               
               
                

                response_data = {
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'error': {
                        'code': 'The request was successful',
                        'message': "Course Created!",
                    },
                    'data': serializer_data.data
                }

                
            

            except ValidationError as e:
                return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'error': {
                        'code': 'The request was unsuccessful',
                        'message': str(e),
                    },
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'error': {
                'code': 'The request was unsuccessful',
                'message': 'Invalid input data',
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request):
        # Extract query parameters
        course_id = request.query_params.get('id')
       

        if not course_id:
            return Response({
                'status': False,
                'error': 'id is required.'
            }, status=400)

        # Check for existing course to prevent duplicates
        existing_Batch = COURSE.objects.filter(
            user=request.user,
            course_name=request.data.get('course_name')
            
        ).exclude(id=course_id)

        if existing_Batch.exists():
            return Response({
                'status': False,
                'error': f"course already exists."
            }, status=409)

        # Fetch the existing course instance
        try:
            appointment = COURSE.objects.get(id=course_id, COURSE__user=request.user)
        except COURSE.DoesNotExist:
            raise NotFound('course not found.')

        # Prepare the data to be updated
        data = request.data.copy()
       

        # Use the serializer to validate and update the instance
        serializer = self.serializer_class(appointment, data=data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': "course updated successfully."
            }, status=200)
        else:
            return Response({
                'status': False,
                'errors': serializer.errors
            }, status=400)
        
    def delete(self, request):
        course_id = request.query_params.get('id')

        # Check if the appointment ID is provided
        if not course_id:
            return Response({
                "status": False,
                "code": 400,
                "message": "id is required."
            }, status=400)

        try:
            # Ensure the batch exists and belongs to the authenticated user
            batch = COURSE.objects.get(id=course_id, COURSE__user=request.user)

            # Delete the appointment
            batch.delete()

            return Response({
                "status": True,
                "code": 200,
                "message": "course successfully deleted.",
                "course_deleted_id": batch.id
            }, status=200)

        except COURSE.DoesNotExist:
            # If the appointment does not exist or doesn't belong to the user
            return Response({
                "status": False,
                "code": 404,
                "message": f"course with ID {course_id} does not exist.",
            }, status=404)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                "status": False,
                "code": 500,
                "message": f"An error occurred: {str(e)}",
            }, status=500)


    def list(self,request):
        query_set = COURSE.objects.filter(user=request.user).order_by('-id')
        serializer_obj = self.serializer_class(query_set, many=True)
        
        return Response({
            "status": True,
            "table_data": serializer_obj.data,
        })

    



class Student(CreateAPIView,UpdateAPIView,ListAPIView,DestroyAPIView):
    serializer_class = Student_Serializer
    permission_classes = [IsAuthenticated]



    def Post(self,request):
        data = request.data
        serializer = self.serializer_class(data=request.data, context={"request": request})

        if serializer.is_valid():
            try:
                serializer_data = serializer.create(serializer.validated_data)
                
               
               
                

                return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'error': {
                        'code': 'The request was successful',
                        'message': "Student Created!",
                    },
                    'data': serializer_data.data
                })

                
            

            except ValidationError as e:
                return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'error': {
                        'code': 'The request was unsuccessful',
                        'message': str(e),
                    },
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'error': {
                'code': 'The request was unsuccessful',
                'message': 'Invalid input data',
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request):
        # Extract query parameters
        student_id = request.query_params.get('id')
       

        if not student_id:
            return Response({
                'status': False,
                'error': 'id is required.'
            }, status=400)

        # Check for existing BATCH to prevent duplicates
        existing_Batch = STUDENT.objects.filter(
            COURSE_id=request.data.get('COURSE'),
           
            
        ).exclude(id=student_id)

        if existing_Batch.exists():
            return Response({
                'status': False,
                'error': f"student already exists."
            }, status=409)

        # Fetch the existing appointment instance
        try:
            student = STUDENT.objects.get(id=student_id, COURSE__user=request.user)
        except STUDENT.DoesNotExist:
            raise NotFound('Student not found.')

        # Prepare the data to be updated
        data = request.data.copy()
       

        # Use the serializer to validate and update the instance
        serializer = Student_Update_Serializer(student, data=data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': "student updated successfully."
            }, status=200)
        else:
            return Response({
                'status': False,
                'errors': serializer.errors
            }, status=400)
        
    def delete(self, request):
        student_id = request.query_params.get('id')

        # Check if the appointment ID is provided
        if not student_id:
            return Response({
                "status": False,
                "code": 400,
                "message": "student_id is required."
            }, status=400)

        try:
            # Ensure the batch exists and belongs to the authenticated user
            batch = STUDENT.objects.get(id=student_id, COURSE__user=request.user)

            # Delete the appointment
            batch.delete()

            return Response({
                "status": True,
                "code": 200,
                "message": "student successfully deleted.",
                "batch_deleted_id": batch.id
            }, status=200)

        except STUDENT.DoesNotExist:
            # If the appointment does not exist or doesn't belong to the user
            return Response({
                "status": False,
                "code": 404,
                "message": f"student with ID {student_id} does not exist.",
            }, status=404)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                "status": False,
                "code": 500,
                "message": f"An error occurred: {str(e)}",
            }, status=500)


    def list(self,request):
        query_set = STUDENT.objects.filter(COURSE__user=request.user).order_by('-id')
        serializer_obj = self.serializer_class(query_set, many=True)
        
        return Response({
            "status": True,
            "table_data": serializer_obj.data,
        })


class Assets(ListAPIView,CreateAPIView):
    serializer_class = Assets_Serializer
    permission_classes = [IsAuthenticated]
    def list(self,request):
        query_set = ASSETS.objects.filter(user=request.user).order_by('-id')
        serializer_obj = self.serializer_class(query_set, many=True)
        
        return Response({
            "status": True,
            "table_data": serializer_obj.data,
        })
    def Post(self,request):
        data = request.data
        serializer = self.serializer_class(data=request.data, context={"request": request})

        if serializer.is_valid():
            try:
                serializer_data = serializer.create(serializer.validated_data)
                
               
               
                

                response_data = {
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'error': {
                        'code': 'The request was successful',
                        'message': "Assets Created!",
                    },
                    'data': serializer_data.data
                }

                
            

            except ValidationError as e:
                return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'error': {
                        'code': 'The request was unsuccessful',
                        'message': str(e),
                    },
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'error': {
                'code': 'The request was unsuccessful',
                'message': 'Invalid input data',
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    