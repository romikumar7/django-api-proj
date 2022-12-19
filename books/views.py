from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from books.models import Book, Author
from books.serializers import BookSerializer, AuthorSerializer, BookListSerializer
from datetime import datetime
import re

# Create your views here.

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer

@api_view(['GET'])
def filter_book_title(request, title):
    try:
        title += '+'
        book_list = Book.objects.filter(title__iregex=title)
    except Book.DoesNotExist:
        return Response({"message": "Book Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
    serializer  = BookListSerializer(book_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_book_page(request, pageCnt):
    try:
        book_list = Book.objects.filter(pageCount__gte=pageCnt)
    except Book.DoesNotExist:
        return Response({"message": "Book Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
    serializer  = BookListSerializer(book_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_book_date(request, dt):
    try:
        dt_obj= datetime.strptime(dt, '%Y-%m-%d').date()       
        book_list = Book.objects.filter(releaseDate__lte=dt_obj)
    except Book.DoesNotExist:
        return Response({"message": "Book Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
    serializer  = BookListSerializer(book_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_book_author_id(request, id):
    try:
        book_list = Book.objects.filter(authors__id=id)
    except Book.DoesNotExist:
        return Response({"message": "Book Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
    serializer  = BookListSerializer(book_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_book_author_name(request, name):
    try:
        name += '+'
        book_list = Book.objects.filter(authors__name__iregex=name)
    except Book.DoesNotExist:
        return Response({"message": "Book Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
    serializer  = BookListSerializer(book_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_book_author_surname(request, surname):
    try:
        surname += '+'
        book_list = Book.objects.filter(authors__surname__iregex=surname)
    except Book.DoesNotExist:
        return Response({"message": "Book Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
    serializer  = BookListSerializer(book_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_book_author_fullname(request, fullname):
    bl= []
    try:
        fullname += '+'
        book_list = Book.objects.all()
        for book in book_list:
            for author in book.authors.all():
                if re.search(fullname, author.full_name) is not None:
                    bl.append(book)
    except Book.DoesNotExist:
        return Response({"message": "Book Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
    serializer  = BookListSerializer(bl, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_author_name(request, name):
    try:
        name += '+'   
        author_list = Author.objects.filter(name__iregex=name)
    except Author.DoesNotExist:
        return Response({"message": "Author Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
    serializer  = AuthorSerializer(author_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_author_surname(request, surname):
    try:
        surname += '+'   
        author_list = Author.objects.filter(surname__iregex=surname)
    except Author.DoesNotExist:
        return Response({"message": "Author Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
    serializer  = AuthorSerializer(author_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_author_email(request, email):
    try:  
        author_list = Author.objects.filter(email__iregex=email)
    except Author.DoesNotExist:
        return Response({"message": "Author Doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
    serializer  = AuthorSerializer(author_list, many=True)
    return Response(serializer.data)

class AuthorCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

class BookCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

class AuthorUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    lookup_url_kwarg = 'author_id'
    serializer_class = AuthorSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

class BookUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    lookup_url_kwarg = 'book_id'
    serializer_class = BookSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]
