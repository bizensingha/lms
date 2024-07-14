
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register/',views.register,name="register"),
     path('login/',views.loginpage,name="login"),
      path('home/',views.home,name="home"),
        path('dashboard/', views.dashboard_view, name='dashboard'),
        path('books/', views.books_view, name='books'),
        path('booklist/', views.booklist, name='booklist'),
         path('welcome/', views.welcome, name='welcome'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
     path('add-book/', views.add_book, name='add_book'),
      path('logout/', views.log_out, name='logout'),
       path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
       path('borrowed/', views.borrowed_books, name='borrowed_books'),
       path('return-book/<int:borrow_id>/', views.return_book, name='return_book'),
        path('renew/<int:borrow_id>/', views.renew_loan, name='renew_loan'),
         path('help/', views.help_request, name='help_request'),
          path('requests/', views.requests_view, name='requests'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)