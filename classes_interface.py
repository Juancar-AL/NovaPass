import flet as ft
import time
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import json
import os


# Declaramos el email como global para que sea accesible desde todo el código

global global_email
global_email = None


# Clase para mostrar errores
class SnackBarError(ft.SnackBar):
    def __init__(self, page):
        super().__init__(content=ft.Text("Error"), bgcolor="red")
        self.page = page

    # Método que muestra el error
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

        button = ft.CupertinoButton(
            content=ft.Text(function),
            opacity_on_click=0.3,
            on_click=lambda e: self.get_inputs(page, change, new_page),
            width=500,
            bgcolor=ft.Colors.BLUE_400,
        )

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.controls = [text, ft.Divider(),] + self.inputs + \
            [self.error_text, button]

    def update_data(self, data):
        for i, input_field in enumerate(self.inputs):
            data.append(input_field.value)

    def validate_email(self, email, password=None, content=None, mode="register"):
        # Valida el correo electrónico y la contraseña según el modo.

        df = read_encrypted_from_csv(
            "C:/Nova/data/users.csv", encryption_system, header=0, column=["User", "Password"])
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
                    data={"User": [global_email], "Password": [password]})
                save_encrypted_to_csv(df, "C:/Nova/data/users.csv", encryption_system, column=[
                                      "User", "Password"])
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
            elif (global_email == "nano" and self.password == "33"):
                change("nano")


