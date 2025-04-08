from django.shortcuts import render, get_object_or_404
from .models import blogpost  # Ensure this matches the model name

# Home Page
def index(request):
    myposts= blogpost.objects.all()
    print(myposts)
    return render(request, 'blog/index.html', {'myposts': myposts})



# Blog Post Page
def blogpost_view(request, id):  
    post = get_object_or_404(blogpost, post_id=id)  # Safe way to get object
    return render(request, 'blog/blogpost.html', {'post': post})

