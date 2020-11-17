from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import *

class Pupil:
    def __init__(self):
        self.name = 'Will'

pupils = [Pupil()]

class LoginScreen(GridLayout):
    def __init__(self, pupilList, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.names = []
        for pupil in pupilList:
            self.names.append(pupil.name)
        for widget in self.add_widgets:
            self.add_widget(Label(text=widget))

class MainApp(App):
    def build(self):
        # Drag'n'Drop
        Window.bind(on_dropfile=self._on_file_drop)

        return LoginScreen(pupils)
    
    def _on_file_drop(self, window, file_path):
        print(file_path)
        return file_path

if __name__ == '__main__':
    app = MainApp()
    app.run()