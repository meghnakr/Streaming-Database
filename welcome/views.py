from django.http import HttpResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from django.shortcuts import get_object_or_404, render
from django.template import loader
#from .models import Post
from django import forms


from welcome.db import sqlConnector
from welcome.models import *
#class PostForm(forms.ModelForm):
 #   class Meta:
  #      model = Post

def index(request):

    cnx = sqlConnector().engine
    with cnx.connect() as db_conn:
        stmt = select(Media)

        result = db_conn.execute(stmt).fetchall()

    # Do something with the results
    template = loader.get_template('welcome/index.html')
    context = {
        'medias': result
    }
    return HttpResponse(template.render(context, request))

def submit(request):
    if request.method == 'POST':
        m = Media(request.POST.get("media_name"),
            request.POST.get("media_type"),
            request.POST.get("age_rating"),
            request.POST.get("release_year"),
            request.POST.get("language"),
            request.POST.get("date_added"),
            request.POST.get("date_leaving"),
            request.POST.get("genre"),
            request.POST.get("length_in_minutes"))
        print(request.POST.get("age_rating"))
        print(m.age_rating)

        cnx = sqlConnector().engine
        with cnx.connect() as db_conn:
            print("test")
            print(m.age_rating)
            session = Session(db_conn)
            session.add(m)
            session.commit()
            
    template = loader.get_template('welcome/submit.html')
    context = {}
    return HttpResponse(template.render(context, request))

def edit(request):
    #post=get_object_or_404(request.POST)


    template = loader.get_template('welcome/edit.html')
    context = {}
    return HttpResponse(template.render(context, request))

# def put_media(requestx):
#     if request.method == 'POST':
#         m = Media(name="Admin", id=5, age=20)
#         print(m)


#         cnx = sqlConnector().engine
#         with cnx.connect() as db_conn:
#             session = Session(db_conn)
#             session.add(m)

#             session.commit()

#             return HttpResponse("Please go to Welcome page to reconfirm user has been added.")

#     return render(request, 'submit.html')

def search(request):
    result = []
    if request.method == 'POST':
        
        searchMedia = Media(request.POST.get("media_name"),
            request.POST.get("media_type"),
            request.POST.get("age_rating"),
            request.POST.get("release_year"),
            request.POST.get("language"),
            request.POST.get("date_added"),
            request.POST.get("date_leaving"),
            request.POST.get("genre"),
            request.POST.get("length_in_minutes"))

        searchCompany = request.POST.get("company_name")

        mediaFilters = getMediaFilters(searchMedia)

        attributesToReturn = [Media.id, Media.name, Media.year_of_release]
        
        cnx = sqlConnector().engine
        with cnx.connect() as db_conn:
            session = Session(db_conn)
            statement = select(*attributesToReturn).filter_by(**mediaFilters)
            result = session.execute(statement).all()
            print("Result:")
            print(result)
    
    template = loader.get_template('welcome/search.html')
    context = {
        'medias': result
    }
    return HttpResponse(template.render(context, request))

def getMediaFilters(searchMedia):
    filters = {}
    if (not searchMedia.name == None) and (not searchMedia.name == ""):
        filters["name"] = searchMedia.name
    
    if (not searchMedia.media_type == None) and (not searchMedia.media_type == ""):
        filters["media_type"] = searchMedia.media_type
    
    if (not searchMedia.age_rating == None) and (not searchMedia.age_rating == ""):
        filters["age_rating"] = searchMedia.age_rating
    
    if (not searchMedia.year_of_release == None) and (not searchMedia.year_of_release == ""):
        filters["year_of_release"] = searchMedia.year_of_release
    
    if (not searchMedia.language == None) and (not searchMedia.language == ""):
        filters["language"] = searchMedia.language
    
    if (not searchMedia.date_added == None) and (not searchMedia.date_added == ""):
        filters["date_added"] = searchMedia.date_added
    
    if (not searchMedia.date_leaving == None) and (not searchMedia.date_leaving == ""):
        filters["date_leaving"] = searchMedia.date_leaving
    
    if (not searchMedia.genre == None) and (not searchMedia.genre == ""):
        filters["genre"] = searchMedia.genre
    
    if (not searchMedia.length_in_minutes == None) and (not searchMedia.length_in_minutes == ""):
        filters["length_in_minutes"] = searchMedia.length_in_minutes
    return filters

def analyse(request):
    context = {}
    if request.method == "POST":
        cnx = sqlConnector().engine
        with cnx.connect() as db_conn:
            result = db_conn.execute("CALL getNumNewSubs(6);")
            context = {
                'medias': result
            }

    template = loader.get_template('welcome/analyse.html')
    return HttpResponse(template.render(context, request))