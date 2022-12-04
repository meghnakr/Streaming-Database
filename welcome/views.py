import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from django.shortcuts import get_object_or_404, render
from django.template import loader
#from .models import Post
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect


from .forms import MediaEditForm

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
    success = {'success': False}
    if request.method == 'POST':
        cnx = sqlConnector().engine
        actors = request.POST.get("actors").split(",")
        directors = request.POST.get("directors").split(",")

        for i in range(len(actors)):
            actors[i] = actors[i].strip()
        
        for i in range(len(directors)):
            directors[i] = directors[i].strip()

       
        session = Session(bind=cnx)
        ###BEGINING OF TRANSACTION###
        session.connection(execution_options={"isolation_level" : "SERIALIZABLE"})

        #add company if needed and get company id
        sp = text("""CALL addCompany(:name, @company_id)""")
        print(sp)
        session.execute(sp, {"name" : request.POST.get("company_name")})
        company_id = session.execute("SELECT @company_id").fetchone()[0]
        print(f"Company Id = {company_id}")

        #get new media id
        sp = text("CALL getNewMediaId(@media_id)")
        session.execute(sp)
        media_id = session.execute("SELECT @media_id").fetchone()[0]
        print(f"media_id: {media_id}")
        #initialize a media object
        m = Media(media_id,
            request.POST.get("media_name"),
            request.POST.get("media_type"),
            request.POST.get("age_rating"),
            request.POST.get("release_year"),
            request.POST.get("language"),
            request.POST.get("date_added"),
            request.POST.get("date_leaving"),
            request.POST.get("genre"),
            request.POST.get("length_in_minutes"),
            company_id)

        #add media object to table
        session.add(m)

        #add actors if needed and get their ids, then link actors to media
        for actor in actors:
            sp = text("""CALL addActor(:act, @actor_id)""")
            session.execute(sp, {"act" : actor})
            actor_id = session.execute("SELECT @actor_id;").fetchone()[0]
            sp = text("""CALL linkActorMedia(:mediaId, :actorId)""")
            session.execute(sp, {"mediaId" : media_id, "actorId" : actor_id})

        #add directors if needed and get their ids, then link directors to media
        for director in directors:
            sp = text("""CALL addDirector(:direct, @director_id)""")
            session.execute(sp, {"direct" : director})
            director_id = session.execute("SELECT @director_id;").fetchone()[0]
            sp = text("""CALL linkDirectorMedia(:mediaId, :directorId)""")
            session.execute(sp, {"mediaId" : media_id, "directorId" : director_id})
        session.commit()
        

        #needed to display popup
        success["success"] = True
 


 
            
    # template = loader.get_template('welcome/submit.html')
    # context = {}
    # return HttpResponse(template.render(context, request))
    return render(request, 'welcome/submit.html', success)


# Delete
def delete(request, id):
    cnx = sqlConnector().engine
    with cnx.connect() as db_conn:
        session = Session(db_conn)        
        # use a filter
            # in the filter, you can filter a certain id
            # call the delete
        if request.method == 'POST':        # post means that we are submitting
            media = session.query(Media).filter(Media.id == id).delete(synchronize_session=False)   # call built-in delete function
        # Commit the session to save changes to the database
        session.commit()   

    return redirect('index')



