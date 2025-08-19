from model.User import UserModel, User
from view.RegistrationUi import RegistrationView

class RegistrationController:
    def __init__(self, model: UserModel, view: RegistrationView):
        self.model = model
        self.view = view

    def handle_submit(self):
        data = self.view.get_form_data()

        # User data validation
        errors = []
        if not all(data.values()):
            errors.append("Fill all the fields.")
        if "@" not in data["email"]:
            errors.append("Email not valid.")
        if len(data["password"]) < 6:
            errors.append("Password: min 6 chars.")

        if errors:
            self.view.set_status(" ".join(errors))
            self.view.show_popup("Error", "\n".join(errors))
            return

        # If ok --> update Model
        user = User(**data)
        self.model.register_user(user)

        self.view.set_status(f"Registration ok: {user.username}!")
        self.view.show_popup("OK", f"User {user.username} registered.")
        self.view.clear()

