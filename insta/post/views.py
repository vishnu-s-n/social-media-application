from django.shortcuts import render,redirect,get_object_or_404
from post.models import Tag,Stream,Follow,Post,Likes
from post.forms import NewPostform
from django.http import HttpResponseRedirect
from django.urls import reverse
from userprofile.models import Profile

# Create your views here.

def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context={
        'post_items': post_items
    }
    return render(request, 'index.html', context)

def NewPost(request):
    user = request.user.id
    tags_objs = []

    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get("picture")
            caption = form.cleaned_data.get("caption")
            tag_form = form.cleaned_data.get("tag")
            
            tag_list = list(tag_form.split(','))
            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tags.set(tags_objs)
            p.save()
            return redirect('index')
    else:
        form = NewPostform()
    context = {
        "form" : form
    }
    return render(request, 'newpost.html', context)

def PostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context ={
        "post" : post
    }
    return render(request, 'postdetail.html', context)

def Like(request,post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked = Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
    post.likes = current_likes
    post.save()
    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))

def favourite(request,post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
    




