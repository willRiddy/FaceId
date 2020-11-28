from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

class AppUI(Widget):
    pass

class AppApp(App):

    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        return AppUI()

    def _on_file_drop(self, window, file_path):
        print(file_path)

if __name__ == '__main__':
    AppApp().run()