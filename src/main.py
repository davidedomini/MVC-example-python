from kivy.app import App
from model.User import UserModel
from view.RegistrationUi import RegistrationView
from controller.RegistrationController import RegistrationController

class RegistrationApp(App):
    def build(self):
        model = UserModel()
        controller_holder = {}

        def on_submit():
            controller_holder["c"].handle_submit()

        view = RegistrationView(model=model, on_submit=on_submit)
        controller = RegistrationController(model=model, view=view)
        controller_holder["c"] = controller
        return view


if __name__ == "__main__":
    RegistrationApp().run()