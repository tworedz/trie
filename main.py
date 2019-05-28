from kivy import Config
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 500)


class MyApp(App):
    def func(self, instance):
        self.lbel.text = instance.text

    def build(self):
        box = BoxLayout(orientation='vertical')
        gl = GridLayout(cols=4, rows=4, size_hint=(1, 1))
        self.lbel = Label(text='123', font_size=40, halign='left')
        box.add_widget(self.lbel)
        box.add_widget(gl)
        for x in range(16):
            gl.add_widget(Button(text=str(x), on_press=self.func))
        return box


if __name__ == '__main__':
    MyApp().run()
