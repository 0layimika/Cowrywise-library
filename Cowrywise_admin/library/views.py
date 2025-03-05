import requests
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

library_api = "http://localhost:8080/library"

class CreateView(APIView):
    def post(self, request):
        try:
            data = request.data
            title = data.get('title')
            author = data.get('author')
            publisher = data.get('publisher')
            category = data.get('category')
            if not title or not author or not publisher or not category:
                return Response({
                    "message":"title, author, publisher and category are all required"
                }, status=status.HTTP_400_BAD_REQUEST)
            book = Book.objects.create(title=title, author=author, publisher=publisher, category=category)
            try:
                requests.post(f"{library_api}/book", json=BookSerializer(book).data)
            except requests.exceptions.RequestException as e:
                print(f'failed to notify library')
            return Response({
                "message":"Book added to catelogue",
                "data":BookSerializer(book).data
            }, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({
                "message":str(err)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteView(APIView):
    def delete(self, request, id):
        book = get_object_or_404(Book, pk=id)
        book.delete()
        return Response({
            "message":"Deleted",
            "data":BookSerializer(book).data
        }, status=status.HTTP_200_OK)

class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        return Response({
            "message":"All users retrieved",
            "data": UserSerializer(users, many=True).data
        }, status=status.HTTP_200_OK)

class DebtorsView(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            data = []
            for user in users:
                borrowed_books =BorrowedBook.objects.filter(user=user).select_related('book')
                user_data = {
                    'email': user.email,
                    'name': f"{user.firstName} {user.lastName}",
                    "borrowed_books": BorrowedSerializer(borrowed_books, many=True).data
                }
                data.append(user_data)
            return Response({
                "message":"Users with borrowed books fetched successfully",
                "data":data
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message":str(err)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnavView(APIView):
    def get(self, request):
        books = Book.objects.filter(availability=False)
        data = []
        for book in books:
            borrowed_book = BorrowedBook.objects.order_by('-borrowed_at').filter(book=book).first()
            borrow_data={
                "book":book.title,
                "return date":borrowed_book.return_data
            }
            data.append(borrow_data)
        return Response({
            "message":"borrowed books retrieved successfully",
            "data":data
        }, status=status.HTTP_200_OK)