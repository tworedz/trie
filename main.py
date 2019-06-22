import re

from kivy import Config
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from trie import Trie

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '500')


class TrieApp(App):
    def conf(self):
        self.lex = Trie()
        try:
            with open('dict.txt', 'r', encoding='UTF-8') as f:
                tmp = f.read().split('\n')
                for word in tmp:
                    self.lex.put(*word.split())
        except FileNotFoundError:
            with open('data.txt', 'r', encoding='UTF-8') as f:
                self.words = f.read().lower()
                f.close()

            self.words = re.findall("[а-яА-Я]+", self.words)
            for word in self.words:
                self.lex.put(word)

            words = []
            Trie.get_words(self.lex, words)
            with open('dict.txt', 'w', encoding='UTF-8') as f:
                for word in words:
                    f.write(str(word) + '\n')

    def on_text(self, instance, value):
        val = value[value.rfind(' ') + 1:].lower()
        temp = self.lex.get(val)
        self.suggest_words.clear_widgets()
        if temp != 0:
            for word in temp[:5]:
                self.suggest_words.add_widget(self.button(word))
            self.suggest_words.opacity = 1 if val else 0
            x, y = instance.cursor_pos
            self.suggest_words.pos = (x, y - self.suggest_words.height - self.text.font_size)
        else:
            self.suggest_words.add_widget(self.add_word_button(val))

    def insert(self, instance):
        self.text.text = self.text.text[:self.text.text.rfind(' ') + 1]
        self.text.insert_text(instance.text + ' ')

    def button(self, text):
        return Button(text=text.word,
                      on_press=self.insert,
                      font_size=16,
                      size_hint=(None, None),
                      height=30,
                      width=200)

    def add_word_button(self, text):
        txt = f'{text} не найдено.\nДобавить?'
        return Button(text=txt,
                      on_press=self.add_word_to_lex,
                      font_size=16,
                      color=[1, 0, 0, 1],
                      size_hint=(None, None),
                      height=40,
                      width=200,
                      halign='center')

    def add_word_to_lex(self, instance):
        word = instance.text.split()[0]
        self.lex.put(word)
        with open('dict.txt', 'a', encoding='UTF-8') as f:
            f.writelines(f'{word} 1\n')

    def on_focus(self, instance, value):
        instance.focus = True

    def build(self):
        self.conf()
        al = AnchorLayout()
        self.suggest_words = GridLayout(size_hint=(None, None),
                                        opacity=0,
                                        cols=1,
                                        )
        self.text = TextInput(size_hint=(.8, .8),
                              font_size=30,
                              hint_text='Вводите: ',
                              background_normal='',
                              foreground_color=[1, 1, 1, 1],
                              background_color=[.43, .43, .43, .5],
                              )
        self.text.bind(text=self.on_text)
        self.text.bind(focus=self.on_focus)

        al.add_widget(self.text)
        al.add_widget(self.suggest_words)
        return al


if __name__ == '__main__':
    TrieApp().run()
