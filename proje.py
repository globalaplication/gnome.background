# -*- coding: utf-8 -*-
#!/usr/bin/env python
import gi, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio, Gdk
from config import load
class Widget(Gtk.VBox):
    def __init__(beta, pictures):
        Gtk.VBox.__init__(beta, spacing = 5, border_width = 5, halign = Gtk.Align.CENTER)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        filename = pictures, 
        width=120, 
        height=100, 
        preserve_aspect_ratio = False)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        image.set_size_request(10, 10)
        beta.add(image)
class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = 'Wallpaper')
        "linuxta default olan backgrounds klasörünün bilgisayardaki dosya yolu"
        self.backgrounds = "/usr/share/backgrounds"
        "ayarların kaydedildiği config dosyasının bilgisayardaki dosya yolu"
        self.data = load("/var/tmp/data")
        self.set_default_size(1050, 700)
        self.set_border_width(10)
        "walk_dir: klasördeki resimlerin listesi"
        self.walk_dir = []
        "seçili resmin index değeri"
        self.select_picture_index = 0
        
        HeaderBar = Gtk.HeaderBar()
        HeaderBar.set_show_close_button(True)
        HeaderBar.props.title = "Ekran Görüntünü Değiştir"
        self.set_titlebar(HeaderBar)
 
        switch = Gtk.Switch()
        switch.connect("notify::active", self.select_switch)
        switch.set_active(False)
        #HeaderBar.pack_end(switch)
 
        self.ComboBoxText = Gtk.ComboBoxText()
        self.ComboBoxText.set_entry_text_column(0)
        self.ComboBoxText.connect("changed", self.select_combobox)
        for options in ["None", "Centered", "Zoom", "Spanned", "Wallpaper", "Scaled", "Stretched"]:
            self.ComboBoxText.append_text(options)
        HeaderBar.pack_end(self.ComboBoxText)

        if self.data.get("index") == "None":  self.ComboBoxText.set_active(int(index))
        else:
            self.ComboBoxText.set_active(int(self.data.get("index")))
             
        Button = Gtk.Button(label = "Cancel")
        Button.connect('clicked', self.info)
        HeaderBar.pack_start(Button)

        ScrolledWindow = Gtk.ScrolledWindow(visible = True)
        self.add(ScrolledWindow)
       
        self.FlowBox = Gtk.FlowBox()
        self.FlowBox.connect("child-activated", self.select_picture)
        self.FlowBox.set_valign(Gtk.Align.START)
        ScrolledWindow.add(self.FlowBox)
        
        for picture in os.walk(self.backgrounds):
            for test in picture[2]:
                if test.endswith(".jpg") is True:
                    object = Widget( "{}/{}".format(picture[0], test) )
                    self.walk_dir.append("{}/{}".format(picture[0], test))
                    self.FlowBox.add(object)

    def select_combobox(self, combo):
        text = combo.get_active_text()
        self.set_options(text.lower())
        if (text is not None):
            self.data.set("duzen", text.lower())
            self.data.set("index", int(combo.get_active()))
        print ("walpaper select index", text)

    def select_picture(self, beta, picture): 
        select_picture_file = self.walk_dir[picture.get_index()]
        self.select_picture_index = picture.get_index()
        self.set_wallpaper(select_picture_file)
        print ("select_picture_index", self.select_picture_index)

    def select_switch(self, switch, gparam):
        if switch.get_active():
            self.set_options(self.data.get("duzen"))
        else:
            self.set_options("none")

    def set_wallpaper(self, picture):
        command = Gio.Settings.new("org.gnome.desktop.background")
        command.set_string("picture-uri", picture)
        command.apply()

    def set_options(self, config = "none"):
        command = Gio.Settings.new("org.gnome.desktop.background")
        command.set_string("picture-options", config)
        command.apply()

    def info(self, widged, data = None):
        return 

window = MainWindow()
window.connect('delete-event', Gtk.main_quit)
window.show_all()
Gtk.main()



