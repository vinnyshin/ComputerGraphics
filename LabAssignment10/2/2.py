import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.


def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -1 ,  1 ,  1 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  1 ,  1 ,  1 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  1 , -1 ,  1 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -1 , -1 ,  1 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -1 ,  1 , -1 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  1 ,  1 , -1 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  1 , -1 , -1 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,3.]))
    glEnd()

def exp(rv):
    # 크기는 Theta, 방향은 V
    # Theta 단위는 라디안
    theta = np.sqrt(np.dot(rv, rv))
    if theta == 0:
        return np.identity(3)
    rv_unit = rv / theta

    x_unit = rv_unit[0]
    y_unit = rv_unit[1]
    z_unit = rv_unit[2]

    R00 = np.cos(theta) + x_unit**2 * (1 - np.cos(theta))
    R01 = x_unit * y_unit * (1 - np.cos(theta)) - z_unit * np.sin(theta)
    R02 = x_unit * z_unit * (1 - np.cos(theta)) + y_unit * np.sin(theta)
    R10 = y_unit * x_unit * (1 - np.cos(theta)) + z_unit * np.sin(theta)
    R11 = np.cos(theta) + y_unit**2 * (1 - np.cos(theta))
    R12 = y_unit * z_unit * (1 - np.cos(theta)) - x_unit * np.sin(theta)
    R20 = z_unit * x_unit * (1 - np.cos(theta)) - y_unit * np.sin(theta)
    R21 = z_unit * y_unit * (1 - np.cos(theta)) + x_unit * np.sin(theta)
    R22 = np.cos(theta) + z_unit**2 * (1 - np.cos(theta))
    
    R = np.array([[R00, R01, R02],
                  [R10, R11, R12],
                  [R20, R21, R22]])

    return R

def log(R):
    trR = R[0][0] + R[1][1] + R[2][2]

    w = None
    theta = None
    theta = np.arccos((trR - 1) / 2)

    v1 = (R[2][1] - R[1][2]) / (2 * np.sin(theta))
    v2 = (R[0][2] - R[2][0]) / (2 * np.sin(theta))
    v3 = (R[1][0] - R[0][1]) / (2 * np.sin(theta))
        
    w = np.array([v1, v2, v3])
    return theta * w

def slerp(R1, R2, t):
    return R1 @ exp(t * log(R1.T @ R2))

def makeEulerXYZRotationMatrix(x, y, z):
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(np.deg2rad(x)), -np.sin(np.deg2rad(x))],
                   [0, np.sin(np.deg2rad(x)), np.cos(np.deg2rad(x))]])

    Ry = np.array([[np.cos(np.deg2rad(y)), 0, np.sin(np.deg2rad(y))],
                   [0, 1, 0],
                   [-np.sin(np.deg2rad(y)), 0, np.cos(np.deg2rad(y))]])
          
    Rz = np.array([[np.cos(np.deg2rad(z)), -np.sin(np.deg2rad(z)), 0],
                   [np.sin(np.deg2rad(z)),  np.cos(np.deg2rad(z)), 0],
                   [0, 0, 1]])
    return Rx @ Ry @ Rz

def setInnerFrame(objectColorList, R1List, R2List):
    for i in range(len(R1List)):
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColorList[i])
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

        R1 = np.identity(4)
        R1[:3, :3] = R1List[i]
        J1 = R1
        
        glPushMatrix()
        glMultMatrixf(J1.T)
        glPushMatrix()
        glTranslatef(0.5,0,0)
        glScalef(0.5, 0.05, 0.05)
        drawCube_glDrawElements()
        glPopMatrix()
        glPopMatrix()

        R2 = np.identity(4)
        R2[:3, :3] = R2List[i]
        T1 = np.identity(4)
        T1[0][3] = 1.

        J2 = R1 @ T1 @ R2

        glPushMatrix()
        glMultMatrixf(J2.T)
        glPushMatrix()
        glTranslatef(0.5,0,0)
        glScalef(0.5, 0.05, 0.05)
        drawCube_glDrawElements()
        glPopMatrix()
        glPopMatrix()

def setLight():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

def interpolateInnerFrame(frame, R1List, R2List):
    objectColor = (1., 1., 1., 1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    mode = 0
    
    # 0 ... 19
    if frame < 20:
        mode = 0
    # 20 ... 39
    elif frame < 40:
        mode = 1
    # 40 ... 59
    elif frame < 60:
        mode = 2
        
    t = (frame % 20 / 20)
    
    R1Slerp = slerp(R1List[mode], R1List[mode + 1], t)
    R2Slerp = slerp(R2List[mode], R2List[mode + 1], t)
    glPushMatrix()
    
    R1 = np.identity(4)
    R1[:3, :3] = R1Slerp
    J1 = R1
    
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    R2 = np.identity(4)
    R2[:3, :3] = R2Slerp
    T1 = np.identity(4)
    T1[0][3] = 1.

    J2 = R1 @ T1 @ R2

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()

    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

def render(frame, R1List, R2List):
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    # draw global frame
    drawFrame()

    setLight()
    
    # 차례로 Red, Yello, Green, Blue
    objectColorList = [(1.,0.,0.,1.), (1.,1.,0.,1.), (0.,1.,0.,1.), (0.,0.,1.,1.)]
    setInnerFrame(objectColorList, R1List, R2List)
    interpolateInnerFrame(frame, R1List, R2List)

    glDisable(GL_LIGHTING)


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2017029870', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    frame = 0

    R1Frame0 = makeEulerXYZRotationMatrix(20, 30, 30)
    R2Frame0 = makeEulerXYZRotationMatrix(15, 30, 25)

    R1Frame20 = makeEulerXYZRotationMatrix(45, 60, 40)
    R2Frame20 = makeEulerXYZRotationMatrix(25, 40, 40)

    R1Frame40 = makeEulerXYZRotationMatrix(60, 70, 50)
    R2Frame40 = makeEulerXYZRotationMatrix(40, 60, 50)

    R1Frame60 = makeEulerXYZRotationMatrix(80, 85, 70)
    R2Frame60 = makeEulerXYZRotationMatrix(55, 80, 65)

    R1List = [R1Frame0, R1Frame20, R1Frame40, R1Frame60]
    R2List = [R2Frame0, R2Frame20, R2Frame40, R2Frame60]

    while not glfw.window_should_close(window):
        glfw.poll_events()
        frame = frame % 61
        render(frame, R1List, R2List)
        frame += 1
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

