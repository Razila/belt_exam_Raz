from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(
            request.POST.get('password').encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            user_name=request.POST['user_name'],
            email=request.POST['email'],
            password=pw_hash
        )
        messages.success(request, "You have successfully registered!")
        return redirect('/wishes')


def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST.get('email'), request.POST.get('password')):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/wishes')


def logout(request):
    request.session.clear()
    return redirect('/')


def wishes(request):
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id),
        'wishes': User.objects.get(id=user_id).wishes.all(),
        'granted_wishes': Granted_wish.objects.all()
    }
    return render(request, 'wishes.html', context)


def wish_stats(request):
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id),
        'granted_wishes': Granted_wish.objects.count(),
        'user_wishes': User.objects.get(id=user_id).granted_wishes.count(),
        'wishes_limbo': User.objects.get(id=user_id).wishes.count()
    }
    return render(request, 'stats.html', context)


def new(request):
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'new.html', context)

def new_wish(request):
    if request.method == 'POST':
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('wishes/new')
        else:
            Wish.objects.create(item=request.POST['item'], description=request.POST['description'], user=User.objects.get(id=request.POST['user_id']))
            return redirect('/wishes')
    else:
        return redirect('/')



def grant_wish(request):
    if request.method == 'POST':
        Granted_wish.objects.create(item=request.POST['item'], user=User.objects.get(id=request.POST['user_id']), date_added=request.POST['wish_created'])
        wish = Wish.objects.get(id=request.POST['wish_id'])
        wish.delete()
        return redirect('/wishes')
    else:
        return redirect("/")


def edit_wish(request, wish_id):
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id),
        'wish': Wish.objects.get(id=wish_id)
    }
    return render(request, 'edit.html', context)

def update_wish(request, wish_id):
    if request.method == 'POST':
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/edit')
        else:
            wish = Wish.objects.get(id=wish_id)
            wish.item = request.POST['item']
            wish.description = request.POST['description']
            wish.save()
            return redirect('/wishes')
    else:
        return redirect('/')


def remove_wish(request):
    if request.method == 'POST':
        wish = Wish.objects.get(id=request.POST['wish_id'])
        wish.delete()
        return redirect('/wishes')
    else:
        return redirect('/')


def like_wish(request):
    if request.method == 'POST':
        granted = Granted_wish.objects.get(id=request.POST['grant_id'])
        user = User.objects.get(id=request.POST['user_id'])
        if granted.user_id == user.id:
            messages.error(request, "Users cannot enter likes for their own wish")
            return redirect('/wishes')
        if len(granted.likes.filter(id=request.POST['user_id'])) > 0:
            messages.error(request, "You already hit like on this one.")
            return redirect('/wishes')
        else:
            granted.likes.add(user)
            return redirect('/wishes')
