import math
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
is_animate = False


class Node(object):
    def __init__(self, type, name):
        # for debugging
        self.type = type
        self.name = name
        self.offset = []
        self.num_of_channels = 0
        self.channels = []
        self.children = []
        self.rotation_matrix = []

    def add_child(self, obj):
        self.children.append(obj)

    def get_offset_length(self):
        return math.sqrt(self.offset[0] ** 2 + self.offset[1] ** 2 + self.offset[2] ** 2)

    def __str__(self):
        return f'str : {self.name}'

def drawCube_glVertex(child):
    line_length = child.get_offset_length()
    side_length = 0.025
    # side_length = 1.0

    glBegin(GL_QUADS)

    # 윗면
    glNormal3f(0, 1, 0)
    glVertex3f(side_length, line_length, -side_length)
    glVertex3f(-side_length, line_length, -side_length)
    glVertex3f(-side_length, line_length, side_length)
    glVertex3f(side_length, line_length, side_length)

    # 밑면
    glNormal3f(0, -1, 0)
    glVertex3f(side_length, 0, side_length)
    glVertex3f(-side_length, 0, side_length)
    glVertex3f(-side_length, 0, -side_length)
    glVertex3f(side_length, 0, -side_length)

    # 앞면
    glNormal3f(0, 0, 1)
    glVertex3f(side_length, line_length, side_length)
    glVertex3f(-side_length, line_length, side_length)
    glVertex3f(-side_length, 0, side_length)
    glVertex3f(side_length, 0, side_length)

    # 뒷면
    glNormal3f(0, 0, -1)
    glVertex3f(side_length, 0, -side_length)
    glVertex3f(-side_length, 0, -side_length)
    glVertex3f(-side_length, line_length, -side_length)
    glVertex3f(side_length, line_length, -side_length)

    # 왼쪽 면
    glNormal3f(-1, 0, 0)
    glVertex3f(-side_length, line_length, side_length)
    glVertex3f(-side_length, line_length, -side_length)
    glVertex3f(-side_length, 0, -side_length)
    glVertex3f(-side_length, 0, side_length)

    #오른쪽 면
    glNormal3f(1, 0, 0)
    glVertex3f(side_length, line_length, -side_length)
    glVertex3f(side_length, line_length, side_length)
    glVertex3f(side_length, 0, side_length)
    glVertex3f(side_length, 0, -side_length)
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

def rotate_to_child_offset(child):
    x = child.offset[0]
    y = child.offset[1]
    z = child.offset[2]

    r = child.get_offset_length()

    azimuth = np.arctan2(x, z)
    azimuth = np.rad2deg(azimuth)

    theta = np.arccos(y / r)
    theta = np.rad2deg(theta)

    glRotatef(azimuth, 0, 1, 0)
    glRotatef(theta, 1, 0, 0)

def draw_Tpose(root):
    # root is empty
    if root.type == '':
        return

    # pre-order traversal

    glPushMatrix()
    preorder_Tpose(root)
    glPopMatrix()

def preorder_Tpose(parent):
    parent_offset_x = parent.offset[0]
    parent_offset_y = parent.offset[1]
    parent_offset_z = parent.offset[2]

    for child in parent.children:
        glPushMatrix()
        glTranslatef(parent_offset_x, parent_offset_y, parent_offset_z)

        glPushMatrix()
        rotate_to_child_offset(child)
        drawCube_glVertex(child)
        glPopMatrix()

        glBegin(GL_LINES)
        # root 한번 찍고
        glVertex3fv(np.array([0., 0., 0.]))
        # child 한번 찍고
        glVertex3fv(np.array(child.offset))
        glEnd()
        preorder_Tpose(child)
        glPopMatrix()

def animate_motion(root):
    global frame_data, frames, frame_time
    # root is empty
    if root.type == '':
        return

    frame = int(glfw.get_time() / frame_time) % frames

    glPushMatrix()

    root_position_x = frame_data[frame][0]
    root_position_y = frame_data[frame][1]
    root_position_z = frame_data[frame][2]

    glTranslatef(root_position_x, root_position_y, root_position_z)
    preorder_motion(root, frame)
    glPopMatrix()

def preorder_motion(parent, frame):
    parent_offset_x = parent.offset[0]
    parent_offset_y = parent.offset[1]
    parent_offset_z = parent.offset[2]

    for child in parent.children:
        glPushMatrix()
        glTranslatef(parent_offset_x, parent_offset_y, parent_offset_z)
        glMultMatrixf(parent.rotation_matrix[frame].T)

        glPushMatrix()
        rotate_to_child_offset(child)
        drawCube_glVertex(child)
        glPopMatrix()

        glBegin(GL_LINES)
        # root 한번 찍고
        glVertex3fv(np.array([0., 0., 0.]))
        # chile 한번 찍고
        glVertex3fv(np.array(child.offset))
        glEnd()
        preorder_motion(child, frame)
        glPopMatrix()

def lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_RESCALE_NORMAL)

    glPushMatrix()
    lightPos = (3., 4., 5., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()

    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)

    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    objectColor = (1., 1., 0., 1.)
    specularObjectColor = (1., 1., 1., 1.)

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)


def render(root):
    global gCamAng, gCamHeight, panningPosX, panningPosY, currentZoomLevel, isOrthoEnabled, is_animate
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 100000)
    
    if isOrthoEnabled:
        glLoadIdentity()
        glOrtho(-3, 3, -3, 3, -30, 30)

    glTranslatef(0,0, currentZoomLevel)
    glTranslatef(panningPosX, panningPosY, 0)

    glRotatef(gCamHeight, 1, 0, 0)
    glRotatef(36.264, 1, 0, 0)
    glRotatef(gCamAng, 0, 1, 0)
    glRotatef(-45, 0, 1, 0)

    drawRectGrid()
    drawFrame()

    lighting()

    glPushMatrix()
    # glScalef(0.02, 0.02, 0.02)
    if is_animate:
        animate_motion(root)
    else:
        draw_Tpose(root)

    glPopMatrix()
    glDisable(GL_LIGHTING)

