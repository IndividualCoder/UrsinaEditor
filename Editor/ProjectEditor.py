from ursina import *
from ursina import invoke
from ursina.color import tint
from OtherStuff import CustomWindow
from SceneEditor import SceneEditor
from random import randint
from OpenFile import OpenSeletor
class ProjectEditor(Entity):
    def __init__(self,ExportToPyFunc,CurrentTabs,EditorCamera,cam = camera,enabled = True,**kwargs):
        super().__init__(kwargs)
        self.ExportToPyFunc = ExportToPyFunc
        self.CurrentTabs = CurrentTabs
        self.EditorCamera = EditorCamera
        self.IsEditing = True
        self.enabled = enabled


        self.UniversalParentEntity = Entity(parent = cam.ui,enabled = self.enabled)

        self.TopButtonsParentEntity = Entity(parent = self.UniversalParentEntity,enabled = self.enabled,model = "cube",color = tint(color.white,-.6),texture ="white_cube",position  = (window.top[0],window.top[1] - .03,0) ,scale =(window.screen_resolution[0] / 1052,window.screen_resolution[1]/18000,2),always_on_top = True)
        self.TabsMenuParentEntity = Button(parent  = self.UniversalParentEntity,enabled = self.enabled,color = tint(color.green,-.1),highlight_color = tint(color.green,-.1),pressed_color = tint(color.green,-.1),position  = Vec3(0, 0.5, -20) ,scale = Vec3(1.78, 0.1, 1),always_on_top = True,render_queue = -3,Key = "tab",on_key_press=self.ShowTabMenu,radius=0) # Vec3(0, 0.39, 1) animate

        self.TabsForegroundParentEntity = Button(parent = self.TabsMenuParentEntity,radius=0,color = color.green,position = Vec3(-0.136, 0, -22),rotation = Vec3(0, 0, 0),scale = Vec3(0.727004, 1, 1),always_on_top = True,render_queue = -1)

        self.ProjectTabsScrollEntity = Button(parent = self.TabsMenuParentEntity,radius=0,color = tint(color.green,-.1),highlight_color = tint(color.green,-.1),pressed_color = tint(color.green,-.1),origin = (-.5,0,0),position = Vec3(0.2277, 0, -21),rotation = Vec3(0, 0, 0),scale = Vec3(.271, 1, 1),always_on_top = True,render_queue = -2)

        self.AddEditorToPrjectButton = Button(parent = self.TabsForegroundParentEntity,text = "+",on_click = Func(print,"hi"),render_queue = self.TabsForegroundParentEntity.render_queue,always_on_top = True,radius=.1)

        self.SaveProjectButton = Button(parent = self.TopButtonsParentEntity,text="Save",color = color.blue,radius  = 0,position =(-0.437, 0, -25),scale = (1/11,0.7),always_on_top = True) #Vec3(0.179, 0.0385, 1)
        self.FinishProjectButton = Button(parent = self.TopButtonsParentEntity,text="Finish",color = color.blue,radius  = 0,position =(-0.337, 0, -25),scale = (1/11,0.7),on_click = self.FinishProject,always_on_top = True) #Vec3(0.179, 0.0385, 1)
        self.PlayProjectButton = Button(parent = self.TopButtonsParentEntity,text="Play",color = color.blue,radius  = 0,position =(-0.237, 0, -25),scale = (1/11,0.7),always_on_top = True) #Vec3(0.179, 0.0385, 1)


        #  = self.ProjectTabsScrollEntity.add_script(Scrollable())

        # self.AddTabsMenuButtons()

    def updateVal(self):
        if len(self.ProjectTabsScrollEntity.children) == 4:
            self.val = self.val - .13
        else:
            self.val = self.val - .096

    def FinishProject(self):
        invoke(self.ShowCustomWindow,ToEnable = self.CancelFinishingProject,Title = "Export to py",OnEnable = self.ShowFinishProjectMenu,
               CalcAndAddTextLines = False,ToAddHeight = 3,
               Content = [Text("Note: You can later export the project to cpp.\nWhen it is implemented ;)\n\nNote: There will be a folder named 'Exported games'\n           in your selected dir and your game will be saved in \n           that folder in a .py format."),
                          Button(color = color.rgba(255,255,255,125),text  = "Open file selector",highlight_color = color.blue,on_click = Sequence(Func(self.ExportToPy),Func(self.DestroyCurrentWindow))),
                          Button(color = color.rgba(255,255,255,125),text  = "Cancel",highlight_color = color.blue,click_to_destroy = True)],
                          delay = .1)


    def ShowFinishProjectMenu(self):
        self.EditorCamera.disable()
        for i in range(len(self.CurrentTabs)):
            if isinstance(self.CurrentTabs,SceneEditor):
                self.CurrentTabs[i].IsEditing = False

    def ExportToPy(self):
        self.ExportToPyFunc(OpenSeletor())

    def CancelFinishingProject(self):
        self.EditorCamera.enable()
        for i in range(len(self.CurrentTabs)):
            if isinstance(self.CurrentTabs,SceneEditor):
                self.CurrentTabs[i].IsEditing = True

    def EnableEditor(self,EditorsOldestAncestor):
        EditorsOldestAncestor.enable()
        for i in range(len(EditorsOldestAncestor.children)):
            EditorsOldestAncestor.children[i].enable()
            if len(EditorsOldestAncestor.children[i].children) > 0:
                self.EnableEditor(EditorsOldestAncestor.children[i])

    def ShowCustomWindow(self,ToEnable,OnEnable,Title = "Info",CalcAndAddTextLines  = True,ToAddHeight = 0,Content = None):
        self.CurrentCustomWindow = CustomWindow(ToEnable=ToEnable,title = Title,OnEnable=OnEnable,
                CalcAndAddTextLines = CalcAndAddTextLines,ToAddHeight = ToAddHeight,content = Content)


    def ShowTabMenu(self):
        # print(len(self.CurrentTabs))
        if self.IsEditing:
            if not held_keys["control"] and not held_keys["shift"] and not held_keys["alt"]:
                if round(self.TabsMenuParentEntity.y,2) == 0.39:
                    self.TabsMenuParentEntity.animate_position(Vec3(0, 0.5, 0),.5)
                else:
                    self.TabsMenuParentEntity.animate_position(Vec3(0, 0.39, 0),.5)
        
        # a = ",".join([str(self.CurrentTabs[i].name) for i in range(len(self.CurrentTabs))])
        # print(",".join([str(self.CurrentTabs[i].name.replace("_"," ").capitalize()) for i in range(len(self.CurrentTabs))]))

    def UpdateTabsMenu(self):
        # for i in range(len())
        self.ProjectTabsScrollEntity.children.append(Button(text=self.CurrentTabs[len(self.ProjectTabsScrollEntity.children)].name,parent = self.ProjectTabsScrollEntity,scale = (.28,.4),position = (len(self.ProjectTabsScrollEntity.children)/3+.2,0,-22),radius=0,render_queue = self.ProjectTabsScrollEntity.render_queue))
        self.ProjectTabsScrollEntity.children[-1].text_entity.render_queue = self.ProjectTabsScrollEntity.render_queue
        self.ProjectTabsScrollEntity.children[-1].text_entity.wordwrap = 10
        self.ProjectTabsScrollEntity.children[-1].text_entity.scale -= .1


        for i in range(len(self.ProjectTabsScrollEntity.children)):
            self.ProjectTabsScrollEntity.children[i].text_entity.render_queue = self.ProjectTabsScrollEntity.children[i].text_entity.render_queue

        if len(self.ProjectTabsScrollEntity.children) > 3:
            if len(self.ProjectTabsScrollEntity.children) == 4:
                self.ProjectTabsScrollEntity.scale_x = self.ProjectTabsScrollEntity.scale_x+ .14
            else:
                self.ProjectTabsScrollEntity.scale_x = self.ProjectTabsScrollEntity.scale_x+ .09582

            for i in range(len(self.ProjectTabsScrollEntity.children)):
                self.ProjectTabsScrollEntity.children[0].x = .08 / self.ProjectTabsScrollEntity.scale_x
                self.ProjectTabsScrollEntity.children[i].scale_x = .08 / self.ProjectTabsScrollEntity.scale_x
                self.ProjectTabsScrollEntity.children[i].text = self.ProjectTabsScrollEntity.children[i].text 
                self.ProjectTabsScrollEntity.children[i].text_entity.render_queue = self.ProjectTabsScrollEntity.children[i].text_entity.render_queue
                self.ProjectTabsScrollEntity.children[i].text_entity.scale -= .1

            for i in range(1,len(self.ProjectTabsScrollEntity.children)):
                self.ProjectTabsScrollEntity.children[i].x = self.ProjectTabsScrollEntity.children[i-1].x + (self.ProjectTabsScrollEntity.children[i].scale_x) * 1.2
                # print(self.ProjectTabsScrollEntity.children[i-1].x + (self.ProjectTabsScrollEntity.children[i].scale_x) * 1.2)
            self.updateVal()
            self.Scroller.update_target("min",self.val)

    def AddTabsMenuButtons(self):

        ...

    def PrintItemStatTemp(self,Entity):
        for i in range(len(Entity.children)):
            print(f"name: {Entity.children[i].name} position = {Entity.children[i].position},rotation = {Entity.children[i].rotation},scale = {Entity.children[i].scale}")
            if len(Entity.children[i].children) > 0:
                self.PrintItemStatTemp(Entity.children[i])

    def DestroyCurrentWindow(self):
        self.CurrentCustomWindow.PlayerNotQuitting()
        # print("hi")

    def SetUp(self):
        self.AddEditorToPrjectButton.position = Vec3(0.476, 0, -23)
        self.AddEditorToPrjectButton.scale = Vec3(0.0299989, 0.369998, 1)
        self.AddEditorToPrjectButton.text = self.AddEditorToPrjectButton.text
        self.AddEditorToPrjectButton.text_entity.render_queue = self.AddEditorToPrjectButton.render_queue

        self.val = .22
        self.Scroller  = self.ProjectTabsScrollEntity.add_script(Scrollable(axis = "x",scroll_speed = 0.004,min = self.val,max = .2))


