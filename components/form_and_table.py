import flet as ft

def base(title, contenA, contenB, page):
    content_principal=[
        ft.Column(
            [
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text(title, size=30, weight=ft.FontWeight.BOLD, font_family="bodoni"),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton("Volver al inicio", on_click=lambda e: page.go("/")),
                            alignment=ft.alignment.center,
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ),
            ],
        ),
        ft.ResponsiveRow(
            expand=True,
            controls = [
                ft.Container(
                    bgcolor = "#222222",
                    border_radius = 10,
                    col = 4,
                    expand=True,
                    content= ft.Column(
                        controls= contenA
                    )
                ),
                ft.Container(
                    bgcolor = "#222222",
                    border_radius = 10,
                    col = 8,
                    expand=True,
                    content= ft.Column(
                        controls= contenB
                    )
                )
            ]
        )
    ]

    return content_principal