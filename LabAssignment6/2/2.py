###################################################
# [Practice] glFrustum(), gluPerspective()
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.
gCamHeight = 1.

gVertexArrayIndexed = None
gIndexArray = None

def createVertexAndIndexArrayIndexed(): 
    varr = np.array([
    ( -1 , 1 , 1 ), # v0
    ( 1 , 1 , 1 ), # v1
    ( 1 , -1 , 1 ), # v2
    ( -1 , -1 , 1 ), # v3
    ( -1 , 1 , -1 ), # v4
    ( 1 , 1 , -1 ), # v5
    ( 1 , -1 , -1 ), # v6
    ( -1 , -1 , -1 ), # v7
    ], 'float32')

    iarr = np.array([
    (0,3,2,1),
    (4,5,6,7),
    (0,1,5,4),
    (3,7,6,2),
    (1,2,6,5),
    (0,4,7,3),
    ])

    return varr, iarr

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def render():
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()

    gluPerspective(45, 1, 1, 10)
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()

    glScalef(3/4, 3/4, 3/4)
    glTranslatef(1.0, 1.0, 1.0)
    glColor3ub(255, 255, 255)
    drawCube_glDrawElements()
    
def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_QUADS, iarr.size, GL_UNSIGNED_INT, iarr)

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2017029870', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    
    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()