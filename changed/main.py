
import os

def change(wallpaper, options):
    center = "gsettings set org.gnome.desktop.background picture-options 'centered'"
    gnome = "gsettings set org.gnome.desktop.background picture-uri"
    wallpaper = ""
    string = "{} {}".format(gnome, wallpaper)
    os.system(string)
    
