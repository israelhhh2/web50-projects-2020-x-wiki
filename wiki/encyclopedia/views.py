from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from random import choice
from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'rows': 5
    }))
    entry_text = forms.CharField(label="Entry Text", widget=forms.Textarea(attrs={
        "class": 'form-control',
        "rows" :10, 
        "cols" :10
        }))


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

def new_page(request):
    message_submission = False
    # Get all entries into a list
    entries = []
    for entry in util.list_entries():
            entries.append(entry)
            print(f"{entry} was added to entries array")
    print(entries)


    if request.method == "POST":
        form_data = NewEntryForm(request.POST)
        

        if form_data.is_valid():
            title = form_data.cleaned_data['title']
            entry_exist = False
            message_submission = False
            if title in entries:
                entry_exist = True
                return render(request, "entry.html", {
                    "form": form_data,
                    "entry_exist": entry_exist
                })
            else:
                textarea = form_data.cleaned_data['entry_text']           
                util.save_entry(title, textarea)
                message_submission = True

        else:
            return render(request, "entry.html", {
                "form": form_data,
                # "entry_exist": entry_exist
            })
    return render(request, "entry.html", {
        "form": NewEntryForm(),
        "message_submission": message_submission
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = choice(entries)
    return redirect("entry_title", entry_name=random_entry)
    return HttpResponse(random_entry)

def search(request):
    if request.method == "GET":

        search_input = request.GET.get('q')
        get_entry = util.get_entry(search_input)

        if(get_entry is not None):
            return HttpResponseRedirect(reverse(f"wiki/{search_input}"))
            # response = redirect(f"wiki/{search_input}")
            # return response
        
        else:
        
            string_entries = []
            for entry in util.list_entries():
                if search_input.upper() in entry.upper():
                    string_entries.append(entry)

            return render(request, "encyclopedia/index.html", {
                "search": True, 
                "search_input": search_input,
                "string_entries": string_entries

            })