# Edit
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

        companySubquery = "SELECT Media.id, Media.name, Media.year_of_release "
        
        searchCompany = request.POST.get("company_name")
        actorList = request.POST.get("actors")
        directorList = request.POST.get("directors")

        if (searchCompany is not None) and (not searchCompany == ""):
            companySubquery += "FROM Media JOIN Company ON Media.company_id = Company.id "
        else:
            companySubquery += "FROM Media "
        
        companySubquery += "WHERE "
        
        searchMedia = Media(None, request.POST.get("media_name"),
            request.POST.get("media_type"),
            request.POST.get("age_rating"),
            request.POST.get("release_year"),
            request.POST.get("language"),
            request.POST.get("date_added"),
            request.POST.get("date_leaving"),
            request.POST.get("genre"),
            request.POST.get("length_in_minutes"),
            None)

        companySubquery = getMediaFilters(searchMedia, companySubquery)

        if (searchCompany is not None) and (not searchCompany == ""):
            companySubquery += "Company.name = \"" + searchCompany + "\""
        
        companySubquery = companySubquery.strip()
            
        if companySubquery.endswith("AND"):
            companySubquery = companySubquery[0:len(companySubquery) - 3]
            companySubquery = companySubquery.strip()
        if companySubquery.endswith("WHERE"):
            #companySubquery = companySubquery[0:len(companySubquery) - 5]
            #companySubquery = companySubquery.strip()
            companySubquery = ""
        
        print("Company Subquery: " + companySubquery)

        actorSubquery = ""
        directorSubquery = ""

        if (actorList is not None) and (not actorList == ""):
            actorList = actorList.split(",")
            for i in range(len(actorList)):
                actorList[i] = actorList[i].strip()
            
            actorList = [*set(actorList)] 
            # this gets rid of duplicates by converting the list to a set and then back to a list

            actorSubquery = "SELECT M1.id, M1.name, M1.year_of_release, count(DISTINCT A.id) AS actorCount "
            actorSubquery += "FROM (Media_Actor MA JOIN Actor A ON MA.actor_id = A.id) "
            actorSubquery += "JOIN Media M1 ON MA.media_id = M1.id "
            actorSubquery += "WHERE "
            for actor in actorList:
                actorSubquery += "A.name = \"" + actor + "\" OR "
            
            actorSubquery = actorSubquery.strip()
            if actorSubquery.endswith("OR"):
                actorSubquery = actorSubquery[0:len(actorSubquery) - 2]
                actorSubquery = actorSubquery.strip()
            if actorSubquery.endswith("WHERE"):
                actorSubquery = actorSubquery[0:len(actorSubquery) - 5]
                actorSubquery = actorSubquery.strip()
            
            actorSubquery += " GROUP BY M1.id HAVING actorCount = " + str(len(actorList))
            actorSubquery = "SELECT id, name, year_of_release FROM (" + actorSubquery + ") AS T1"

        if (directorList is not None) and (not directorList == ""):
            directorList = directorList.split(",")
            for i in range(len(directorList)):
                directorList[i] = directorList[i].strip()
            
            directorList = [*set(directorList)] 
            # this gets rid of duplicates by converting the list to a set and then back to a list

            directorSubquery = "SELECT M2.id, M2.name, M2.year_of_release, count(DISTINCT D.id) AS directorCount "
            directorSubquery += "FROM (Media_Director MD JOIN Director D ON MD.director_id = D.id) "
            directorSubquery += "JOIN Media M2 ON MD.media_id = M2.id "
            directorSubquery += "WHERE "
            for director in directorList:
                directorSubquery += "D.name = \"" + director + "\" OR "
            
            directorSubquery = directorSubquery.strip()
            if directorSubquery.endswith("OR"):
                directorSubquery = directorSubquery[0:len(directorSubquery) - 2]
                directorSubquery = directorSubquery.strip()
            if directorSubquery.endswith("WHERE"):
                directorSubquery = directorSubquery[0:len(directorSubquery) - 5]
                directorSubquery = directorSubquery.strip()
            
            directorSubquery += " GROUP BY M2.id HAVING directorCount = " + str(len(directorList))
            directorSubquery = "SELECT id, name, year_of_release FROM (" + directorSubquery + ") AS T2"

        query = companySubquery

        if actorSubquery != "":
            if query == "":
                query = actorSubquery
            elif query.find("WHERE") == -1:
                query = actorSubquery + " WHERE EXISTS (" + query + " WHERE Media.id = T1.id)"
                companySubquery += " WHERE "
            else:
                query = actorSubquery + " WHERE EXISTS (" + query + " AND Media.id = T1.id)"
        
        if directorSubquery != "":
            if query == "":
                query = directorSubquery
            elif companySubquery.find("WHERE") == -1:
                if query.endswith(")"):
                    query = query[0:len(query)-1]
                query = directorSubquery + " WHERE EXISTS (" + query + " WHERE Media.id = T2.id)"
            else:
                if query.endswith(")"):
                    query = query[0:len(query)-1]
                query = directorSubquery + " WHERE EXISTS (" + query + " AND Media.id = T2.id)"
        
        if actorSubquery != "" and directorSubquery != "":
            query += ")"

        query += ";"

        print("Query: " + query)

        cnx = sqlConnector().engine
        with cnx.connect() as db_conn:
            # session = Session(db_conn)
            # statement = select(*attributesToReturn).filter_by(**mediaFilters)
            # result = session.execute(statement).all()
            result = db_conn.execute(query).fetchall()
            print("Result:")
            print(result)
    
    template = loader.get_template('welcome/search.html')
    context = {
        'medias': result
    }
    return HttpResponse(template.render(context, request))

def getMediaFilters(searchMedia, query):

    if (not searchMedia.name == None) and (not searchMedia.name == ""):
        #filters["name"] = searchMedia.name
        query += "Media.name = \"" + searchMedia.name + "\" AND "

    if (not searchMedia.media_type == None) and (not searchMedia.media_type == ""):
        #filters["media_type"] = searchMedia.media_type
        query += "Media.media_type = \"" + searchMedia.media_type + "\" AND "
    
    if (not searchMedia.age_rating == None) and (not searchMedia.age_rating == ""):
        #filters["age_rating"] = searchMedia.age_rating
        query += "Media.age_rating = \"" + searchMedia.age_rating + "\" AND "
    
    if (not searchMedia.year_of_release == None) and (not searchMedia.year_of_release == ""):
        #filters["year_of_release"] = searchMedia.year_of_release
        query += "Media.year_of_release = \"" + searchMedia.year_of_release + "\" AND "
    
    if (not searchMedia.language == None) and (not searchMedia.language == ""):
        #filters["language"] = searchMedia.language
        query += "Media.language = \"" + searchMedia.language + "\" AND "
    
    if (not searchMedia.date_added == None) and (not searchMedia.date_added == ""):
        #filters["date_added"] = searchMedia.date_added
        query += "Media.date_added = \"" + searchMedia.date_added + "\" AND "
    
    if (not searchMedia.date_leaving == None) and (not searchMedia.date_leaving == ""):
        #filters["date_leaving"] = searchMedia.date_leaving
        query += "Media.date_leaving = \"" + searchMedia.date_leaving + "\" AND "
    
    if (not searchMedia.genre == None) and (not searchMedia.genre == ""):
        #filters["Media.genre"] = searchMedia.genre
        query += "Media.genre = \"" + searchMedia.genre + "\" AND "
    
    if (not searchMedia.length_in_minutes == None) and (not searchMedia.length_in_minutes == ""):
        #filters["length_in_minutes"] = searchMedia.length_in_minutes
        query += "Media.length_in_minutes = \"" + searchMedia.length_in_minutes + "\" AND "

    return query

