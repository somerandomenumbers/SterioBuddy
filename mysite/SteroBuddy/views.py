
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader 
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Song, User_prof, List, ListCat
from pprint import pprint
import requests
import random


# Create your views here.

@login_required(login_url="/SteroBuddy/login")
def home(request):
    try:
        songs = random.sample(list(Song.objects.all()), 3)
        print(songs)
    except:
        songs = []

    return render(request, "sterobuddy/home.html", {'songs':songs})

def loginpage(request):
    return render(request, "sterobuddy/login.html" )

def signup(request):
     return render(request, "sterobuddy/signup.html" )

def athentic(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('SteroBuddy:home')
    else:
        return redirect('/SteroBuddy/login')

def new_ac(request):
    username = request.POST["user_name"]
    pword = request.POST["password"]
    user = User.objects.create_user(username=username, password=pword)

    if user:
        login(request, user)
    return redirect('SteroBuddy:home')
    
@login_required(login_url="/SteroBuddy/login")
def newsong(request):
    fav_songs = request.user.fav_songs.all()
    print(fav_songs)
    return render(request, "sterobuddy/newsong.html", {'fav_songs':fav_songs} )

@login_required(login_url="/SteroBuddy/login")
def findsong(request):
    song_nm = request.GET['songnm']
    user = request.user
    try:
        song_n = Song.objects.get(song_name=song_nm)
        song_n.fans.add(user)
        return redirect('/SteroBuddy/newsong', songnm=song_nm)
    except:
        
        url = f'http://ws.audioscrobbler.com/2.0/?method=track.search&track={song_nm}&api_key=d1b9ac6fed8ace6dbafa0a7bc1c47ec0&format=json'

        print(url)
        response = requests.get(url).json()
        tracks = response['results']['trackmatches']['track']
        MBsong = []
        for track in tracks:
            print(track['name'], track['artist'])
            Msong = (f"{track['name']}", f"{track['artist']}")
            MBsong.append(Msong)


       
        return render(request, "sterobuddy/songselct.html", {'MBsong':MBsong})

       
        # pprint((response['recordings'][0]['releases'][0]['media'][0]['track'][0]['title']))


@login_required(login_url="/SteroBuddy/login")
def addingsong(request, track, artist):
    print(Song.objects.all()) 
    
    try:
        song = Song.objects.get(song_name=track)
        user = request.user
        song.fans.add(user)
        return redirect(f'/SteroBuddy/findsong?songnm={song}')
    except:
        Lsong = Song(song_name=track)
        Lsong.save()
        return redirect(f'/SteroBuddy/findsong?songnm={track}')
            
       
        


@login_required(login_url="/SteroBuddy/login")
def findcommonusers(request):
    fav_songs = request.user.fav_songs.all()
    ids = fav_songs.only('id')
    # common_users = song.fans.all()
    common_songs = Song.objects.filter(
        fans__in = User.objects.filter(fav_songs__in=fav_songs)
        .exclude(id=request.user.id).distinct()).distinct()
    print(common_songs)
    new_songs = common_songs.exclude(id__in=ids)
    print(new_songs)
    return render(request, "sterobuddy/foundsong.html", {'new_song':new_songs})

@login_required(login_url="/SteroBuddy/login")
def mixes(request):
    return render(request, "sterobuddy/mixes.html")



@login_required(login_url="/SteroBuddy/login")
def postmix(request):
    nm = request.GET['name']
    cmix = List(name=nm, auther=request.user)
    cmix.save()
    cmix_id = cmix.id
    
    return redirect('SteroBuddy:songmix',cmix_id=cmix_id)


@login_required(login_url="/SteroBuddy/login")
def songmix(request, cmix_id):
    cmix = List.objects.get(id=cmix_id)
    return  render(request, "sterobuddy/creatingmix.html", {'mix':cmix})

@login_required(login_url="/SteroBuddy/login")
def mix(request, cmix_id):
    
    cmix = List.objects.get(id=cmix_id)
    print(cmix.name)
    song_nm = request.GET['songnm']
    user = request.user
    song_n = Song.objects.filter(song_name__icontains=song_nm)[0]
    cmix.songs.add(song_n)
    cmix.save()
    cmix_id = cmix.id

    return redirect('SteroBuddy:songmix', cmix_id=cmix_id)


@login_required(login_url="/SteroBuddy/login")
def findlist(request):

    vlist = List.objects.all()
    list1, list2, list3 = [], [], []
    for i, item in enumerate(vlist):
        if i % 3 == 0:
            list1.append(item)
        elif (i - 1)%3 == 0:
            list2.append(item)
        elif (i - 2) % 3 == 0:
            list3.append(item)

    return render(request, "sterobuddy/findlist.html", {'list':vlist, 'list1':list1, 'list2':list2, 'list3':list3})

def trash(request, list_id):
    tlist = List.objects.get(id=list_id)
    print(tlist)
    tlist.delete()
    return redirect('SteroBuddy:findlist')


def logout_(request):
    logout(request)
    return redirect('SteroBuddy:signup')
    







