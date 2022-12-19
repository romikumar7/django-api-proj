from django.urls import path, include
from books.views import AuthorListView, BookListView, \
        filter_book_title, filter_book_page, filter_book_date, \
        filter_author_name, filter_author_surname, filter_author_email, \
        filter_book_author_id, filter_book_author_name,filter_book_author_surname, filter_book_author_fullname,\
        AuthorCreateView, BookCreateView, AuthorUpdateView, BookUpdateView

urlpatterns = [
    path('book/', BookCreateView.as_view(), name="bookCreate"),
    path('book/<int:book_id>', BookUpdateView.as_view(), name="bookUpdate"),
    path('books/', BookListView.as_view(), name="bookList"),
    path('books/title/<str:title>', filter_book_title, name="bookTitle"),
    path('books/page/<int:pageCnt>', filter_book_page, name='bookPages'),
    path('books/date/<str:dt>', filter_book_date, name='bookPubDate'),
    path('books/author/<int:id>',filter_book_author_id, name='bookAuthorId'),
    path('books/author/name/<str:name>',filter_book_author_name, name='bookAuthorName'),
    path('books/author/surname/<str:surname>', filter_book_author_surname, name='bookAuthorSurname'),
    path('books/author/fullname/<str:fullname>', filter_book_author_fullname, name='bookAuthorFullname'),
    path('authors/', AuthorListView.as_view(), name='authorList'),
    path('authors/name/<str:name>', filter_author_name, name='authorName'),
    path('authors/surname/<str:surname>', filter_author_surname, name='authorSurname'),
    path('authors/email/<str:email>', filter_author_email, name='authorEmail'),
    path('author/',AuthorCreateView.as_view(), name='authorCreate'),
    path('author/<int:author_id>',AuthorUpdateView.as_view(), name='authorUpdate'),
    path('api-auth/', include('rest_framework.urls')),
]