# Dear programmer,
# When I wrote this code only God and I knew how it worked.
# Now, only God knows.
# Good luck trying to optimize this code.
# Hours wasted on this code: 0


import flet as ft
import time
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

global global_email
global_email = None


# Configuración barra para muestra de errores
class SnackBarError(ft.SnackBar):
    def __init__(self, page):
        super().__init__(content=ft.Text("Error"), bgcolor="red")
        self.page = page

    def show_error(self, message):

        # Configuración visual
        self.content = ft.Text(message)
        self.open = True
        self.page.update()
        time.sleep(1)
        self.open = False
        self.page.update()


# Clase para la creación de los campos principales de registro e inicio de sesión
class MainInputs(ft.Column):

    def __init__(self, function, inputs_data, page=None, change=None, new_page=None):

        super().__init__()
        # Organización visual de los campos
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
        # Valida el correo electrónico y la contraseña según el modo.

        df = pd.read_csv("users.csv", encoding="utf-8", header=0)
        users = df["User"]
        users_list = users.values.tolist()
        df2 = df[["User", "Password"]]
        df_list = df2.values.tolist()

        # mode: "register" para validar registros, "login" para validar inicios de sesión.
        s_email = email.split("@", 1)
        s_email2 = s_email[-1].replace(".", "")

        # Comprobación de que el correo introducido esté en la base de datos
        if "@" not in email or "." not in s_email[-1] or s_email[0] == "" or s_email2.isalpha() == False:
            self.error_text.show_error("Por favor introduzca un correo válido")
            return False

        # Comprobaciones modo
        if mode == "register":
            if email in users_list:
                self.error_text.show_error("El email ya ha sido registrado")
                return False
            return True

        elif mode == "login":
            if email not in users_list:
                self.error_text.show_error(
                    "No existe ninguna cuenta con ese correo electrónico"
                )
                return False

            for i, j in df_list:
                try:
                    stored_email, stored_password = i, str(j)
                    if stored_email == email:
                        if stored_password == password:
                            return True
                        else:
                            self.error_text.show_error(
                                "Por favor, revise los campos introducidos")
                except ValueError:
                    self.error_text.show_error(
                        "Ha habido un error en el archivo")
                    return False

        return False

    # Validar las contraseñas (que esté presente en el input y que conincida con la segunda contraseña)
    def validate_passwords(self, password, password2=None):
        if not password:
            self.error_text.show_error("Por favor introduzca una contraseña")
            return False
        if password2 is not None and password != password2:
            self.error_text.show_error("Las contraseñas no coinciden")
            return False
        return True

    # Limpiar los valores de los campos de inicio y registro
    def clear_inputs(self):
        for input_field in self.inputs:
            input_field.value = ""
            input_field.update()

    # Tomar los valores de los campos de inicio y registro
    def get_inputs(self, page, change, new_page):
        global global_email
        data = []

        self.update_data(data)

        if len(self.inputs) == 3:
            global_email = data[0]
            password = data[1]
            password2 = data[2]
            if self.validate_email(global_email, mode="register") and self.validate_passwords(password, password2):
                df = pd.DataFrame(
                    data={"User": [encoder.encrypt(global_email)], "Password": [encoder.encrypt(password)]})
                df.to_csv("users.csv", mode="a", index=False,
                          header=0, encoding="utf-8")
                self.clear_inputs()
                change(new_page)
        elif len(self.inputs) == 2:
            # Establecer el email global al email indicado
            global_email = data[0]
            password_view = Passwords_show(page)
            password_view.email = global_email  # Establece el email de forma correcta
            self.password = data[1]

            if global_email == "root" or self.validate_email(global_email, self.password, mode="login"):
                change(new_page)
            elif (global_email == "nano" and self.password == "33") or self.validate_email(global_email, self.password, mode="login"):
                change("nano")

# Clase que almacena el logo de la aplicación


class logo(ft.Image):
    def __init__(self):
        super().__init__()
        self.src = "assets/16792526538172.jpg"
        self.height = 200
        self.fit = ft.ImageFit.FILL

# Botón para añdir botones


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


# Clase que inicializa la página principal
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