def key_callback(window, key, scancode, action, mods):
    global isOrthoEnabled, is_animate
    if key==glfw.KEY_V and action==glfw.PRESS:
        isOrthoEnabled = not isOrthoEnabled
    elif key==glfw.KEY_SPACE and action==glfw.PRESS:
        is_animate = not is_animate

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

def drop_callback(window, paths):
    global root, frames, frame_time, frame_data

    file = open(paths.pop(), 'r')

    level = -1
    hierarchy = []
    current_node = None
    channel_list = []
    preorder_traversal_stack = []
    frame_data = []

    # Parsing
    while True:
        line = file.readline()

        if not line:
            break

        split_line = line.split()

        if len(split_line) == 0:
            continue

        symbol = split_line[0]

        if symbol == '{':
            level += 1
            hierarchy.append(current_node)
            if current_node.name != 'End Site':
                preorder_traversal_stack.append(current_node)

        elif symbol == '}':
            level -= 1
            # Pop last
            hierarchy.pop()
            # If not empty
            if level != -1:
                # Make it point to last one
                current_node = hierarchy[len(hierarchy) - 1]
            # print(current_node)
            # print(current_node.channels)
            # for child in current_node.children:
            #     print(child.name, end=', ')
            # print()

        elif symbol == 'OFFSET':
            # e.g. ['OFFSET', '0.0', '0.0', '0.0']
            offset = [float(split_line[1]), float(split_line[2]), float(split_line[3])]
            current_node.offset = offset

        elif symbol == 'CHANNELS':
            # e.g. ['CHANNELS', '6', 'XPOSITION', 'YPOSITION', 'ZPOSITION', 'XROTATION', 'YROTATION', 'ZROTATION']
            split_line.pop(0) # Removing 'CHANNELS'
            num_of_channels = split_line.pop(0)
            channels = split_line
            channel_list.extend(channels)
            current_node.num_of_channels = num_of_channels
            current_node.channels = channels

        elif symbol == 'JOINT':
            # ['JOINT', 'Spine']
            type = symbol
            name = split_line[1]
            child = Node(type, name)
            current_node.add_child(child)
            current_node = child

        elif symbol == 'End':
            type = 'End Site'
            name = 'End Site'
            child = Node(type, name)
            current_node.add_child(child)
            current_node = child

        elif symbol == 'ROOT':
            # e.g. ['ROOT', 'Hips']
            type = symbol
            name = split_line[1]
            root = Node(type, name)
            current_node = root

        elif symbol == 'MOTION' or symbol == 'HIERARCHY':
            continue

        elif symbol == 'Frames:':
            # Frames: 199
            frames = int(split_line[1])

        elif symbol == 'Frame':
            # Frame Time: 0.033333
            frame_time = float(split_line[2])

        else:
            # frame motion data
            frame_data_float = []
            for number in split_line:
                frame_data_float.append(float(number))
            frame_data.append(frame_data_float)

    # Computing a rotation matrix
    for frame_row_data in frame_data:
        # Starting from root 'ZROTATION'
        # 0         1         2         3         4         5
        # XPOSITION YPOSITION ZPOSITION ZROTATION XROTATION YROTATION
        column = 3

        # 각 frame 정보들에 대하여 node들의 matrix값을 계산해주어야 함
        for node in preorder_traversal_stack:
            matrix = np.identity(3)
            # 3번씩 반복한다.
            for _ in range(3):
                rotation = channel_list[column]
                degree = frame_row_data[column]
                if rotation.upper() == 'XROTATION':
                    matrix = matrix @ np.array([[1, 0, 0],
                                                [0, np.cos(np.deg2rad(degree)), -np.sin(np.deg2rad(degree))],
                                                [0, np.sin(np.deg2rad(degree)), np.cos(np.deg2rad(degree))]])
                elif rotation.upper() == 'YROTATION':
                    matrix = matrix @ np.array([[np.cos(np.deg2rad(degree)), 0, np.sin(np.deg2rad(degree))],
                                                [0, 1, 0],
                                                [-np.sin(np.deg2rad(degree)), 0, np.cos(np.deg2rad(degree))]])
                elif rotation.upper() == 'ZROTATION':
                    matrix = matrix @ np.array([[np.cos(np.deg2rad(degree)), -np.sin(np.deg2rad(degree)), 0],
                                                [np.sin(np.deg2rad(degree)), np.cos(np.deg2rad(degree)), 0],
                                                [0, 0, 1]])
                column += 1
            rotation_matrix = np.identity(4)
            rotation_matrix[:3, :3] = matrix
            node.rotation_matrix.append(rotation_matrix)

    # Printing file information
    file_name = file.name.split('\\').pop()
    print('File name : ', file_name)
    print('Number of frames : ', frames)
    print('FPS : ', 1/frame_time)
    print('Number of joints : ', len(preorder_traversal_stack))
    print('List of all joint names (pre-order) : ', end="")
    for node in preorder_traversal_stack:
        print(node.name, end= " ")
    print()

root = Node('', '')
frames = 0
frame_time = 0

def main():
    global root

    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1280, 1280, "ClassAssignment3", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    # Make the window's context current
    glfw.make_context_current(window)

    glfw.swap_interval(1)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        render(root)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
