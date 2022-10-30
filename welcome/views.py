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
        m = Media(name="Admin", id=5, age=20)
        print(m)

        cnx = sqlConnector().engine
        with cnx.connect() as db_conn:
            session = Session(db_conn)
            session.add(m)

            session.commit()

            return HttpResponse("Please go to Welcome page to reconfirm user has been added.")

    return render(request, 'submit.html')