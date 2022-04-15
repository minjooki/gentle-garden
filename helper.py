# from cmu 112 graphics notes 
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html 
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'