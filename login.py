import flet as ft

language = "Spanish"


def main(page: ft.Page):
    global language

    login_button_ref = ft.Ref[ft.CupertinoFilledButton]()
    register_button_ref = ft.Ref[ft.CupertinoFilledButton]()

    page.title = "NovaPass | Password Manager"
    page.theme_mode = ft.ThemeMode.LIGHT
    quit = ft.Row(
        [
            ft.Column(
                [
                    ft.IconButton(icon=ft.Icons.EXIT_TO_APP_ROUNDED,
                                  icon_color="blue400",
                                  icon_size=30,
                                  on_click=lambda e: e.page.window_close())
                ],
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.END,
            )
        ],
        alignment=ft.MainAxisAlignment.END,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    def set_language(lan):
        global language
        language = lan

        login_button_ref.current.content.value = "Iniciar sesión" if language == "Spanish" else "Log in"
        register_button_ref.current.content.value = "Registrarse" if language == "Spanish" else "Register"
        page.close(dialog_lan)
        page.update()
    dialog_lan = ft.AlertDialog(actions=[
        ft.CupertinoButton(content=ft.Image(
            src=f"assets/esp.png", width=100, height=100, fit=ft.ImageFit.CONTAIN), on_click=lambda e: set_language("Spanish")),
        ft.CupertinoButton(content=ft.Image(
            src=f"assets/uk.png", width=100, height=100, fit=ft.ImageFit.CONTAIN), on_click=lambda e: set_language("English"))
    ])

    about_page = ft.Row(
        [
            ft.Column(
                [
                    ft.Image(src=f"assets/logo.png", width=200,
                             height=200,
                             fit=ft.ImageFit.CONTAIN),
                    ft.Column(
                        [
                            ft.Text("Iniciar sesión" if language == "Spanish" else "Log in", theme_style=ft.TextThemeStyle.HEADLINE_LARGE),
                            ft.Divider(),
                            ft.CupertinoTextField(
                                ref=login_button_ref,
                                placeholder_text="Correo electrónico" if language == "Spanish" else "Email",
                                width=500
                            ),
                            ft.CupertinoTextField(
                                ref=register_button_ref,
                                placeholder_text="Contraseña" if language == "Spanish" else "Password",
                                width=500
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Divider()
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    lan = ft.Row(
        [
            ft.Column(
                [
                    ft.IconButton(icon=ft.Icons.TRANSLATE_ROUNDED,
                                  icon_color="blue400",
                                  icon_size=30,
                                  on_click=lambda e: page.open(dialog_lan))
                ],
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.END,
            )
        ],
        alignment=ft.MainAxisAlignment.END,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    page.add(quit, about_page, lan)


ft.app(target=main)