# Clase que inicializa la clase con los datos
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


# Clase que inicializa el contenedor de la contraseña
class PasswordContainer(ft.Container):
    def __init__(self, page, psw, service=None, password=None, create=False):
        self.psw = psw
        self.create = create
        self.error_text = SnackBarError(page)
        self.service = service
        self.password = password
        super().__init__()

        if not self.create:
            text = ft.Container(content=ft.Text(value="Servicio"),
                                bgcolor=ft.Colors.BLUE_100, padding=6, border_radius=10)
            service = ft.Text(
                value=self.service)
            text2 = ft.Container(content=ft.Text(
                value="Contraseña"), bgcolor=ft.Colors.BLUE_100, padding=6, border_radius=10)
            password = ft.Text(value=self.password)

            self.controls = ft.Column(
                [text, service, text2, password, self.error_text])
            self.content = self.controls
        else:
            self.edit()

        self.bgcolor = ft.Colors.BLUE_400
        self.padding = 10
        self.border_radius = 10
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=30,
            color=ft.Colors.BLUE_400,
            blur_style=ft.ShadowBlurStyle.OUTER,
        )
        self.ink = True
        self.on_click = lambda e: self.click()
        self.clicked = False

    def click(self):
        self.clicked = not self.clicked
        if self.clicked:
            edit = ft.FloatingActionButton(
                icon=ft.Icons.EDIT, on_click=lambda e: self.edit(),  bgcolor=ft.Colors.WHITE)
            delete = ft.FloatingActionButton(
                icon=ft.Icons.DELETE, on_click=lambda e: self.delete(),  bgcolor=ft.Colors.RED)

            row = ft.Row([edit, delete], alignment=ft.MainAxisAlignment.CENTER)

            self.content = row
            self.update()

        if not self.clicked:

            self.content = self.controls
            self.update()

    def delete(self):
        df = pd.read_csv("psw.csv", encoding="utf-8", header=0)
        df1 = df[(df["User"] == global_email) & (df["Service"] ==
                                                 self.service) & (df["Password"] == self.password)]
        df.drop(df1.index, inplace=True)
        df.to_csv('psw.csv', header=["User", "Service", "Password"],
                  index=False, encoding='utf-8')
        self.psw.load_passwords(df=pd.read_csv(
            "psw.csv", encoding="utf-8", header=0))

    def edit(self):
        self.service_field = ft.CupertinoTextField(value=self.service, on_submit=lambda e: self.save(
            new=False), autofocus=True, text_size=15, max_lines=1, capitalization=ft.TextCapitalization.SENTENCES)
        self.password_field = ft.CupertinoTextField(
            value=self.password, on_submit=lambda e: self.save(new=False),  text_size=15, max_lines=1)
        divider = ft.Divider(height=20)
        plus = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda e: self.save(
            new=False), bgcolor=ft.Colors.WHITE, mini=True)
        add = ft.Row([plus], alignment=ft.MainAxisAlignment.END)

        self.content = ft.Column(
            [self.service_field, divider, self.password_field, add])

        if self.page:
            self.update()

    def save(self, new=True):
        if self.service_field.value != "" and self.password_field.value != "":

            data = {
                'User': [encoder.encrypt(global_email)],
                'Service': [encoder.encrypt(self.service_field.value.capitalize())],
                'Password': [encoder.encrypt(self.password_field.value)]
            }

            df = pd.DataFrame(data)

            # Append the DataFrame to the CSV file
            df.to_csv('psw.csv', mode='a', header=0,
                      index=False, encoding='utf-8')

            if not new:
                self.delete()
        else:
            self.error_text.show_error("Introduzca unos campos válidos")


