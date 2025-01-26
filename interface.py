import flet as ft
import classes_interface as cl


# Función princial de flet que carga la página principal
def main(page: ft.Page):
    page.title = "NovaPass | Password Manager"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Función para cambiar entre las diferentes páginas
    def page_change(new_page):
        if new_page != None:
            page.controls.clear()  # Se limpian los elementos de la página actual
            # Se añaden los elementos de la página nueva
            page.controls.extend(pages.get(new_page, []))
            page.update()  # Se actualiza la páagina
            if new_page == "main":
                # En caso de que la página sea la principal, se cargan las contraseñas
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

    # Instancias para las páginas
    quit = cl.IconButtonRow(on_click=page_change,
                            icon=ft.Icons.EXIT_TO_APP_ROUNDED)
    about_page = cl.AboutPage(page_change)

    psw_page = cl.Passwords_show(page)

    logo = cl.Logo_2(width=800, opacity=0.2)

    log_page = cl.data_page(
        "Inicio de sesión", log_inputs_data, page, change=page_change, new_page="main")
    reg_page = cl.data_page(
        "Registro", reg_inputs_data, page, change=page_change, new_page="main")

    main_page = cl.MainPage(page_change, page, psw_page)

    back_button = cl.IconButtonRow(
        on_click=page_change, new_page="welcome", icon=ft.Icons.ARROW_BACK)

    nano_page = cl.NanoPage()

    # Diccionario de páginas
    pages = {
        "welcome": [quit, about_page],
        "login": [back_button, log_page],
        "register": [back_button, reg_page],
        "main": [main_page, ft.Stack([ft.Container(
            ft.Column([logo, ft.Divider(height=200, opacity=0.0)], alignment=ft.MainAxisAlignment.CENTER,
                      horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.top_center,
            expand=True,
            width=page.width,
            height=page.height
        ), psw_page])],
        "nano": [back_button, nano_page]
    }

    # Inicializar la página de bienvenida
    page.controls.extend(pages["welcome"])
    page.update()


ft.app(target=main)
