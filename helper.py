# from cmu 112 graphics notes 
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html 
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

def clickedOn(cx,cy,x0,y0,width,height):
    x1 = x0 + width
    y1 = y0 + height

    if cx>x0 and cx<x1 and cy>y0 and cy<y1:
        return True
    return False