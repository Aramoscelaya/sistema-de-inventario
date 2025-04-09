import flet as ft

def alert_dialog(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = True

    def handle_action_click(e):
        page.add(ft.Text(f"Action clicked: {e.control.text}"))
        page.close(e.control.parent)

    cupertino_actions = [
        ft.CupertinoDialogAction(
            "Yes",
            is_destructive_action=True,
            on_click=handle_action_click,
        ),
        ft.CupertinoDialogAction(
            text="No",
            is_default_action=False,
            on_click=handle_action_click,
        ),
    ]

    return ft.FilledButton(
        text="Open Cupertino Dialog",
        on_click=lambda e: page.open(
            ft.CupertinoAlertDialog(
                title=ft.Text("Cupertino Alert Dialog"),
                content=ft.Text("Do you want to delete this file?"),
                actions=cupertino_actions,
            )
        ),
    )