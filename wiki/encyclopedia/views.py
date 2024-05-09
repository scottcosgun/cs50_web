from django.shortcuts import render
from markdown2 import Markdown
from http.client import HTTPResponse
import random

from . import util

# Converd md to html if md file exists
def to_html(title):
    file = util.get_entry(title)
    markdowner = Markdown()
    if file:
        return markdowner.convert(file)
    return None

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Display a wiki entry if it exists
def entry(request, title):
    content = to_html(title)
    if not content:
        return render(request, "encyclopedia/error.html", {
            "message": "The page you requested does not exist"
        })
    return render(request, "encyclopedia/entry.html",{
        "title": title,
        "content": content
    })

# Search for a wiki entry
def search(request):
    if request.method == "POST":
        find = request.POST['q']
        content = to_html(find)
        # If an entry matchces the search query exactly, display it
        if content:
                return render(request, "encyclopedia/entry.html",{
            "title": find,
            "content": content
        })
        # List all entries that contain the query as a substring
        results = [entry for entry in util.list_entries() if find.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "results": results
        })

# Add a new wiki entry
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    title = request.POST['title']
    content = request.POST['content']
    # Return error message if an entry already exists with this title
    if util.get_entry(title):
        return render(request, "encyclopedia/error.html", {
            "message": "A Wiki entry with this title already exists."
        })
    util.save_entry(title, content)
    html_content = to_html(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def rand(request):
    choice = random.choice(util.list_entries())
    content = to_html(choice)
    return render(request, "encyclopedia/entry.html", {
        "title": choice,
        "content": content
    })