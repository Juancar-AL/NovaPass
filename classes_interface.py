import flet as ft
import csv
from IPython.display import clear_output
import time

class MainInputs(ft.Column):

    def __init__(self, function, inputs_data, page):
        super().__init__()
        text = ft.Text(function, theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        text_e = ft.Text(
            "Revisa los datos introducidos e inténtelo de nuevo.", visible=False, color="red")
<<<<<<< HEAD
        text_r = ft.Text("El email ya ha sido registrado",
                         visible=False, color="red")
        # Crear los campos de texto dinámicamente
        self.inputs = [ft.CupertinoTextField(**data) for data in inputs_data]

        def print_inputs(self):
            data = []
            with open("users.csv", mode="r", newline="") as fp:
                s = fp.read()
            if len(self.inputs) == 3:
                for i, input_field in enumerate(self.inputs):
                    data.append(input_field.value)
                with open("users.csv", mode="a", newline="") as f:
                    writer = csv.writer(f, delimiter=",")
=======
        text_e = ft.Text("El email ya ha sido registrado", visible=False, color = "red")
        # Crear los campos de texto dinámicamente
        self.inputs = [ft.CupertinoTextField(**data) for data in inputs_data]

        def error(n_text):
            text_e.value = n_text
            text_e.visible = True
            page.update()
            time.sleep(3)
            text_e.visible = False
            page.update()


        def get_inputs():
                data = []
                with open("users.csv", mode="r", newline="") as fp:
                    s = fp.read()
                if len(self.inputs) == 3:
                    for i, input_field in enumerate(self.inputs):
                        data.append(input_field.value)
                    with open("users.csv", mode="a", newline="") as f:
                        writer = csv.writer(f, delimiter=",")
                        email = data[0]
                        password = data[1]
                        password2 = data[2]

                        clear_output()

                        if "@" in email:
                            if password == "" and password2 == "":
                                error("Por favor introduzca una contraseña")
                            elif email in s:
                                error("El email ya ha sido registrado")
                            elif password == password2:
                                writer.writerow(
                                    [email, password])
                                for i, input_field in enumerate(self.inputs):
                                    input_field.value = ""
                                    input_field.update()
                            else:
                                error("Por favor, revise los datos e inténtelo de nuevo")
                        else:
                            error("Por favor introduzca un correo válido")
                elif len(self.inputs) == 2:
                    for i, input_field in enumerate(self.inputs):
                        data.append(input_field.value)

>>>>>>> a0603ed4b93b6588c29d3c4eeddb7af589c88ffd
                    email = data[0]
                    password = data[1]

                    if email not in s:
                        error("No existe ninguna cuenta con ese correo electrónico")
                    elif email in s:
                        text_e.visible = False
                        page.update()
                        print("Email dentro")

<<<<<<< HEAD
                email = data[0]
                password = data[1]

                if email not in s:
                    text_r.value = "No existe ninguna cuenta con ese correo electrónico"
                    text_r.visible = True
                    page.update()
                elif email in s:
                    text_r.visible = False
                    page.update()
=======
>>>>>>> a0603ed4b93b6588c29d3c4eeddb7af589c88ffd

        button = ft.CupertinoFilledButton(
            content=ft.Text(function),
            opacity_on_click=0.3,
            on_click=lambda e: get_inputs(),
            width=500
        )

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [text] + self.inputs + [text_e, button]


class logo(ft.Image):
    def __init__(self):
        super().__init__()
        self.src = "assets/16792526538172.jpg"
        self.height = 200
        self.fit = ft.ImageFit.FILL


class quit(ft.Row):
    def __init__(self):
        super().__init__()

        column = ft.Column(
            [
                ft.IconButton(icon=ft.Icons.EXIT_TO_APP_ROUNDED,
                              icon_color="blue400",
                              icon_size=30,
                              on_click=lambda e: e.page.window_close())
            ],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        )
        self.alignment = ft.MainAxisAlignment.END
        self.vertical_alignment = ft.CrossAxisAlignment.END

        self.controls = [column]


class back(ft.Row):
    def __init__(self, function, new_page):
        super().__init__()

        column = ft.Column(
            [
                ft.IconButton(icon=ft.Icons.ARROW_BACK,
                              icon_color="blue400",
                              icon_size=30,
                              on_click=lambda e: function(new_page))
            ],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        )
        self.alignment = ft.MainAxisAlignment.END
        self.vertical_alignment = ft.CrossAxisAlignment.END

        self.controls = [column]


class AboutPage(ft.Row):

    def __init__(self, page, function, ):

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
    def __init__(self, text, inputs_data, page):

        super().__init__()

        column = ft.Column([logo(), MainInputs(text, inputs_data, page)],
                           alignment=ft.MainAxisAlignment.CENTER,
                           horizontal_alignment=ft.CrossAxisAlignment.CENTER
                           )

        self.expand = True
        self.alignment = ft.MainAxisAlignment.CENTER
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [column]
