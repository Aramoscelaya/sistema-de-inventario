import flet as ft

class Notificador(ft.UserControl):
    def build(self):
        self.page.pubsub.subscribe(self.mostrar_notificacion)
        return ft.Text("")  # No es visible, solo escucha mensajes

    def mostrar_notificacion(self, mensaje):
        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje))
        self.page.snack_bar.open = True
        self.page.update()

class EnviarNotificacion(ft.UserControl):
    def build(self):
        return ft.ElevatedButton("Enviar Notificación", on_click=self.enviar)

    def enviar(self, e):
        self.page.pubsub.send_all("🔔 ¡Nueva Notificación!")

def main(page: ft.Page):
    page.title = "Notificaciones Globales con PubSub"

    notificador = Notificador()  # Solo escucha mensajes
    boton_notificacion = EnviarNotificacion()  # Envía mensajes

    page.add(notificador, boton_notificacion)

ft.app(target=main)
