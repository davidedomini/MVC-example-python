from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from model.User import UserModel
from typing import List, Callable

class RegistrationView(BoxLayout):
    user_count = NumericProperty(0)      
    status_text = StringProperty("")      

    def __init__(self, model: UserModel, on_submit: Callable[[], None], **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=20, **kwargs)
        self.model = model
        self.on_submit = on_submit

        self.header = Label(text="Registration", font_size=22, size_hint=(1, None), height=36)
        self.add_widget(self.header)

        self.user_count_label = Label(text=self._count_text(), size_hint=(1, None), height=24)
        self.add_widget(self.user_count_label)

        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.email_input = TextInput(hint_text="Email", multiline=False)
        self.birthdate_input = TextInput(hint_text="Birth date (gg/mm/aaaa)", multiline=False)
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True)

        for w in (self.username_input, self.email_input, self.birthdate_input, self.password_input):
            self.add_widget(w)

        self.status_label = Label(text="", size_hint=(1, None), height=20)
        self.add_widget(self.status_label)

        btn = Button(text="Sign Up", size_hint=(1, None), height=44)
        btn.bind(on_press=lambda *_: self.on_submit())
        self.add_widget(btn)

        # Subscribe as an observer
        self.model.add_observer(self._on_model_changed)
        self._on_model_changed(self.model)  # Counter init

        self.bind(user_count=lambda *_: self._refresh_count_label())
        self.bind(status_text=lambda *_: self._refresh_status())

    
    def get_form_data(self) -> dict:
        return {
            "username": self.username_input.text.strip(),
            "email": self.email_input.text.strip(),
            "birthdate": self.birthdate_input.text.strip(),
            "password": self.password_input.text,
        }

    def clear(self):
        self.username_input.text = ""
        self.email_input.text = ""
        self.birthdate_input.text = ""
        self.password_input.text = ""
        self.status_text = ""

    def show_popup(self, title: str, message: str):
        Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4)).open()

    def set_status(self, msg: str):
        self.status_text = msg

    # Observer callback
    def _on_model_changed(self, model: UserModel):
        self.user_count = model.count

    # UI helpers
    def _count_text(self) -> str:
        return f"Registered users: {self.user_count}"

    def _refresh_count_label(self):
        self.user_count_label.text = self._count_text()

    def _refresh_status(self):
        self.status_label.text = self.status_text
