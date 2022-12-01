import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from django.shortcuts import get_object_or_404, render
from django.template import loader
#from .models import Post
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .forms import MediaEditForm

from welcome.db import sqlConnector
from welcome.models import *
#class PostForm(forms.ModelForm):
 #   class Meta:
  #      model = Post

def index(request):

    cnx = sqlConnector().engine
    print("test1")
    with cnx.connect() as db_conn:
        print("test")
        stmt = select(Media)

        result = db_conn.execute(stmt).fetchall()

    # Do something with the results
    template = loader.get_template('welcome/index.html')
    context = {
        'medias': result
    }
    return HttpResponse(template.render(context, request))

def submit(request):
    success = {'success': False}
    if request.method == 'POST':
        cnx = sqlConnector().engine
        actors = request.POST.get("actors").split(",")
        directors = request.POST.get("directors").split(",")

        #add actors if needed
        for actor in actors:
            with cnx.connect() as db_conn:
                sp = f"""CALL addActor("{actor}");"""
                print(sp)
                session = Session(db_conn)
                session.execute(sp)
                session.commit()

        #add directors if needed
        for director in directors:
            with cnx.connect() as db_conn:
                sp = f"""CALL addDirector("{director}");"""
                print(sp)
                session = Session(db_conn)
                session.execute(sp)
                session.commit()

        #add company if needed
        company_id = 0
        with cnx.connect() as db_conn:
            sp = f"""CALL addCompany("{request.POST.get("company_name")}");"""
            print(sp)
            session = Session(db_conn)
            session.execute(sp)
            session.commit()
            get_company_id = f"""SELECT C.id from Company C WHERE name="{request.POST.get("company_name")}";"""
            company_id = db_conn.execute(get_company_id).fetchall()[0]

        

        m = Media(request.POST.get("media_name"),
            request.POST.get("media_type"),
            request.POST.get("age_rating"),
            request.POST.get("release_year"),
            request.POST.get("language"),
            request.POST.get("date_added"),
            request.POST.get("date_leaving"),
            request.POST.get("genre"),
            request.POST.get("length_in_minutes"),
            company_id)


        with cnx.connect() as db_conn:
            print("test")
            print(m.age_rating)
            session = Session(db_conn)
            session.add(m)
            session.commit()
        success["success"] = True
 


 
            
    # template = loader.get_template('welcome/submit.html')
    # context = {}
    # return HttpResponse(template.render(context, request))
    return render(request, 'welcome/submit.html', success)




def edit(request, id):
    cnx = sqlConnector().engine
    with cnx.connect() as db_conn:
        session = Session(db_conn)
        media = session.query(Media).get(id)

        # obj = get_object_or_404(Media, pk=id)
        # if this is a POST request we need to process the form data
        if request.method == 'POST':        # post means that we are submitting
            # create a form instance and populate it with data from the request:
            form = MediaEditForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                # grab data from form.cleaned and plug it into my sql alchemy object
                # Submit the updated properties
                media.name = form.cleaned_data["name"]
                media.media_type = form.cleaned_data["media_type"]
                media.age_rating = form.cleaned_data["age_rating"]
                media.year_of_release = form.cleaned_data["year_of_release"]
                media.language = form.cleaned_data["language"]
                media.date_added = form.cleaned_data["date_added"]
                media.date_leaving = form.cleaned_data["date_leaving"]
                media.genre = form.cleaned_data["genre"]
                media.length_in_minutes = form.cleaned_data["length_in_minutes"]



                # Commit the data
                session.add(media)
                session.commit()   
                return HttpResponseRedirect(reverse('index'))

        # if a GET (or any other method) we'll create a blank form
        else:
            # make a dictionary 
            formFields = dict(name = media.name, media_type = media.media_type,
            age_rating = media.age_rating, year_of_release = media.year_of_release,
            language = media.language, date_added = media.date_added, date_leaving = media.date_leaving,
            genre = media.genre, length_in_minutes = media.length_in_minutes)
            form = MediaEditForm(formFields)

            # fill with initial values

    return render(request, 'welcome/edit.html', {'form': form})






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
    context = {'show_table': False}
    if request.method == "POST":
        subsType = request.POST.get("subs-type")
        cnx = sqlConnector().engine
        with cnx.connect() as db_conn:
            stmt = "CALL getNum{}Subs({});".format(subsType, request.POST.get("number"))
            result = db_conn.execute(stmt)
            mths = []
            subs = []
            mthSubpairs = list(result)
            for r in mthSubpairs:
                mths.append(r.mth)
                subs.append(r.num)

            context = {
                'medias': mthSubpairs,
                'show_table': True,
                'mths': json.dumps(mths),
                'subs': json.dumps(subs),
                'subsType': subsType
            }

    template = loader.get_template('welcome/analyse.html')
    return HttpResponse(template.render(context, request))