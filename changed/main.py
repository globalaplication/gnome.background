
import os

def change():
    gnome = "gsettings set org.gnome.desktop.background picture-uri"
    wallpaper = ""
    string = "{} {}".format(gnome, wallpaper)
