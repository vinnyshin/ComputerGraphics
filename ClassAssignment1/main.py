import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

isLeftMousePressed = False
isRightMousePressed = False

initialCamPosX = 0
initialCamPosY = 0
lastCamPosX = 0
lastCamPosY = 0
gCamAng = 0
gCamHeight = 0

panningPosX = 0.
panningPosY = 0.
lastPanningPosX = 0.
lastPanningPosY = 0.

currentZoomLevel = -10

isOrthoEnabled = False

def drawUnitCube():
    glBegin(GL_QUADS)
    glColor3ub(0, 0, 100)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glColor3ub(50, 50, 100)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
    
    glColor3ub(100, 100, 100)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)

    glColor3ub(150, 150, 100)
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glColor3ub(200, 200, 100)
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 

    glColor3ub(250, 250, 100)           
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-15.,0.,0.]))
    glVertex3fv(np.array([15.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,-15.,0.]))
    glVertex3fv(np.array([0.,15.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,-15.]))
    glVertex3fv(np.array([0.,0.,15.]))
    glEnd()

def drawRectGrid():
    glBegin(GL_LINES)
    glColor3ub(255,255,255)

    rows = 30
    columns = 30

    for i in range(rows):
        glVertex3f(i - rows / 2, 0, -columns)
        glVertex3f(i - rows / 2, 0, columns)    
    
    for i in range(columns):
        glVertex3f(-rows, 0, i - columns / 2)
        glVertex3f(rows, 0, i - columns / 2)
    
    glEnd()

def render():
    global gCamAng, gCamHeight, panningPosX, panningPosY, currentZoomLevel, isOrthoEnabled
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    # glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()
    gluPerspective(45, 1, 1,30)
    
    if isOrthoEnabled:
        glLoadIdentity()
        glOrtho(-3,3, -3,3, -30,30)

    glTranslatef(0,0, currentZoomLevel)
    glTranslatef(panningPosX, panningPosY, 0)

    glRotatef(gCamHeight, 1, 0, 0)
    glRotatef(36.264, 1, 0, 0)
    glRotatef(gCamAng, 0, 1, 0)
    glRotatef(-45, 0, 1, 0)
    
    drawRectGrid()
    drawFrame()
    drawUnitCube()

def key_callback(window, key, scancode, action, mods):
    global isOrthoEnabled
    if key==glfw.KEY_V and action==glfw.PRESS:
        isOrthoEnabled = not isOrthoEnabled

def button_callback(window, button, action, mod):
    global isLeftMousePressed, isRightMousePressed
    global initialCamPosX, initialCamPosY, lastCamPosX, lastCamPosY
    global lastPanningPosX, lastPanningPosY

    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            isLeftMousePressed = True
            initialCamPosX, initialCamPosY = glfw.get_cursor_pos(window)

        elif action==glfw.RELEASE:
            isLeftMousePressed = False
            lastCamPosX = gCamAng
            lastCamPosY = gCamHeight

    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            isRightMousePressed = True
            initialCamPosX, initialCamPosY = glfw.get_cursor_pos(window)
        elif action==glfw.RELEASE:
            isRightMousePressed = False
            lastPanningPosX = panningPosX
            lastPanningPosY = panningPosY

def cursor_callback(window, xpos, ypos):
    global gCamAng, gCamHeight, lastCamPosX, lastCamPosY
    global panningPosX, panningPosY, lastPanningPosX, lastPanningPosY
    if isLeftMousePressed:
        gCamAng = lastCamPosX - (initialCamPosX - xpos) / 5
        gCamHeight = lastCamPosY - (initialCamPosY - ypos) / 5

    elif isRightMousePressed:
        panningPosX = lastPanningPosX - (initialCamPosX - xpos) / 100
        panningPosY = lastPanningPosY + (initialCamPosY - ypos) / 100

def scroll_callback(window, xoffset, yoffset):
    global currentZoomLevel
    currentZoomLevel += yoffset
    if currentZoomLevel > 0:
        currentZoomLevel = 0

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1280,1280,"Assignment1", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
        
        # Render here, e.g. using pyOpenGL
        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
