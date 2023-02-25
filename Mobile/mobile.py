from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


class NavButton(Button):
    def __init__(self, screen, direction, goal, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.direction = direction
        self.goal = goal

    def on_press(self):
        self.screen.manager.transition.direction = self.direction
        self.screen.manager.current = self.goal


class Main(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        vl = BoxLayout(orientation='vertical', padding=8, spacing=8)
        hl = BoxLayout()
        text = Label(text='Вибери екран')
        vl.add_widget(NavButton(self, direction='down', goal='first', text="1"))
        vl.add_widget(NavButton(self, direction='left', goal='second', text="2"))
        vl.add_widget(NavButton(self, direction='up', goal='third', text="3"))
        vl.add_widget(NavButton(self, direction='right', goal='fourth', text="4"))
        hl.add_widget(text)
        hl.add_widget(vl)
        self.add_widget(hl)


class First(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        vl = BoxLayout(orientation='vertical', size_hint=(.5, .5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        btn = Button(text='Екран: 1', size_hint=(.5, 1), pos_hint={'left': 0})
        btn_back = NavButton(self, direction='up', goal='main', text='Назад', size_hint=(.5, 1), pos_hint={'right': 1})
        vl.add_widget(btn)
        vl.add_widget(btn_back)
        self.add_widget(vl)


class Second(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        vl = BoxLayout(orientation='vertical', padding=8, spacing=8)
        self.text = Label(text='Екран: 2')
        vl.add_widget(self.text)

        hl_input = BoxLayout(size_hint=(0.8, None), height='30sp')
        lbl = Label(text='Введіть пароль:', halign='right')
        self.input = TextInput(multiline=False)
        hl_input.add_widget(lbl)
        hl_input.add_widget(self.input)
        vl.add_widget(hl_input)

        hl_button = BoxLayout(padding=20, spacing=50, size_hint=(1, 0.2), pos_hint={'center_x': 0.5})
        btn_false = Button(text='OK!')
        btn_back = NavButton(self, direction='right', goal='main', text='Назад')
        hl_button.add_widget(btn_false)
        hl_button.add_widget(btn_back)
        vl.add_widget(hl_button)

        self.add_widget(vl)
        btn_false.on_press = self.change_text

    def change_text(self):
        self.text.text = self.input.text + '? Не спрацювало...'


class Third(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        btn_back = NavButton(self, direction='down', goal='main', text='Назад', size_hint=(1, None), height='40sp')
        test_label = Label(text='Твій власний екран')
        layout.add_widget(test_label)
        layout.add_widget(btn_back)
        self.add_widget(layout)


class Fourth(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        vl = BoxLayout(orientation='vertical', spacing=8)
        label = Label(text='Додаткове завдання', size_hint=(0.3, None))
        text = 'START ' + 'Екран: 3 ' * 200
        btn_back = NavButton(self, direction='left', goal='main', text='Назад', size_hint=(1, .2), pos_hint={'center-x': 0.5})
        self.label = Label(text=text, size_hint_y=None, font_size='24sp', halign='left', valign='top')
        self.label.bind(size=self.resize)
        self.scroll = ScrollView(size_hint=(1, 1))
        self.scroll.add_widget(self.label)

        vl.add_widget(label)
        vl.add_widget(btn_back)
        vl.add_widget(self.scroll)
        self.add_widget(vl)

    def resize(self, *args):
        self.label.text_size = (self.label.width, None)
        self.label.texture_update()
        self.label.height = self.label.texture_size[1]


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Main(name='main'))
        sm.add_widget(First(name='first'))
        sm.add_widget(Second(name='second'))
        sm.add_widget(Third(name='third'))
        sm.add_widget(Fourth(name='fourth'))
        return sm


MyApp().run()