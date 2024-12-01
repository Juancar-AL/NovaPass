import flet as ft


class MainInputs(ft.Column):
    def __init__(self, function, inputs_data):
        super().__init__()
        text = ft.Text(function, theme_style=ft.TextThemeStyle.HEADLINE_LARGE)

        # Crear los campos de texto dinámicamente
        self.inputs = [ft.CupertinoTextField(**data) for data in inputs_data]

        def print_inputs(e):
            for i, input_field in enumerate(self.inputs):
                print(f"Input {i + 1}: {input_field.value}")
                input_field.value = ""
                input_field.update()

        button = ft.CupertinoFilledButton(
            content=ft.Text(function),
            opacity_on_click=0.3,
            on_click=print_inputs,
            width=500
        )

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [text] + self.inputs + [button]


class logo(ft.Image):
    def __init__(self):
        super().__init__()
        self.src = "assets/logo.png"
        self.width = 200
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
    def __init__(self, text, inputs_data):

        super().__init__()

        column = ft.Column([logo(), MainInputs(text, inputs_data)],
                           alignment=ft.MainAxisAlignment.CENTER,
                           horizontal_alignment=ft.CrossAxisAlignment.CENTER
                           )

        self.expand = True
        self.alignment = ft.MainAxisAlignment.CENTER
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [column]
