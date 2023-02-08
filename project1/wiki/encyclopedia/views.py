from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.http import Http404
from django.urls import reverse
from django import forms
from markdown2 import Markdown
import random

from . import util

#init

markdowner = Markdown()

class newEntryForm(forms.Form):
    entry = forms.CharField( label='', widget = forms.Textarea( attrs = { 'name':'entry', 'placeholder':'entry in markdown', 'style':'height:500px; placeholder:markdown entry;' } ), required = False )


#main chunk

def index(request):
    lentries = util.list_entries()
    entries = []
    search = ""
    title = "All pages"
    if( request.method == "POST" ):
        search = request.POST['q']
        title = "Search results:"
    for entry in lentries:
        if search == entry:
            return get_page(request, entry)
        if search in entry:
            entries.append( markdowner.convert( f"[{entry}](/wiki/{entry})" ) )
    return render(request, "encyclopedia/index.html", {
        "title": title,
        "entries": entries
    })

def get_page(request, title):
    if title=="randompagegenerator":
        lentries = util.list_entries()
        return HttpResponseRedirect( reverse( 'get_page', args=[lentries[random.randint(0,len(lentries)-1)]] ) )
    content = util.get_entry(title)
    if content is None:
        raise Http404("Page not found")
    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": markdowner.convert( content )
    })

def edit(request, type):
    error = ""
    input_value = " "
    form = newEntryForm()
    if type!="addanewpage":
        if util.list_entries().count(type)==0:
            raise Http404("Page not found")
        input_value = type
    if request.method == "POST":
        form = newEntryForm( request.POST );
        if form.is_valid():
            title = request.POST["title"]
            entry = form.cleaned_data["entry"]
            if title=="":
                error = "please fill out title"
            elif type=="addanewpage" and util.list_entries().count(title):
                error = "title exists"
            else:
                file = open( f"entries/{title}.md", 'w' )
                file.write(entry)
                file.close()
                return HttpResponseRedirect( reverse( 'get_page', args=[title] ) )
    return render(request, "encyclopedia/edit.html", {
        "title": type,
        "isadd": type=="addanewpage",
        "error": error,
        "input_value": input_value, 
        "form": form
    })