if __name__ == "__main__":
    from CodeEditorPython import CodeEditorPython
    from ursina import print_on_screen
    app = Ursina()
    cam = EditorCamera()
    Sky()
    editor = ProjectEditor(ExportToPyFunc=Func(print_on_screen,"<color:red>yeah <color:blue>yes"),CurrentTabs=[SceneEditor(EditorCamera=cam,enabled=False,WorldItems=[],ToImport=set(),SaveFunction=Func(print,'hi'),ShowInstructionFunc=Func(print,"e")),CodeEditorPython(enabled=False)],EditorCamera=cam)
    editor.AddTabsMenuButtons()
    top,left = 0.001,0.001
    editor.SetUp()
    # def input(key):
    #     if key == "-":
    #         editor.UpdateTabsMenu()

    toedit = editor.AddEditorToPrjectButton
    # print(editor.CurrentTabs)


    def input(key):
        global top,bottom,left,right,toedit
        if key == "-":
            editor.UpdateTabsMenu()
        if key in ["w","w hold"] and not held_keys["shift"]:
            # top += .001

            toedit.y += top
        elif key in ["s","s hold"] and not held_keys["shift"]:
            # bottom += .001
            toedit.y -= top
        elif key in ["a","a hold"] and not held_keys["shift"]:
            # left += .001
            toedit.x -= left
        elif key in ["d","d hold"] and not held_keys["shift"]:
            # right += .001
            toedit.x += left

        elif key in ["r","r hold"] and not held_keys["shift"]:
            # left += .001
            toedit.scale_x += left
            toedit.collider = toedit.collider
        elif key in ["t","t hold"] and not held_keys["shift"]:
            # right += .001
            toedit.scale_y += left
            toedit.collider = toedit.collider

        elif key in ["r","r hold"] and held_keys["shift"]:
            # left += .001
            toedit.scale_x -= left
            toedit.collider = toedit.collider
        elif key in ["t","t hold"] and held_keys["shift"]:
            # right += .001
            toedit.scale_y -= left
            toedit.collider = toedit.collider

        elif key == "up arrow":
            left += 0.001
            top += 0.001
        elif key == "down arrow":
            left -= 0.001
            top -= 0.001

        # elif key == "o":
        #     if toedit == editor.TempButton1 :
        #         toedit = editor.TempButton2
        #     elif toedit == editor.TempButton2 :
        #         toedit = editor.TempButton1

        elif key == "p":
            # dis = 0
            # ray = raycast(origin=editor.TempButton1.position,direction=editor.TempButton2.position,traverse_target=editor.TempButton2,debug=True)
            # if ray.hit:
            # print(ray.hit)
            # print(dis)
            editor.PrintItemStatTemp(editor.UniversalParentEntity)

    # def update():
    #     if held_keys["1"]:
    #         editor.TabsMenuParentEntity.radius += 0.001
    #     if held_keys["2"]:
    #         editor.TabsMenuParentEntity.radius -= 0.001

    app.run()