###################################################
# [Practice] First OpenGL Program
import glfw
from OpenGL.GL import *
import numpy as np

N_POLYGON = 12
input_key = glfw.KEY_W
keys = [glfw.KEY_3, glfw.KEY_2, glfw.KEY_1, glfw.KEY_W, glfw.KEY_Q, glfw.KEY_0, glfw.KEY_9, glfw.KEY_8, glfw.KEY_7, glfw.KEY_6, glfw.KEY_5, glfw.KEY_4]

def makeVertexArray():
    theta_array = np.arange(N_POLYGON)
    theta_array = theta_array * 2 * (1/N_POLYGON) * np.pi

    sin_array = np.sin(theta_array)
    cos_array = np.cos(theta_array)

    xy_array = np.array([cos_array, sin_array], dtype='float32')
    
    return xy_array

def render(): 
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    glBegin(GL_LINE_LOOP)
    array = makeVertexArray()
    for i in range(N_POLYGON):
        glVertex2f(array[0, i], array[1, i])
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(0.0, 0.0)
    for glkey in keys:
        index = keys.index(glkey)
        if input_key == glkey:
            glVertex2f(array[0, index], array[1, index])
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global input_key, keys
    for glkey in keys:
        if key == glkey:
            input_key = key
    
def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2017029870", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

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
