import wx
import cv2
import shutil
import os
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='will',
    password='toor',
    database='faceRegistration'
)

mycursor = mydb.cursor()
knownFacesPath = 'C:\\Users\\willi\\Documents\\GitHub\\FaceID\\knownFaces\\'

class MyFileDropTarget(wx.FileDropTarget):

    def __init__(self, window):

        wx.FileDropTarget.__init__(self)
        self.window = window
        self.path = None

    def OnDropFiles(self, x, y, filenames):

        self.window.SetInsertionPointEnd()
        self.window.updateText(f"{len(filenames)} file(s) dropped at {x},{y}:\n")
        self.path = filenames
        for filepath in filenames:
            self.window.updateText(filepath + '\n')  

        return True 

class MultiEnter(wx.Frame):

    def __init__(self, parent):
        super(MultiEnter, self).__init__(parent)
        self.parent = parent
        self.Centre()
        self.SetTitle('Enter Users')
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self)

        self.FileDropTarget = MyFileDropTarget(self)

        lbl = wx.StaticText(self.panel, label="Drag some files here:")
        self.fileTextCtrl = wx.TextCtrl(self.panel,
                                        style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
        self.fileTextCtrl.SetDropTarget(self.FileDropTarget)

        enterButton = wx.Button(self.panel, label='Enter Users', pos=(275, 5))
        enterButton.Bind(wx.EVT_BUTTON, self.onButton)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(lbl, 0, wx.ALL, 5)
        sizer.Add(self.fileTextCtrl, 1, wx.EXPAND|wx.ALL, 5)
        self.panel.SetSizer(sizer)

    def SetInsertionPointEnd(self):
        self.fileTextCtrl.SetInsertionPointEnd()

    def updateText(self, text):
        self.fileTextCtrl.WriteText(text)

    def enterUser(self, name, photo):
        sql = f"INSERT INTO pupils (name, photo) VALUES (%s, %s)" # sql to insert new user
        val = (name, photo)
        mycursor.execute(sql, val)
        mydb.commit()

    def getName(self, path, name):
        text = wx.TextEntryDialog(self.parent, f'Please enter full name for {name}:', 'Enter here...')
        text.ShowModal()
        name = text.GetValue()
        shutil.move(path, f'{knownFacesPath}{name}.jpg')
        return name


    def enter(self):
        paths = self.FileDropTarget.path
        for path in paths:
            for photo in os.listdir(path):
                if photo.split('.')[-1] == 'jpg':
                    fullPath = os.path.join(path, photo)
                    name = self.getName(fullPath, photo)
                    self.enterUser(name, fullPath)
                else:
                    print(f'{photo} is not a jpg.')


    def onButton(self, e):
        self.enter()
        self.Close()

    def main(self):
        self.Show()


class Delete(wx.Frame):

    def __init__(self, parent):
        super(Delete, self).__init__(parent)
        self.parent = parent
        self.dict = {}
        self.Centre()
        self.SetTitle('Delete User')

        self.InitUI()

    def InitUI(self):
        self.createDict()
        users = self.fetchUsers()
        self.panel = wx.Panel(self)
        checkboxes = []
        for i, (ID, name) in enumerate(users):
            pos=(10, (i*40)+30)
            label = wx.StaticText(self.panel, label=name, pos=(10, (i*40)+10))
            chbox = wx.CheckBox(self.panel, label=str(ID), pos=pos)
            checkboxes.append(chbox)
        
        enterButton = wx.Button(self.panel, label='Delete selected', pos = (250, 375))
        enterButton.Bind(wx.EVT_BUTTON, self.onButton)        

        self.Bind(wx.EVT_CHECKBOX, self.onChecked)

    def onButton(self, e):
        for pupils in self.dict:
            pupil = self.dict[pupils]
            if pupil['status']:
                ID = pupil['id']
                self.deleteUser(ID)
        self.Hide()

    def onChecked(self, e):
        cb = e.GetEventObject()
        self.dict[cb.GetLabel()]['status'] = cb.GetValue()
        print(self.dict[cb.GetLabel()]['status'])

    def deleteUser(self, user):
        sql = f"DELETE FROM pupils WHERE pupilID={user}"
        mycursor.execute(sql)
        mydb.commit()

    def fetchUsers(self):
        sql = "SELECT pupilID, name FROM pupils"
        mycursor.execute(sql)
        results = mycursor.fetchall()
        return results

    def createDict(self):
        users = self.fetchUsers()
        for ID, name in users:
            self.dict[str(ID)] = {'id':ID,
                            'name':name,
                            'status':False}

    def main(self):
        self.Show()

    

class CapturePanel(wx.Frame):

    def __init__(self, parent):
        super(CapturePanel, self).__init__(parent)
        self.parent = parent
        self.SetSize(wx.Size(1000, 500))
        self.Centre()
        self.SetTitle('Camera')
        self.result = None
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self)
        enterButton = wx.Button(self.panel, label='Save and Upload', pos = (850, 400))
        enterButton.Bind(wx.EVT_BUTTON, self.OnClick)

    def OnClick(self, e):
        name = self.result
        re = self.result.replace(' ', '_')
        shutil.move('imgCache\\frame.jpg', f'{knownFacesPath}{re}.jpg') # move captured frame into final destination
        sql = f"INSERT INTO pupils (name, photo) VALUES (%s, %s)" # sql to insert new user
        val = (name, f'{knownFacesPath}{re}.jpg')
        mycursor.execute(sql, val) # run sql
        mydb.commit()
        self.Close(True)

    def textShow(self):        
        label = wx.StaticText(self.panel, -1, f"""The name you have entered is {self.result}.


Press the cross to exit and re-enter info""", pos=(650, 50))

    def main(self):
        self.Show()
        text = wx.TextEntryDialog(self.parent, 'Please enter full name: ', 'Enter here...')
        text.ShowModal()
        self.result = text.GetValue()
        text.Destroy()
        cap = cv2.VideoCapture(0)

        while(cap.isOpened()):
            ret, frame = cap.read()

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(32) & 0xFF == ord(' '):
                cv2.imwrite('imgCache/frame.jpg', frame)
                break

        cap.release()
        cv2.destroyAllWindows()
        self.updateBackground()

    def updateBackground(self):
        try:
            # pick an image file you have in the working folder
            image_file = 'imgCache/frame.jpg'
            bmp1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            # image's upper left corner anchors at panel coordinates (0, 0)
            self.bitmap1 = wx.StaticBitmap(self, -1, bmp1, (0, 0))
        except IOError:
            print('No image found')

        self.textShow()



