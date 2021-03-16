import glfw
from OpenGL.GL import *
import numpy as np

# Scale by 0.9 times in y direction
W = np.array([[1., 0., 0.],
              [0., .9, 0.],
              [0., 0., 1.]])

# Scale by 1.1 times in y direction
E = np.array([[1., 0., 0.],
              [0., 1.1, 0.],
              [0., 0., 1.]])

ten_degree = np.pi / 18

# Rotate by 10 degrees counterclockwise
S = np.array([[np.cos(ten_degree), -np.sin(ten_degree), 0.],
              [np.sin(ten_degree), np.cos(ten_degree),  0.],
              [0.,        0.,           1.]])

# Rotate by 10 degrees clockwise
D = np.array([[np.cos(-ten_degree), -np.sin(-ten_degree), 0.],
              [np.sin(-ten_degree), np.cos(-ten_degree),0.],
              [0.,        0.,           1.]])

# Translate by 0.1 in x direction
X = np.array([[1., 0., .1],
              [0., 1., 0.],
              [0., 0., 1.]])


# Translate by -0.1 in x direction
C = np.array([[1., 0., -.1],
              [0., 1., 0.],
              [0., 0., 1.]])

# Reflection across the origin
R = np.array([[-1., 0., 0.],
              [0., -1., 0.],
              [0., 0., 1.]])

Keyboard1 = np.identity(3)

buffer = Keyboard1

keys = [glfw.KEY_W, glfw.KEY_E, glfw.KEY_S, glfw.KEY_D, glfw.KEY_X, glfw.KEY_C, glfw.KEY_R]

matrix_arrays = [W, E, S, D, X, C, R]

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global buffer, keys

    if key == glfw.KEY_1:
        if action == glfw.REPEAT or action == glfw.PRESS:
            buffer = Keyboard1

    for index, glkey in enumerate(keys):
        if glkey == key:
            if action == glfw.REPEAT or action == glfw.PRESS:
                buffer = matrix_arrays[index] @ buffer
        
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

    glfw.swap_interval(1)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
        
        # Render here, e.g. using pyOpenGL
        render(buffer)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()