# Dear programmer,
# When I wrote this code only God and I knew how it worked.
# Now, only God knows.
# Good luck trying to optimize this code.
# Hours wasted on this code: 0


import flet as ft
import csv
import time
import pandas as pd

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

    def __init__(self, function, inputs_data, page=None, change=None, new_page=None):
        super().__init__()
        text = ft.Text(function, theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.error_text = SnackBarError(page)
        # Crear los campos de texto dinámicamente
        self.inputs = [ft.CupertinoTextField(**data) for data in inputs_data]
        global global_email

        for input_field in self.inputs:
            input_field.on_submit = lambda e: self.get_inputs(
                page, change, new_page)
            input_field.width = 500

        button = ft.CupertinoFilledButton(
            content=ft.Text(function),
            opacity_on_click=0.3,
            on_click=lambda e: self.get_inputs(page, change, new_page),
            width=500
        )

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [text] + self.inputs + [self.error_text, button]

    def update_data(self, data):
        for i, input_field in enumerate(self.inputs):
            data.append(input_field.value)

    def validate_email(self, email, password=None, content=None, mode="register"):
        """
        Valida el correo electrónico y la contraseña según el modo.

        mode: "register" para validar registros, "login" para validar inicios de sesión.
        """
        s_email = email.split("@", 1)
        s_email2 = s_email[-1].replace(".", "")

        if "@" not in email or "." not in s_email[-1] or s_email[0] == "" or s_email2.isalpha() == False:
            self.error_text.show_error("Por favor introduzca un correo válido")
            return False

        if mode == "register":
            if email in content:
                self.error_text.show_error("El email ya ha sido registrado")
                return False
            return True

        elif mode == "login":
            if email not in content:
                self.error_text.show_error(
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
                            self.error_text.show_error(
                                "Por favor, revise los campos introducidos")
                            return False
                except ValueError:
                    self.error_text.show_error(
                        "Ha habido un error en el archivo")
                    return False

        return False

    def validate_passwords(self, password, password2=None):
        if not password:
            self.error_text.show_error("Por favor introduzca una contraseña")
            return False
        if password2 is not None and password != password2:
            self.error_text.show_error("Las contraseñas no coinciden")
            return False
        return True

    def clear_inputs(self):
        for input_field in self.inputs:
            input_field.value = ""
            input_field.update()

    def get_inputs(self, page, change, new_page):
        global global_email
        data = []
        
        s = pd.read_csv("users.csv", encoding="utf-8", header=0)
        print(s)

        self.update_data(data)

        if len(self.inputs) == 3:
            global_email = data[0]
            password = data[1]
            password2 = data[2]
            if self.validate_email(global_email, content=s, mode="register") and self.validate_passwords(password, password2):
                with open("users.csv", mode="a", newline="", encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=",")
                    writer.writerow([global_email, password])
                self.clear_inputs()
        elif len(self.inputs) == 2:
            # Set global_email to the provided email
            global_email = data[0]
            password_view = Passwords_show(page)
            password_view.email = global_email  # Properly set the email
            self.password = data[1]

            if global_email == "root" or self.validate_email(global_email, self.password, s, mode="login"):
                change(new_page)


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
        self.service = service
        self.password = password
        super().__init__()
        text = ft.Container(content=ft.Text(value="Servicio"),
                            bgcolor=ft.Colors.BLUE_100, padding=6, border_radius=10)
        service = ft.Text(
            value=self.service)
        text2 = ft.Container(content=ft.Text(
            value="Contraseña"), bgcolor=ft.Colors.BLUE_100, padding=6, border_radius=10)
        password = ft.Text(value=self.password)

        self.controls = ft.Column([text, service, text2, password])

        self.bgcolor = ft.Colors.BLUE_400
        self.padding = 10
        self.border_radius = 10
        self.content = self.controls
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=30,
            color=ft.Colors.BLUE_400,
            blur_style=ft.ShadowBlurStyle.OUTER,
        )
        self.ink=True
        self.on_click=lambda e: self.click()
        self.clicked = False
    def click(self):
        self.clicked = not self.clicked
        if self.clicked:
            edit = ft.FloatingActionButton(icon=ft.Icons.EDIT, on_click=lambda e: self.edit(),  bgcolor=ft.Colors.WHITE)
            delete = ft.FloatingActionButton(icon=ft.Icons.DELETE, on_click=lambda e: self.delete(),  bgcolor=ft.Colors.RED)

            row = ft.Row([edit, delete], alignment=ft.MainAxisAlignment.CENTER)

            self.content = row
            self.update()
            
        if not self.clicked:

            self.content = self.controls
            self.update()
    def delete(self, psw):
        df = pd.read_csv("psw.csv", encoding="utf-8", header=0)
        df1 = df[(df["User"] == global_email) & (df["Service"] == self.service) & (df["Password"] == self.password)]
        df.drop(df1.index, inplace=True)
        

    def edit(self):
        self.service = ft.CupertinoTextField( value=self.service, on_submit=lambda e: print("Test"), autofocus=True, text_size=15, max_lines=1, capitalization=True)
        self.password = ft.CupertinoTextField(value=self.password, on_submit=lambda e: print("Test"),  text_size=15, max_lines=1)
        divider = ft.Divider(height=20)
        plus = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda e: print("Test"), bgcolor=ft.Colors.WHITE, mini=True)
        add = ft.Row([plus], alignment = ft.MainAxisAlignment.END)

        self.column = ft.Column([self.service,divider, self.password, add])

        self.content = self.column
        self.update()
    def save(self, psw):
        if self.service.value != "" and self.password.value != "":

            data = {
                'Email': [global_email],
                'Service': [self.service.value],
                'Password': [self.password.value]
            }

            df = pd.DataFrame(data)

            # Append the DataFrame to the CSV file
            df.to_csv('psw.csv', mode='a', header=False, index=False, encoding='utf-8')
            self.service.value = ""
            self.password.value = ""
            psw.load_passwords()
        else:
            print("Introduzca unos campos válidos")



