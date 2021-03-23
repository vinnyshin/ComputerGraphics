import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def render(th):
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
    glColor3ub(255, 255, 255)
    
    
    R = np.identity(3)
    R[:2,:2] = [[np.cos(th),-np.sin(th)],
                [np.sin(th), np.cos(th)]]
    T = np.identity(3)
    T[:2, 2] = [.5, 0.]
    M1 = R @ T
    
    T = np.identity(3)
    T[:2, 2] = [.0, .5]
    M2 = R @ T

    # draw point p
    glBegin(GL_POINTS)
    glVertex2fv((M1 @ np.array([0.5, 0.0, 1.0]))[:-1])
    glVertex2fv((M2 @ np.array([0.0, 0.5, 1.0]))[:-1])
    glEnd()
    # draw vector v
    glBegin(GL_LINES)
    glVertex2fv((M1 @ np.array([0.0, 0.0, 0.0]))[:-1])
    glVertex2fv((M1 @ np.array([0.5, 0.0, 0.0]))[:-1])
    
    glVertex2fv((M1 @ np.array([0.0, 0.0, 0.0]))[:-1])
    glVertex2fv((M1 @ np.array([0.0, 0.5, 0.0]))[:-1])
    glEnd()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(480, 480, '2017029870', None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        t = glfw.get_time()

        render(-t)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()