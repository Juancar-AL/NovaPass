import flet as ft
import csv
from IPython.display import clear_output


class MainInputs(ft.Column):
    def __init__(self, function, inputs_data, page):
        super().__init__()
        text = ft.Text(function, theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        text_e = ft.Text(
            "Revisa los datos introducidos e inténtelo de nuevo.", visible=False, color="red")
        text_r = ft.Text("El email ya ha sido registrado", visible=False, color = "red")
        # Crear los campos de texto dinámicamente
        self.inputs = [ft.CupertinoTextField(**data) for data in inputs_data]

        def print_inputs(e):
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

                    if email in s:
                        text_r.value = "El email ya ha sido registrado"
                        text_r.visible = True
                        page.update()
                    elif password == password2:
                        writer.writerow(
                            [email, password])
                        for i, input_field in enumerate(self.inputs):
                            input_field.value = ""
                            input_field.update()
                    else:
                        text_e.visible = True
                        page.update()
            elif len(self.inputs) == 2:
                for i, input_field in enumerate(self.inputs):
                    data.append(input_field.value)

                email = data[0]
                password = data[1]

                if email not in s:
                    text_r.value = "No existe ninguna cuenta con ese correo electrónico"
                    text_r.visible = True
                    page.update()
                elif email in s:
                    text_r.visible = False
                    page.update()

                    

        button = ft.CupertinoFilledButton(
            content=ft.Text(function),
            opacity_on_click=0.3,
            on_click=print_inputs,
            width=500
        )

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [text] + self.inputs + [text_e, text_r, button]


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

    def __init__(self, page, language, function, ):

        login_button = ft.CupertinoFilledButton(
            content=ft.Text(
                "Iniciar sesión" if language == "Spanish" else "Log in"
            ),
            opacity_on_click=0.3,
            on_click=lambda e: function("login"),
            width=500,
        )

        register_button = ft.CupertinoFilledButton(
            content=ft.Text(
                "Registrarse" if language == "Spanish" else "Register"
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
