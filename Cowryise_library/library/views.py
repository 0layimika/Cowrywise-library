from django.shortcuts import render
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.http import Http404
# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        email = data.get('email')
        if not firstName or not isinstance(data.get('firstName'), str):
            return Response({'errors': [{'field': "firstName", 'message': "firstName is required as string"}]},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not lastName or not isinstance(data.get('lastName'), str):
            return Response({'errors': [{'field': "lastName", 'message': "lastName is required as string"}]},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not email:
            return Response({'errors': [{'field': "email", 'message': "email address is required as email"}]},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            user = User.objects.get(email=email)
            return Response({
                "message":"User already exists in system"
            }, status= status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create(firstName=firstName, lastName=lastName, email=email)
            return Response({
                "message":"User created successfully",
                "data":UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

class BookView(APIView):
    def get(self, request):
        try:
            books = Book.objects.all()
            return Response({
                "message":"All books retrieved successfully",
                "data":BookSerializer(books, many=True).data
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message":err.message
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FilterView(APIView):
    def get(self, request):
        try:
            data = request.data
            if data.get('category') and not data.get('publisher'):
                books = Book.objects.filter(category__iexact=data.get('category'))
            elif data.get('publisher') and not data.get('category'):
                books = Book.objects.filter(publisher__iexact=data.get('publisher'))
            elif data.get('category') and data.get('publisher'):
                books = Book.objects.filter(category__iexact=data.get('category'), publisher__iexact=data.get('publisher'))
            else:
                books = Book.objects.all()
            return Response({
                "message":"Books retrieved successfully",
                "data": BookSerializer(books, many=True).data
            }, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({
                "message": "Such book doesn't exist"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as err:
            return Response({
                "message":err
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SpecificView(APIView):
    def get(self, request, id):
        book = get_object_or_404(Book, pk=id)
        return Response({
            "message":"Book gotten",
            "data":BookSerializer(book).data
        }, status=status.HTTP_200_OK)

    def post(self, request, id):
        try:
            data= request.data
            days = data.get("days")
            email = data.get("email")
            if not days or not email :
                return Response({
                    "message":"days and email are required"
                })
            book = get_object_or_404(Book, pk=id)
            if not book.availability:
                return Response({
                    "message":"Book is currently not available for borrowing"
                })
            borrow_date = datetime.now()
            return_date = (borrow_date +timedelta(days=int(days))).date()
            user = get_object_or_404(User, email=email)
            with transaction.atomic():
                borrow_record = BorrowedBook.objects.create(user=user, book=book, return_data=return_date)
                book.availability = False
                book.save()
            return Response({
                "message":"Book borrowed successfully",
                "data":BorrowedSerializer(borrow_record).data
            }, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({
                "message":str(err)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WebHookView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Book addedd successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)