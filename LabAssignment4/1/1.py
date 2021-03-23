import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def do_Q():
    glTranslatef(-0.1, 0., 0.)
def do_E():
    glTranslatef(0.1, 0., 0.)
def do_A():
    glRotatef(10, 0, 0, 1)
def do_D():
    glRotatef(-10, 0, 0, 1)

buffer = []

keys = [glfw.KEY_Q, glfw.KEY_E, glfw.KEY_A, glfw.KEY_D]
matrix_arrays = [do_Q, do_E, do_A, do_D]

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    
    glColor3ub(255, 255, 255)
    
    for func in list(reversed(buffer)):
        func()

    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global buffer, keys

    if key == glfw.KEY_1:
        if action == glfw.REPEAT or action == glfw.PRESS:
            buffer = []

    for index, glkey in enumerate(keys):
        if glkey == key:
            if action == glfw.REPEAT or action == glfw.PRESS:
                buffer.append(matrix_arrays[index])
 
def main():
    if not glfw.init():
        return

    window = glfw.create_window(480, 480, '2017029870', None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()