class MainUI(wx.Frame):

    def __init__(self, parent, title):
        super(MainUI, self).__init__(parent, title=title)
        
        self.capturePanel = CapturePanel(self)
        self.deletePanel = Delete(self)
        self.multiPanel = MultiEnter(self)

        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        menuQuit = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menuCamera = fileMenu.Append(wx.ID_ANY, 'Camera', 'Open Camera')
        menuDelete = fileMenu.Append(wx.ID_ANY, 'Delete', 'Delete User')
        menuMulti = fileMenu.Append(wx.ID_ANY, 'Multi-Enter', 'Enter multiple users')

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, menuQuit)
        self.Bind(wx.EVT_MENU, self.OnCamera, menuCamera)
        self.Bind(wx.EVT_MENU, self.OnDelete, menuDelete)
        self.Bind(wx.EVT_MENU, self.onMulti, menuMulti)

    def main(self):
        self.InitUI()
        self.Show()

    def onMulti(self, e):
        self.multiPanel = MultiEnter(self)
        self.multiPanel.main()


    def OnQuit(self, e):
        self.Close()

    def OnCamera(self, e):
        self.capturePanel = CapturePanel(self)
        self.capturePanel.main()
    
    def OnDelete(self, e):
        self.deletePanel = Delete(self)
        self.deletePanel.main()



def main():

    app = wx.App()
    UI = MainUI(None, title='Face Recognition Registration')
    UI.main()
    app.MainLoop()

if __name__ =='__main__':
    main()