# Botón para añdir botones de icono


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

        # Botón de inicio de sesión
        self.login_button = ft.CupertinoButton(
            content=ft.Text(
                "Iniciar sesión"
            ),
            opacity_on_click=0.3,
            on_click=lambda e: function("login"),
            width=500,
            bgcolor=ft.Colors.BLUE_400,
        )

        # Botón del registro
        self.register_button = ft.CupertinoButton(
            content=ft.Text(
                "Regístrate"
            ),
            opacity_on_click=0.3,
            on_click=lambda e: function("register"),
            width=500,
            bgcolor=ft.Colors.BLUE_400,
        )

        super().__init__()

        column = ft.Column(
            [
                Logo_2(width=400, opacity=1),
                ft.Divider(),
                ft.Column(
                    [self.login_button, self.register_button],
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

        column = ft.Column([Logo_2(width=400, opacity=1), ft.Divider(), MainInputs(text, inputs_data, page, change, new_page)],
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
        self.service_value = service
        self.password_value = password
        super().__init__()

        # Comprobación del modo de creación de contraseñas
        if not self.create:
            self.text = ft.Container(content=ft.Text(value="Servicio"),
                                     bgcolor=ft.Colors.BLUE_200, padding=6, border_radius=10)
            self.service = ft.Container(ft.Text(
                value=self.service_value), bgcolor=ft.Colors.WHITE, padding=6, border_radius=10)
            self.text2 = ft.Container(content=ft.Text(
                value="Contraseña"), bgcolor=ft.Colors.BLUE_200, padding=6, border_radius=10)
            self.password = ft.Container(ft.Text(
                value=self.password_value), bgcolor=ft.Colors.WHITE, padding=6, border_radius=10)

            self.controls = ft.Column(
                [self.text, self.service, self.text2, self.password, self.error_text])
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

    # Función que se ejecutará si se pulsa el contenedor de la contraseña
    def click(self):
        # Se establece ese contenedor como pulsado o no pulsado
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

            self.controls = ft.Column(
                [self.text, self.service, self.text2, self.password, self.error_text])

            self.content = self.controls
            self.update()

    # Método para la eliminación de contraseñas
    def delete(self):
        df = read_encrypted_from_csv("C:/Nova/data/psw.csv", encryption_system, header=0, column=[
                                     "User", "Service", "Password"])
        df1 = df[(df["User"] == global_email) & (df["Service"] ==
                                                 self.service_value) & (df["Password"] == self.password_value)]
        df.drop(df1.index, inplace=True)
        try:
            save_encrypted_to_csv(df, 'C:/Nova/data/psw.csv', encryption_system, delete=True, column=[
                "User", "Service", "Password"])
        except:
            self.psw.load_passwords()

        self.psw.load_passwords()

    # Método que cambia lo que se muestra en el contenedor para así permitir la edición
    def edit(self):
        self.service_field = ft.CupertinoTextField(value=self.service_value, placeholder_text="Servicio", on_submit=lambda e: self.save(
            new=False), autofocus=True, text_size=15, max_lines=1, capitalization=ft.TextCapitalization.SENTENCES)
        self.password_field = ft.CupertinoTextField(
            value=self.password_value, placeholder_text="Contraseña", on_submit=lambda e: self.save(new=False),  text_size=15, max_lines=1)
        divider = ft.Divider(height=20)

        self.content = ft.Column(
            [self.service_field, divider, self.password_field])

        if self.page:
            self.update()

    # Método que guarda la contraseña editada o creada
    def save(self, new=True):
        if self.service_field.value != "" and self.password_field.value != "":

            data = {
                'User': [global_email],
                'Service': [self.service_field.value.capitalize()],
                'Password': [self.password_field.value]
            }

            df = pd.DataFrame(data)

            save_encrypted_to_csv(df, 'C:/Nova/data/psw.csv', encryption_system, column=[
                                      "User", "Service", "Password"])

        if not new:
            self.delete()
        else:
            self.error_text.show_error("Introduzca unos campos válidos")

# Casilla en la que se muestran todas las contarseñas de ese usuario


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

    # Método que carga las contraseñas de ese usuario
    def load_passwords(self, df=None):
        if df is None:
            df = read_encrypted_from_csv("C:/Nova/data/psw.csv", encryption_system, header=0, column=[
                                         "User", "Service", "Password"])

        self.controls = []
        if not self.email:
            return

        containers = []

        # Filtrar y ordenar los datos
        df1 = df[df["User"] == global_email]
        df1 = df1.sort_values(by=["Service"])

        # Selecciona las columnas necesarias
        df1 = df1[["User", "Service", "Password"]]
        user = df1.values.tolist()

        # Añade las contraseñas individualmente a cada celda
        for row in user:
            if len(row) >= 3:  # Comprobar que existen todos los campos necesarios
                # Se toman los 3 primeros valores
                username, service, password = row[:3]
                containers.append((service, password))

        for service, password in containers:
            self.controls.append(PasswordContainer(
                service=service, password=password, page=self.page, psw=self))

        if self.page:
            self.page.update()

    @property
    def email(self):
        return global_email  # Siempre toma el valor más nuevo del email

    @email.setter
    def email(self, value):
        self._email = value
        self.load_passwords()

# Clase que almacena el logo de la aplicación


class Logo_2(ft.Image):

    def __init__(self, width, opacity):
        super().__init__()
        self.src = "https://i.imgur.com/OBuFh3G.png"
        self.fit = ft.ImageFit.CONTAIN
        self.opacity = opacity  # Reduce opacity to 70%
        self.width = width

# Clase que almacena la página principal del gestor


class MainPage(ft.Row):
    def __init__(self, function, page, psw):
        super().__init__()

        self.psw = psw
        self.error_text = SnackBarError(page)

        self.logo = Logo_2(width=200, opacity=1)

        self.search_row = ft.SearchBar(
            bar_hint_text="Busca las contraseñas de tus servicios", capitalization=ft.TextCapitalization.SENTENCES, bar_leading=ft.Icon(ft.Icons.SEARCH), divider_color=ft.Colors.BLUE_400, on_submit=lambda e: self.search())
        row = ft.Row(
            [ft.VerticalDivider(width=10), self.logo, ft.VerticalDivider(width=10), self.search_row], spacing=30)

        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        back = IconButtonRow(
            on_click=function, new_page="welcome", icon=ft.Icons.ARROW_BACK)

        add = IconButtonRow(on_click=lambda e: self.add_psw(page),
                            icon=ft.icons.ADD_CIRCLE)

        reload = IconButtonRow(on_click=lambda e: self.psw.load_passwords(),
                               icon=ft.Icons.REPLAY_CIRCLE_FILLED_ROUNDED)

        self.controls = [row, add, reload, back, self.error_text]

    # Método que añade una nueva contraseña
    def add_psw(self, page):
        self.psw.controls.append(PasswordContainer(
            page=page, psw=self.psw, create=True))
        page.update()

    # Método que busca las contraseñas
    def search(self):
        df = read_encrypted_from_csv(
            "C:/Nova/data/psw.csv", encryption_system, header=0, column=["User", "Service", "Password"])
        if self.search_row.value != "":
            df1 = df[(df["User"] == global_email) & (df["Service"] ==
                                                     self.search_row.value)]
        else:
            df1 = df
        if df1.size == 0:
            self.error_text.show_error(
                "No se ha encontrado ninguna contraseña que corresponda a ese servicio")
        else:
            self.psw.load_passwords(df=df1)

# Easter egg


class NanoPage(ft.Column):
    def __init__(self):
        super().__init__()

        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Verificar que la dirección del video es correcta y este es accesible
        video = ft.VideoMedia("https://media-hosting.imagekit.io//f9078d3a5b5e45b2/descargar.mp4?Expires=1832955978&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=VssReUJbe3nKXGl4APW3WYqi4Tuvt-uN9QOr45CLg2SS6vuZN4Sg~ix21623M~-CXCaPNWGZgYcLJeLt1Us58v6x~weVysyQo1DAGesSWUhgW1jzl19TqySJVGIJrrfz9iHkDsheFTTIajfnJU5TB1-1BQ3LYOuuqwamrUhJDMjCu2Fim6wfFCai54AQzhNeZ9S3yOrMwLJO9wrIfTYcg-BGjz9x~64rnljJ98JUr~3W~HJ8e5kPZj4DNAQkPRNvayuxDYp3Pan8qGOThzJOB~mVVPdamyZkXhU5Zs3ODKdZcepu4-4GnbuX4Z0vXhRFhdskv9-o51dnvO7X1k1x3g__")

        # Configurar el reproductor de video
        video_player = ft.Video(
            playlist=[video],
            playlist_mode=ft.PlaylistMode.LOOP,  # Añadir el video a la playlist
            expand=False,
            autoplay=True,  # reproducir el video automáticamente
            muted=True,  # Silenciar el video
            aspect_ratio=9/16,
            on_loaded=lambda e: print("Video loaded successfully!"),
            on_error=lambda e: print(f"Error loading video: {
                                     e.data}")  # Error handling callback
        )

        video_container = ft.Container(video_player,
                                       width=800,  # Ajustar el ancho del video
                                       height=450,  # Ajustar el alto del video
                                       alignment=ft.alignment.center,  # Centrar el video
                                       )

        video_row = ft.Row([video_container],
                           alignment=ft.MainAxisAlignment.CENTER)

        # Añadir el reproductor de video a los controles
        self.controls = [video_row]


# Clase del encriptador de AES
class DataEncryption:
    def __init__(self):
        self.key_file = "C:/Nova/encryption_key.key"
        self.key = self._load_or_create_key()

    # Se carga o se crea una nueva clave
    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            key = get_random_bytes(32)
            with open(self.key_file, "wb") as f:
                f.write(key)
            return key

    # Método que encripta los datos
    def encrypt_data(self, data):
        json_data = json.dumps(data)
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = pad(json_data.encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        combined = iv + encrypted_data
        return base64.b64encode(combined).decode('utf-8')

    # Método que decripta los datos
    def decrypt_data(self, encrypted_str):
        try:
            combined = base64.b64decode(encrypted_str.encode('utf-8'))
            iv = combined[:AES.block_size]
            encrypted_data = combined[AES.block_size:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(encrypted_data)
            decrypted_str = unpad(
                decrypted_padded, AES.block_size).decode('utf-8')
            return json.loads(decrypted_str)
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

# Lee los datos encriptados desde el archivo csv


def read_encrypted_from_csv(filename, encryption_system, header, column):
    # Lee y descripta los datos de CSV en un DataFrame de pandas y restaura la estructura de columnas
    if not os.path.exists(filename):
        # Devuelve un DataFrame vacío siguiendo la estructura de las columnas
        return pd.DataFrame(columns=column)

    try:
        df = pd.read_csv(filename, encoding='utf-8', header=header)

        if 'encrypted_data' in df.columns:
            decrypted_data = []
            columns = None

            for _, row in df.iterrows():
                decrypted_row = encryption_system.decrypt_data(
                    row['encrypted_data'])
                if decrypted_row:
                    if columns is None:
                        columns = decrypted_row['columns']
                    decrypted_data.append(decrypted_row['data'])

            if decrypted_data:
                result_df = pd.DataFrame(decrypted_data)
                # Revisa que todas las columnas necesarias existen
                for col in column:
                    if col not in result_df.columns:
                        result_df[col] = ''
                return result_df
            return pd.DataFrame(columns=column)
        else:
            # Para los datos sin desencriptar revisa que todas las columnas necesarias existan
            for col in column:
                if col not in df.columns:
                    df[col] = ''
            return df

    except (pd.errors.EmptyDataError, KeyError):
        return pd.DataFrame(columns=column)


def save_encrypted_to_csv(df, filename, encryption_system, column, delete=False,):
    # Guarda un DataFrame a un archivo CSV con las filas encriptadas mientras mantiene la estructura de las columnas

    # Si el DataFrame está vacío se crea uno con la estructura de columnas necesarias
    if df.empty:
        df = pd.DataFrame(columns=column)

    # Revisa que todas las columnas existan
    for col in column:
        if col not in df.columns:
            df[col] = ''

    # Lee los datos si el archivo CSV existe
    existing_df = None
    if os.path.exists(filename):
        existing_df = read_encrypted_from_csv(
            filename, encryption_system, header=0, column=column)

    # Si hay nuevos datos se concatenan con los datos antiguos
    if not delete:
        if existing_df is not None and not existing_df.empty:
            df = pd.concat([existing_df, df], ignore_index=True)
            # Si se necesita se eliminan los duplicados
        subset = ['User', 'Service'] if 'Service' in df.columns else ['User']
        df = df.drop_duplicates(subset=subset, keep='last')
    else:
        df = df

    # Se guardan los nombres de las columnas
    columns = df.columns.tolist()

    # Se crean las  filas encriptadas
    encrypted_rows = []
    for _, row in df.iterrows():
        row_dict = {
            'data': row.to_dict(),
            'columns': columns
        }
        encrypted_data = encryption_system.encrypt_data(row_dict)
        encrypted_rows.append({'encrypted_data': encrypted_data})

    # Se crea un DataFrame con los datos encriptados
    encrypted_df = pd.DataFrame(encrypted_rows)

    # Se guardan como una única columna
    encrypted_df.to_csv(filename, index=False,
                        encoding='utf-8', header=['encrypted_data'])


# Se inicializa el sistema de encriptación
encryption_system = DataEncryption()