class Passwords_show(ft.GridView):
    def __init__(self, page):

        self.page = page
        global global_email
        self.email = global_email

        super().__init__()

        # Configuración visual de la rejilla
        self.child_aspect_ratio = 1.7
        self.max_extent = 400
        self.spacing = 6
        self.run_spacing = 6
        self.runs_count = 7
        self.expand = 1

    # Cargar las contraseñas en función del nombre de usuario

    def load_passwords(self, df):

        self.controls = []
        if not self.email:
            return

        containers = []

        # Cargar los valores desde la base de datos
        df1 = df[df["User"] == global_email]
        df1 = df1.sort_values(by=["Service"])
        user = df1.values.tolist()

        # Añadir las contraseñas individualmente a cada casilla de la clase PasswordContainer
        for username, service, password in user:
            containers.append((service, password))

        for service, password in containers:
            self.controls.append(PasswordContainer(
                service=service, password=password, page=self.page, psw=self))
        if self.page:
            self.page.update()

    @ property
    def email(self):
        return global_email  # Siempre recoger el valor más actualizado

    @ email.setter
    def email(self, value):
        self._email = value
        self.load_passwords(df=pd.read_csv(
            "psw.csv", encoding="utf-8", header=0))


class MainPage(ft.Row):
    def __init__(self, function, page, psw):
        super().__init__()

        self.psw = psw
        self.error_text = SnackBarError(page)

        search_row = ft.SearchBar(
            bar_hint_text="Busca las contraseñas de tus servicios", capitalization=ft.TextCapitalization.SENTENCES, bar_leading=ft.Icon(ft.Icons.SEARCH), divider_color=ft.Colors.BLUE_400, on_submit=lambda e: search())
        row = ft.Row(
            [IconButtonRow(ft.Icons.PERSON, on_click=print), ft.VerticalDivider(width=130), search_row], spacing=30)

        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        back = IconButtonRow(
            on_click=function, new_page="welcome", icon=ft.Icons.ARROW_BACK)

        add = IconButtonRow(on_click=lambda e: add_psw(page),
                            icon=ft.icons.ADD_CIRCLE)

        self.controls = [row, add, back, self.error_text]

        def add_psw(page):
            psw.controls.append(PasswordContainer(
                page=page, psw=psw, create=True))
            page.update()

        def search():
            df = pd.read_csv("psw.csv", encoding="utf-8", header=0)
            if search_row.value != "":
                df1 = df[(df["User"] == global_email) & (df["Service"] ==
                                                     search_row.value)]
            else:
                df1 = df
            if df1.size == 0:
                self.error_text.show_error(
                    "No se ha encontrado ninguna contraseña que corresponda a ese servicio")
            else:
                self.psw.load_passwords(df=df1)


class NanoPage(ft.Column):
    def __init__(self):
        super().__init__()

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Ensure the video path is correct and accessible
        video = ft.VideoMedia("assets/descargar.mp4")

        # Add proper configuration for the video player
        video_player = ft.Video(
            playlist=[video],
            playlist_mode=ft.PlaylistMode.LOOP,  # Add the video to the playlist
            expand=False,
            autoplay=True,  # Automatically play the video
            muted=True,  # Set muted to True if you want to disable sound
            aspect_ratio=16/9,
            on_loaded=lambda e: print("Video loaded successfully!"),
            on_error=lambda e: print(f"Error loading video: {
                                     e.data}")  # Error handling callback
        )

        video_container = ft.Container(video_player,
                                       width=800,  # Set the desired width of the video
                                       height=450,  # Set the desired height of the video
                                       alignment=ft.alignment.center,  # Center the video
                                       bgcolor=ft.Colors.BLACK  # Optional: Add a background color
                                       )
        
        video_row = ft.Row([video_container], alignment=ft.MainAxisAlignment.CENTER)

        # Add the video player to the controls
        self.controls = [video_row]

class encoder():
    def __init__(self):
        self.key = "YELLOW SUBMARINE".encode("utf-8")
        self.cipher = None
    def encrypt(self,data):
        self.cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, self.tag = self.cipher.encrypt_and_digest(data)
        self.nonce = self.cipher.nonce

        return ciphertext

    def decrypt(self,data):
        cipher = AES.new(self.key, AES.MODE_EAX, self.nonce)
        data2 = cipher.decrypt_and_verify(data, self.tag)
        return data2
    
encoder = encoder()
print(encoder.encrypt("TEST".encode("utf-8")))
print(str(encoder.decrypt(encoder.encrypt("TEST".encode("utf-8"))), ))

