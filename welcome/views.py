from django.http import HttpResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from django.shortcuts import render
from django.template import loader

from welcome.db import sqlConnector
from welcome.models import Media

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
    template = loader.get_template('welcome/submit.html')
    context = {}
    return HttpResponse(template.render(context, request))

def edit(request):
    template = loader.get_template('welcome/edit.html')
    context = {}
    return HttpResponse(template.render(context, request))

def put_media(request):
    if request.method == 'POST':
        m = Media(request.POST.get("media_name"),
                request.POST.get("media_type"),
                request.POST.get("age_rating"),
                request.POST.get("release_year"),
                request.POST.get("languagae"),
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

#         cnx = sqlConnector().engine
#         with cnx.connect() as db_conn:
#             session = Session(db_conn)
#             session.add(m)

#             session.commit()

#             return HttpResponse("Please go to Welcome page to reconfirm user has been added.")

#     return render(request, 'submit.html')

def search(request):
    template = loader.get_template('welcome/search.html')
    context = {}
    return HttpResponse(template.render(context, request))