import flet as ft
import classes as cl

language = "Spanish"


def main(page: ft.Page):
    page.title = "NovaPass | Password Manager"
    page.theme_mode = ft.ThemeMode.LIGHT

    def page_change(new_page):
        page.controls.clear()
        page.controls.extend(pages.get(new_page, []))
        page.update()

    # Datos para inputs
    email_text = "Correo electrónico" if language == "Spanish" else "Email"
    password_text = "Contraseña" if language == "Spanish" else "Password"

    reg_inputs_data = [
        {"placeholder_text": "Nombre" if language ==
            "Spanish" else "Name", "width": 500},
        {"placeholder_text": email_text, "width": 500},
        {"placeholder_text": password_text, "password": True,
            "can_reveal_password": True, "width": 500},
    ]

    log_inputs_data = [
        {"placeholder_text": email_text, "width": 500},
        {"placeholder_text": password_text, "password": True,
            "can_reveal_password": True, "width": 500},
    ]

    # Instancias de las páginas
    quit = cl.quit()
    about_page = cl.AboutPage(page, language, page_change)
    log_page = cl.data_page("Iniciar sesión", log_inputs_data)
    reg_page = cl.data_page("Registrarse", reg_inputs_data)

    # Diccionario de páginas
    pages = {
        "welcome": [quit, about_page],
        "login": [cl.back(page_change, "welcome"), log_page],
        "register": [cl.back(page_change, "welcome"), reg_page],
    }

    # Inicializar la página de bienvenida
    page.controls.extend(pages["welcome"])
    page.update()


ft.app(target=main)