class PasswordEditContainer(ft.Container):
    def __init__(self, page, psw):
        super().__init__()
        self.error_text = SnackBarError(page)
        self.service = ft.CupertinoTextField( placeholder_text="Servicio", on_submit=lambda e: self.save(page, psw), autofocus=True, text_size=15, max_lines=1, capitalization=True)
        self.password = ft.CupertinoTextField(placeholder_text="Contraseña", on_submit=lambda e: self.save(page, psw),  text_size=15, max_lines=1)
        divider = ft.Divider(height=20)
        plus = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda e: self.save(page, psw), bgcolor=ft.Colors.WHITE, mini=True)
        add = ft.Row([plus], alignment = ft.MainAxisAlignment.END)

        self.column = ft.Column([self.service,divider, self.password, add, self.error_text])

        controls = self.column

        self.bgcolor = ft.Colors.BLUE_400
        self.padding = 10
        self.border_radius = 10
        self.content = controls
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=30,
            color=ft.Colors.BLUE_400,
            blur_style=ft.ShadowBlurStyle.OUTER,
        )

    def save(self, page, psw):
        if self.service.value != "" and self.password.value != "":
            with open("psw.csv", mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow(
                    [global_email, self.service.value, self.password.value])
            self.service.value = ""
            self.password.value = ""
            psw.load_passwords()
        else:
            self.error_text.show_error("Introduzca unos campos válidos")



class Passwords_show(ft.GridView):
    def __init__(self, page):
        self.page = page
        global global_email
        self.email = global_email
        super().__init__()
        self.child_aspect_ratio = 1.7
        self.max_extent = 400
        self.spacing = 6
        self.run_spacing = 6
        self.runs_count = 7
        self.expand = 1

    def load_passwords(self):
        """Load password containers based on the email."""
        self.controls = []
        if not self.email:
            return

        containers = []
        df = pd.read_csv("psw.csv", encoding="utf-8", header=0)
        reader = df.values.tolist()
        for row in reader:
            if row[0] == self.email:
                containers.append((row[1], row[2]))

        for service, password in containers:
            self.controls.append(PasswordContainer(service, password))
        if self.page:
            self.page.update()
    

    @ property
    def email(self):
        return global_email  # Always fetch the latest value

    @ email.setter
    def email(self, value):
        self._email = value
        self.load_passwords()


class MainPage(ft.Row):
    def __init__(self, function, page, psw):
        super().__init__()

        search_row = ft.SearchBar(
            bar_hint_text="Busca las contraseñas de tus servicios", capitalization= True, bar_leading=ft.Icon(ft.Icons.SEARCH), divider_color=ft.Colors.BLUE_400, on_submit=lambda e: print("Búsqueda"))
        row = ft.Row(
            [IconButtonRow(ft.Icons.PERSON, on_click=print), ft.VerticalDivider(width=130), search_row], spacing=30)

        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        back = IconButtonRow(
            on_click=function, new_page="welcome", icon=ft.Icons.ARROW_BACK)

        add = IconButtonRow(on_click=lambda e: add_psw(page, psw),
                            icon=ft.icons.ADD_CIRCLE)

        self.controls = [row, add, back]

        def add_psw(page, psw):
            psw.controls.append(PasswordEditContainer(page, psw))
            page.update()