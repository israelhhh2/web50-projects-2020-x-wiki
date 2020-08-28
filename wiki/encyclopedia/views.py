from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry_name):
    
    response = util.get_entry(entry_name)

    if response != None:
        return HttpResponse(response)
    else: 
        return HttpResponseNotFound('<h1>404: Page Not Found :/</h1>')

