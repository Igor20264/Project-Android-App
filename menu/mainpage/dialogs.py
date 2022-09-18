from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog

Builder.load_string("""
<dialog>
    orientation: "vertical"
    size_hint_y: None
    title: "Исправь эти предметы"
    text: root.valse
    radius: [20, 7, 20, 7]
""")

class dialog(MDDialog):
    valse = StringProperty()