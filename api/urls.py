from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet,custom_login_view
from . import views
router = DefaultRouter()
router.register('documents',DocumentViewSet)
urlpatterns = [path('',include(router.urls)),]
urlpatterns += [
    path('technologies/', views.get_technologies),
]
urlpatterns+=[path('domain/',views.get_domain),]
urlpatterns+=[path('level/',views.get_level),]
urlpatterns+=[path('aiModel/',views.get_aiModel),]
urlpatterns+=[path('yrsExp/',views.get_yrsExp),]
urlpatterns+=[path('store_selection/',views.selection_storage,name="selection_storage"),]
urlpatterns+=[path("custom-login/",views.custom_login_view, name="custom_login"),]
urlpatterns+=[path("response/",views.response,name="response"),]
urlpatterns += [path("process_pdfs/",views.process_pdfs),]
urlpatterns += [path("transcribe_audio/",views.transcribe_audio,name="transcribe_audio"),]
urlpatterns += [path("generate_questions/",views.generate_questions,name="generate_questions"),]