def analyse(request):
    context = {'show_table': False}
    if request.method == "POST":
        groupType = request.POST.get("group-type")
        newLostType = request.POST.get("new-lost-type")
        subsMediaType = request.POST.get("subs-media-type")
        cnx = sqlConnector().engine

        if groupType is not None and groupType != "":
            with cnx.connect() as db_conn:
                if groupType == "company":
                    stmt = "SELECT Company.name AS mth, COUNT(*) AS num FROM Media JOIN Company ON Media.company_id = Company.id GROUP BY Company.id;"
                elif groupType == "actor":
                    stmt = "SELECT Actor.name AS mth, COUNT(*) AS num FROM Media_Actor JOIN Actor ON Media_Actor.actor_id = Actor.id GROUP BY Actor.id;"
                elif groupType == "director":
                    stmt = "SELECT Director.name AS mth, COUNT(*) AS num FROM Media_Director JOIN Director ON Media_Director.director_id = Director.id GROUP BY Director.id;"
                elif groupType == "genre":
                    stmt = "SELECT genre AS mth, COUNT(*) AS num FROM Media GROUP BY genre;"
                result = db_conn.execute(stmt)
                name = []
                num = []
                nameNumpairs = list(result)
                for r in nameNumpairs:
                    name.append(r.mth)
                    num.append(r.num)
                
                print(name)
                print(num)
                context = {
                    'pairs': nameNumpairs,
                    'show_table': True,
                    'header1': groupType,
                    'header2': "The number of media",
                    'col1': json.dumps(name),
                    'col2': json.dumps(num),
                }

        else:
            with cnx.connect() as db_conn:
                stmt = "CALL getNum{}{}({});".format(newLostType, subsMediaType, request.POST.get("number"))
                result = db_conn.execute(stmt)
                mths = []
                subs = []
                mthSubpairs = list(result)
                for r in mthSubpairs:
                    mths.append(r.mth)
                    subs.append(r.num)

                context = {
                    'pairs': mthSubpairs,
                    'show_table': True,
                    'header1': "The past # Months",
                    'header2': "The number of {} {}".format(newLostType, subsMediaType),
                    'col1': json.dumps(mths),
                    'col2': json.dumps(subs),
                }

    template = loader.get_template('welcome/analyse.html')
    return HttpResponse(template.render(context, request))

# view details of media
def details(request, id):
    # query = ("SELECT * FROM " +
    #     "(Media M LEFT OUTER JOIN (Media_Actor MA JOIN Actor A ON MA.actor_id = A.id) ON M.id = MA.media_id) " +
    #     "LEFT OUTER JOIN (Media_Director MD JOIN Director D ON MD.director_id = D.id) ON M.id = MD.media_id " +
    #     "WHERE M.id = " + str(id) + ";")

    mediaCompanyQuery = ("SELECT M.name as media_name, M.date_added, M.date_leaving, M.age_rating, M.language, M.genre, M.length_in_minutes, M.company_id, M.media_type, M.year_of_release, C.name as company_name, C.country" +
                " FROM Media M JOIN Company C ON M.company_id = C.id WHERE M.id = " + str(id) + ";")
    actorQuery = "SELECT * FROM Media_Actor MA JOIN Actor A ON MA.actor_id = A.id WHERE MA.media_id = " + str(id) + ";"
    directorQuery = "SELECT * FROM Media_Director MD JOIN Director D ON MD.director_id = D.id WHERE MD.media_id = " + str(id) + ";" 
    
    cnx = sqlConnector().engine
    with cnx.connect() as db_conn:
        mediaCompany = db_conn.execute(mediaCompanyQuery).fetchall()
        actorList = db_conn.execute(actorQuery).fetchall()
        directorList = db_conn.execute(directorQuery).fetchall()
        print("Result:")
        print(mediaCompany)
        print(actorList)
        print(directorList)
    
    template = loader.get_template('welcome/details.html')
    context = {
        'mediaCompany': mediaCompany,
        'actorList': actorList,
        'directorList': directorList
    }
    return HttpResponse(template.render(context, request))