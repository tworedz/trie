import re

from kivy import Config
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from trie import Trie

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '500')


class TrieApp(App):
    def conf(self):
        self.lex = Trie('*')

        with open('data.txt', 'r', encoding='UTF-8') as f:
            self.words = f.read().lower()
            f.close()

        self.words = self.words[:10000]
        self.words = re.split("[:.,;!?\-\[\]\n\t() ]+", self.words)

        for word in self.words:
            self.lex.put(word)

    def on_text(self, instance, value):
        val = value[value.rfind(' ') + 1:].lower()
        temp = self.lex.get(val)
        self.suggest_words.clear_widgets()
        if temp != 0:
            for word in temp[:5]:
                self.suggest_words.add_widget(self.button(word))
            self.suggest_words.opacity = 1 if val else 0
            self.suggest_words.disabled = False if val else True
            x, y = instance.cursor_pos
            self.suggest_words.pos = (x, y - self.suggest_words.height - self.text.font_size)
        else:
            self.suggest_words.add_widget(self.add_word(val))

    def insert(self, instance):
        self.text.text = self.text.text[:self.text.text.rfind(' ') + 1]
        self.text.insert_text(instance.text + ' ')

    def button(self, text):
        return Button(text=text,
                      on_press=self.insert,
                      font_size=16, )

    def add_word(self, text):
        return Button(text=f'{text} не найдено. Добавить?',
                      on_press=self.add_word_to_lex,
                      font_size=16,
                      color=[1, 0, 0, 1])

    def add_word_to_lex(self, instance):
        self.lex.put(instance.text.split()[0])

    def on_focus(self, instance, value):
        instance.focus = True

    def build(self):
        self.conf()
        al = AnchorLayout()
        self.suggest_words = BoxLayout(size_hint=(.3, .3),
                                       opacity=0,
                                       orientation='vertical', )
        self.text = TextInput(size_hint=(.8, .8),
                              font_size=30,
                              hint_text='Вводите: ',
                              background_normal='',
                              foreground_color=[1, 1, 1, 1],
                              background_color=[.43, .43, .43, 1],
                              )
        self.text.bind(text=self.on_text)
        self.text.bind(focus=self.on_focus)

        al.add_widget(self.text)
        al.add_widget(self.suggest_words)
        return al


if __name__ == '__main__':
    TrieApp().run()
