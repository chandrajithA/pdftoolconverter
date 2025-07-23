from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="startingpage"),  
    path('word_to_pdf', views.word_to_pdf, name='word_to_pdf'),
    path('pdf_to_word', views.pdf_to_word, name='pdf_to_word'),
    path('compress_pdf', views.compress_pdf, name='compress_pdf'),
    path('compress_word', views.compress_word, name='compress_word'),
    path('merge_pdf', views.merge_pdf, name='merge_pdf'),
    path('split_pdf', views.split_pdf, name='split_pdf'),
]