import webbrowser

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList

Builder.load_string("""
<ProLabel@MDCard>
    orientation: "vertical"
    size_hint_y: None
    height: m3.height+m1.height+2
    MDSeparator:
        height: "2dp"

    MDLabel:
        id:m1
        halign: "center"
        text: root.predmet
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        id:m3
        size_hint_y: None
        markup: True
        text: f"[ref={root.link}]{root.dz}[/ref]"
        on_ref_press:
            import webbrowser 
            webbrowser.open(args[1])
        
        height: self.texture_size[1]

    MDSeparator:
        height: "2dp"



""")


class ProLabel(BoxLayout):
    link = StringProperty()
    predmet = StringProperty()
    dz = StringProperty()
    kab = StringProperty()
    timee = StringProperty()


class carddZ:
    def boxdze(self,url, predmet, dz, kab, timee):
        prLab = ProLabel(dz=dz,link=url, predmet=predmet, kab=kab, timee=timee, size_hint_y=None)
        return prLab