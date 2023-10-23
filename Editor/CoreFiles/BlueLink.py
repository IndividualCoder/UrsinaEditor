from ursina import *
from CoreFiles.NewCursor import Cursor
import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)

class BlueLink(Button):
    def __init__(self, text='...', radius=0.1, ToSubtract=0, Key=None, partKey="", on_key_press=None, on_hover=None, on_unhover=None, hover_highlight=False, hover_highlight_color=color.white, hover_highlight_size=0.2, hover_highlight_button=False, **kwargs):
        super().__init__(text, radius, ToSubtract, Key, partKey, on_key_press, on_hover, on_unhover, hover_highlight, hover_highlight_color, hover_highlight_size, hover_highlight_button, **kwargs)

        self.MouseCursor = Cursor(model = "cube",texture = "../Images/BlueLinkMouse", scale=.03,enabled = False,collider = None)
        self.text_entity.scale = 2
        self.text_entity.color = color.rgb(51,102,204)
        self.color = color.clear
        self.highlight_color  = color.clear
        self.pressed_color = color.clear

        self.on_hover = self.OnHover
        self.on_unhover = self.OnUnhover
        # self.fit_to_text(0,(0,0))
        self.scale = self.scale

        for key,value in kwargs.items():
            setattr(self,key,value)

    def OnHover(self):
        mouse.visible = False
        self.MouseCursor.enable()

    def OnUnhover(self):
        mouse.visible = True
        self.MouseCursor.disable()

if __name__ == "__main__":
    app = Ursina()
    a = BlueLink("...",scale = .1)
    app.run()