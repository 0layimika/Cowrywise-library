from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowedSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    book = BookSerializer()
    class Meta:
        model = BorrowedBook
        fields = ['book','borrowed_at','return_data']
