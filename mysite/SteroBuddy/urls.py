from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path

app_name = "SteroBuddy"

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.loginpage, name="login"),
    path("signup", views.signup, name="signup"),
    path("athentic", views.athentic, name="athentic"),
    path("signup", views.signup, name="signup"),
    path("new_ac", views.new_ac, name="new_ac"),
    path("newsong", views.newsong, name="newsong"),
    path("findsong", views.findsong, name="findsong"),
    path("findingsong", views.findcommonusers, name="findingsong"),
    path("mixes", views.mixes, name="mixes"),
    path("mixes/<int:cmix_id>", views.mixes, name="mixes"),
    path("mix/<int:cmix_id>", views.mix, name="mix"),
    path("postmix", views.postmix, name="postmix"),
    path("songmix/<int:cmix_id>", views.songmix, name="songmix"),
    path("findlist", views.findlist, name="findlist"),
    path("trash/<int:list_id>", views.trash, name="trash"),
    path("logout", views.logout_, name="logout"),
    path("addingsong/<str:track>/<str:artist>", views.addingsong, name="addingsong")


]