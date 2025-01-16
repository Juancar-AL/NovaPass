import flet as ft
import classes_interface as cl


def main(page: ft.Page):
    page.title = "NovaPass | Password Manager"
    page.theme_mode = ft.ThemeMode.LIGHT

    def page_change(new_page):
        if new_page != None:
            page.controls.clear()
            page.controls.extend(pages.get(new_page, []))
            page.update()
            if new_page == "main":
                psw_page.load_passwords()
            page.update()
        else:
            page.window.close()

    # Datos para inputs
    email_text = "Correo electrónico"
    password_text = "Contraseña"

    reg_inputs_data = [
        {"placeholder_text": email_text},
        {"placeholder_text": password_text, "password": True,
            "can_reveal_password": True},
        {"placeholder_text": f"Confirmar {password_text}", "password": True,
            "can_reveal_password": True},
    ]

    log_inputs_data = [
        {"placeholder_text": email_text},
        {"placeholder_text": password_text, "password": True,
            "can_reveal_password": True},
    ]

    # Instancias de las páginas
    quit = cl.IconButtonRow(on_click=page_change,
                            icon=ft.Icons.EXIT_TO_APP_ROUNDED)
    about_page = cl.AboutPage(page_change)

    psw_page = cl.Passwords_show(page)

    log_page = cl.data_page(
        "Iniciar sesión", log_inputs_data, page, change=page_change, new_page="main")
    reg_page = cl.data_page(
        "Registrarse", reg_inputs_data, page, change=page_change, new_page="main")

    main_page = cl.MainPage(page_change, page, psw_page)

    back_button = cl.IconButtonRow(
        on_click=page_change, new_page="welcome", icon=ft.Icons.ARROW_BACK)

    # Diccionario de páginas
    pages = {
        "welcome": [quit, about_page],
        "login": [back_button, log_page],
        "register": [back_button, reg_page],
        "main": [main_page, psw_page]
    }

    # Inicializar la página de bienvenida
    page.controls.extend(pages["welcome"])
    page.update()


ft.app(target=main)