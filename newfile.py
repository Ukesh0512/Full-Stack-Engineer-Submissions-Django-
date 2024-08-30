#Project Structure
note_taking_api/
note_taking_api/
settings.py
urls.py
wsgi.py
__init__.py
apps/
notes/
models.py
views.py
serializers.py
urls.py
__init__.py
__pycache__/
requirements.txt
README.md

#models.py
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
#serializers.py
from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'body', 'created_at', 'updated_at']
        
#views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Note
from .serializers import NoteSerializer

class NoteCreateView(APIView):
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class NoteDetailView(APIView):
    def get(self, request, pk):
        note = Note.objects.get(pk=pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk):
        note = Note.objects.get(pk=pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class NoteQueryView(APIView):
    def get(self, request):
        title = request.GET.get('title')
        if title:
            notes = Note.objects.filter(title__icontains=title)
        else:
            notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
        
#urls.py
from django.urls import path
from .views import NoteCreateView, NoteDetailView, NoteQueryView

urlpatterns = [
    path('notes/', NoteCreateView.as_view()),
    path('notes/<int:pk>/', NoteDetailView.as_view()),
    path('notes/', NoteQueryView.as_view()),
]

#settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'notes.apps.NotesConfig',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'note_taking_api',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

#requirements.txt
Django==3.2.5
djangorestframework==3.12.4
psycopg2-binary==2.9.3

#README.md
#To set up the project locally:

1. Clone the repository: `git clone https://github.com/your_username/note_taking_api.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Create a PostgreSQL database and update the `DATABASES` settings in `settings.py`
4. Run the migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`
6. Use a tool like `curl` or a REST client to test the API endpoints                                                                
#Swagger Documentation
#To integrate Swagger, I'll use the drf-yasg library. Here's an example of how to add Swagger documentation to the API:       
#swagger.py  
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Note Taking API",
        default_version='v1',
        description="A simple note-taking API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)   

#urls.py
from django.urls import path, include
from rest_framework import routers
from .views import NoteCreateView, NoteDetailView, NoteQueryView
from .swagger import schema_view

router = routers.DefaultRouter()
router.register(r'notes', NoteCreateView, basename='notes')

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]                