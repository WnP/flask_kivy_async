from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import socket
import json
import threading


TCP_IP = 'cheellex.com'
TCP_PORT = 5010
BUFFER_SIZE = 1024
MESSAGE = json.dumps((123, 0, 0))



class SclMain(BoxLayout):
    r = ObjectProperty(None)
    g = ObjectProperty(None)
    b = ObjectProperty(None)

    def send_rgb(self):
        t = threading.Thread(
            target=self.send_rgb_to_tcp,
            args=())
        t.daemon = True
        t.start()

    def send_rgb_to_tcp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))

        try:
            s.send(
                json.dumps((
                    int(self.r.value),
                    int(self.g.value),
                    int(self.b.value),
                )))
        except ValueError, error:
            pass
        finally:
            s.close()


class SclApp(App):
    def build(self):
        return SclMain()


if __name__ == '__main__':
    SclApp().run()
