from cmu_112_graphics import *

def appStarted(app):
    pass

def mousePressed(app,event):
    app.cx,app.cy = event.cx,event.cy
    newTree = appleTree(app.cx,app.cy)

# apple tree
class appleTree:
    def __init__(self,cx,cy):
        app.