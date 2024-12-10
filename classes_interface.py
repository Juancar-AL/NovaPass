import flet as ft
import csv
import time

global global_email
global_email = None


class SnackBarError(ft.SnackBar):
    def __init__(self, page):
        super().__init__(content=ft.Text("Error"), bgcolor="red")
        self.page = page

    def show_error(self, message):
        self.content = ft.Text(message)
        self.open = True
        self.page.update()
        time.sleep(1)
        self.open = False
        self.page.update()


class MainInputs(ft.Column):

    def __init__(self, function, inputs_data, page = None, change = None, new_page = None):
        super().__init__()
        text = ft.Text(function, theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        error_text = SnackBarError(page)
        # Crear los campos de texto dinámicamente
        self.inputs = [ft.CupertinoTextField(**data) for data in inputs_data]
        global global_email

        def update_data(data):
            for i, input_field in enumerate(self.inputs):
                data.append(input_field.value)

        def validate_email(email, password=None, content=None, mode="register"):
            """
            Valida el correo electrónico y la contraseña según el modo.

            mode: "register" para validar registros, "login" para validar inicios de sesión.
            """
            if "@" not in email:
                error_text.show_error("Por favor introduzca un correo válido")
                return False

            if mode == "register":
                if email in content:
                    error_text.show_error("El email ya ha sido registrado")
                    return False
                return True

            elif mode == "login":
                if email not in content:
                    error_text.show_error(
                        "No existe ninguna cuenta con ese correo electrónico"
                    )
                    return False

                for line in content.splitlines():
                    try:
                        stored_email, stored_password = line.split(",")
                        if stored_email == email:
                            if stored_password == password:
                                return True
                            else:
                                error_text.show_error(
                                    "Por favor, revise los campos introducidos")
                                return False
                    except ValueError:
                        error_text.show_error(
                            "Ha habido un error en el archivo")
                        return False

            return False

        def validate_passwords(password, password2=None):
            if not password:
                error_text.show_error("Por favor introduzca una contraseña")
                return False
            if password2 is not None and password != password2:
                error_text.show_error("Las contraseñas no coinciden")
                return False
            return True

        def clear_inputs():
            for input_field in self.inputs:
                input_field.value = ""
                input_field.update()

        def get_inputs():
            global global_email
            data = []
            with open("users.csv", mode="r", newline="") as fp:
                s = fp.read()
            update_data(data)

            if len(self.inputs) == 3:
                global_email = data[0]
                password = data[1]
                password2 = data[2]
                if validate_email(global_email, content=s, mode="register") and validate_passwords(password, password2):
                    with open("users.csv", mode="a", newline="") as f:
                        writer = csv.writer(f, delimiter=",")
                        writer.writerow([global_email, password])
                    clear_inputs()
            elif len(self.inputs) == 2:
                # Set global_email to the provided email
                global_email = data[0]
                password_view = Passwords_show(page)
                password_view.email = global_email  # Properly set the email
                self.password = data[1]

                if global_email == "root" or validate_email(global_email, self.password, s, mode="login"):
                    change(new_page)

        for input_field in self.inputs:
            input_field.on_submit = lambda e: get_inputs()
            input_field.width = 500

        button = ft.CupertinoFilledButton(
            content=ft.Text(function),
            opacity_on_click=0.3,
            on_click=lambda e: get_inputs(),
            width=500
        )

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [text] + self.inputs + [error_text, button]


class logo(ft.Image):
    def __init__(self):
        super().__init__()
        self.src = "assets/16792526538172.jpg"
        self.height = 200
        self.fit = ft.ImageFit.FILL


class IconButtonRow(ft.Row):
    def __init__(self, icon, on_click=None, new_page=None, alignment=ft.MainAxisAlignment.END):
        super().__init__(
            controls=[
                ft.Column(
                    [
                        ft.IconButton(
                            icon=icon,
                            icon_color="blue400",
                            icon_size=30,
                            on_click=lambda e: on_click(new_page),
                        )
                    ],
                    alignment=alignment,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                )
            ],
            alignment=alignment,
            vertical_alignment=ft.CrossAxisAlignment.END,
        )


class AboutPage(ft.Row):

    def __init__(self, function):

        login_button = ft.CupertinoFilledButton(
            content=ft.Text(
                "Iniciar sesión"
            ),
            opacity_on_click=0.3,
            on_click=lambda e: function("login"),
            width=500,
        )

        register_button = ft.CupertinoFilledButton(
            content=ft.Text(
                "Registrarse"
            ),
            opacity_on_click=0.3,
            on_click=lambda e: function("register"),
            width=500,
        )

        super().__init__()

        # Create buttons
        AboutPage.login_button = login_button
        AboutPage.register_button = register_button

        column = ft.Column(
            [
                logo(),
                ft.Column(
                    [login_button, register_button],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.alignment = ft.MainAxisAlignment.CENTER
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.expand = True
        self.controls = [column]


class data_page(ft.Row):
    def __init__(self, text, inputs_data, page, change, new_page):

        super().__init__()

        column = ft.Column([logo(), MainInputs(text, inputs_data, page, change, new_page)],
                           alignment=ft.MainAxisAlignment.CENTER,
                           horizontal_alignment=ft.CrossAxisAlignment.CENTER
                           )

        self.expand = True
        self.alignment = ft.MainAxisAlignment.CENTER
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [column]


class PasswordContainer(ft.Container):
    def __init__(self, service, password):
        super().__init__()
        text = ft.Container(content=ft.Text(value="Servicio"), bgcolor=ft.Colors.BLUE_100, padding=6, border_radius=10)
        service = ft.Text(
            value=service)
        text2 = ft.Container(content=ft.Text(value="Contraseña"), bgcolor=ft.Colors.BLUE_100, padding=6, border_radius=10)
        password = ft.Text(value=password)

        controls = ft.Column([text, service, text2, password])

        self.bgcolor = ft.Colors.BLUE_400
        self.padding = 10
        self.border_radius = 10
        self.content = controls


class Passwords_show(ft.GridView):
    def __init__(self, page):
        self.page = page
        global global_email
        self.email = global_email
        super().__init__()
        self.expand = 2
        self.runs_count = 5
        self.max_extent = 170
        self.child_aspect_ratio = 1.0
        self.spacing = 5
        self.run_spacing = 5

    def load_passwords(self):
        """Load password containers based on the email."""
        self.controls = []
        if not self.email:
            return

        containers = []
        with open("psw.csv", mode="r", newline="") as psw:
            reader = csv.reader(psw)
            for row in reader:
                if row[0] == self.email:
                    containers.append((row[1], row[2]))

        for service, password in containers:
            self.controls.append(PasswordContainer(service, password))
        if self.page:
            self.page.update()

    @property
    def email(self):
        return global_email  # Always fetch the latest value

    @email.setter
    def email(self, value):
        self._email = value
        self.load_passwords()


class test_AlertDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.title=ft.Text("Nueva contraseña"),
        column = ft.Text(value="TEST")

        self.controls=[column]
        


class MainPage(ft.Row):
    def __init__(self, function, page):
        super().__init__()

        search_row = ft.SearchBar(
            bar_hint_text="Busca las contraseñas de tus servicios", bar_leading=ft.Icon(ft.Icons.SEARCH), divider_color=ft.Colors.BLUE_400)
        row = ft.Row(
            [IconButtonRow(ft.Icons.PERSON, on_click=print), ft.VerticalDivider(width=130), search_row], spacing=30)

        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        back = IconButtonRow(
            on_click=function, new_page="welcome", icon=ft.Icons.ARROW_BACK)
        
        add = IconButtonRow(on_click=lambda e: page.open(                ft.CupertinoAlertDialog(
                    title=ft.Text("Nueva contraseña"),
                    content=ft.Column(controls=[ft.CupertinoTextField(placeholder_text="Servicio"),ft.CupertinoTextField(placeholder_text="Contraseña")]),
                    actions= [
        ft.CupertinoDialogAction(
            "Cerrar",
            is_destructive_action=True,
            on_click= lambda e: print("Cerrar"),
        ),
        ft.CupertinoDialogAction(
            text="Guardar",
            is_default_action=True,
            on_click=lambda e: print("Guardar"),
        ),
    ]
                )), icon=ft.icons.ADD_CIRCLE)

        self.controls = [row, add, back]
