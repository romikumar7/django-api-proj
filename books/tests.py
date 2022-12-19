from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Author, Book, Genre
from collections import OrderedDict
import datetime

def create_author(nam, sname, emails, fbName):
    return Author.objects.create(name=nam, surname= sname,
                email=emails, facebookUserName=fbName)

def create_genre(name):
    return Genre.objects.create(genre=name)

def create_book(title, pageCount, releaseDate, authors, genre):
    book = Book.objects.create(title=title, pageCount=pageCount, releaseDate=releaseDate,
                               genre=genre)
    for author in authors:
        book.authors.add(author)
    return book

def create_book_test_db():
    a1 = create_author('author4', 'sname3', 'as4@test.com', 'as4')
    a2 = create_author('author5', 'sname2', 'as5@test.com', 'as5')
    g1 = create_genre("horror")
    g2 = create_genre("comic")
    create_book('horro1', 100, datetime.date.today(), [a1], g1)
    create_book('comichorror1', 140, datetime.date.today(), [a1,a2], g2)

class AuthorTests(APITestCase):
    res = [OrderedDict([('id', 1), ('name', 'author1'), ('surname', 'sname1'),
                            ('email', 'as1@test.com'), ('phoneNo', ''), 
                            ('facebookUserName', 'as1'), ('image', None)])]
    
    def test_list_author(self):
        create_author('author1', 'sname1', 'as1@test.com', 'as1')
        url = reverse('authorList')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.res)

    def test_filter_author_by_name(self):
        create_author('author1', 'sname1', 'as1@test.com', 'as1')
        url = reverse('authorName', args=('author',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.res)

    def test_filter_author_by_name1(self):
        create_author('author1', 'sname1', 'as1@test.com', 'as1')
        url = reverse('authorName', args=('test',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_filter_author_by_surname(self):
        create_author('author1', 'sname1', 'as1@test.com', 'as1')
        url = reverse('authorSurname', args=('sname',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.res)

    def test_filter_author_by_email(self):
        create_author('author1', 'sname1', 'as1@test.com', 'as1')
        url = reverse('authorEmail', args=('as1@test.com',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.res)

    def test_author_create(self):
        url = reverse('authorCreate')
        res = OrderedDict([('id', 1), ('name', 'author1'), ('surname', 'sname1'),
                            ('email', 'as1@test.com'),
                            ('facebookUserName', 'as1')])
        response = self.client.post(url, data=res)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_update(self):
        url = reverse('authorUpdate', args=(1,))
        res = OrderedDict([('id', 1), ('name', 'author1'), ('surname', 'sname1'),
                            ('email', 'as1@test.com'),
                            ('facebookUserName', 'as1')])
        response = self.client.post(url, data=res)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class BookTests(APITestCase):
    
    def test_list_book(self):
        create_book_test_db()
        url = reverse('bookList')
        response = self.client.get(url)
        res = [OrderedDict([('title', 'horro1'), ('pageCount', 100), ('releaseDate', '2022-12-19'),
                            ('authors', ['author4 sname3']), ('genre', 'horror')]),
                OrderedDict([('title', 'comichorror1'), ('pageCount', 140), 
                ('releaseDate', '2022-12-19'), ('authors', ['author4 sname3', 'author5 sname2']),
                ('genre', 'comic')])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, res)

    def test_filter_book_title(self):
        create_book_test_db()
        url = reverse('bookTitle', args=('comi',))
        response = self.client.get(url)
        res = [OrderedDict([('title', 'comichorror1'), ('pageCount', 140), 
                ('releaseDate', '2022-12-19'), ('authors', ['author4 sname3', 'author5 sname2']),
                ('genre', 'comic')])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, res)

    def test_filter_book_pageCount(self):
        create_book_test_db()
        url = reverse('bookPages', args=(120,))
        response = self.client.get(url)
        res = [OrderedDict([('title', 'comichorror1'), ('pageCount', 140), 
                ('releaseDate', '2022-12-19'), ('authors', ['author4 sname3', 'author5 sname2']),
                ('genre', 'comic')])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, res)

    def test_filter_book_date(self):
        create_book_test_db()
        url = reverse('bookPubDate', args=(datetime.date.today(),))
        response = self.client.get(url)
        res = [OrderedDict([('title', 'horro1'), ('pageCount', 100), ('releaseDate', '2022-12-19'),
                            ('authors', ['author4 sname3']), ('genre', 'horror')]),
                OrderedDict([('title', 'comichorror1'), ('pageCount', 140), 
                ('releaseDate', '2022-12-19'), ('authors', ['author4 sname3', 'author5 sname2']),
                ('genre', 'comic')])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, res)

    def test_filter_book_authorid(self):
        create_book_test_db()
        url = reverse('bookAuthorId', args=(1,))
        response = self.client.get(url)
        res = [OrderedDict([('title', 'horro1'), ('pageCount', 100), ('releaseDate', '2022-12-19'),
         ('authors', ['author4 sname3']), ('genre', 'horror')]), 
         OrderedDict([('title', 'comichorror1'), ('pageCount', 140), ('releaseDate', '2022-12-19'),
        ('authors', ['author4 sname3', 'author5 sname2']), ('genre', 'comic')])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, res)

    def test_filter_book_authorName(self):
        create_book_test_db()
        url = reverse('bookAuthorName', args=('author5',))
        response = self.client.get(url)
        res = [OrderedDict([('title', 'comichorror1'), ('pageCount', 140), ('releaseDate', '2022-12-19'),
        ('authors', ['author4 sname3', 'author5 sname2']), ('genre', 'comic')])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, res)

    def test_filter_book_authorSurName(self):
        create_book_test_db()
        url = reverse('bookAuthorSurname', args=('sname2',))
        response = self.client.get(url)
        res = [OrderedDict([('title', 'comichorror1'), ('pageCount', 140), ('releaseDate', '2022-12-19'),
        ('authors', ['author4 sname3', 'author5 sname2']), ('genre', 'comic')])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, res)

    def test_filter_book_authorFullName(self):
        create_book_test_db()
        url = reverse('bookAuthorFullname', args=('author5 sname2',))
        response = self.client.get(url)
        res = [OrderedDict([('title', 'comichorror1'), ('pageCount', 140), ('releaseDate', '2022-12-19'),
        ('authors', ['author4 sname3', 'author5 sname2']), ('genre', 'comic')])]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, res)

    def test_book_create(self):
        url = reverse('bookCreate')
        data = OrderedDict([('title', 'comichorror1'), ('pageCount', 140), ('releaseDate', '2022-12-19'),
        ('authors', ['author4 sname3', 'author5 sname2']), ('genre', 'comic')])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_update(self):
        url = reverse('bookUpdate', args=(1,))
        data = OrderedDict([('title', 'comichorror1'), ('pageCount', 140), ('releaseDate', '2022-12-19'),
        ('authors', ['author4 sname3', 'author5 sname2']), ('genre', 'comic')])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)