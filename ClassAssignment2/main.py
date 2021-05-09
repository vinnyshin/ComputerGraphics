import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import re

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
isAnimateEnabled = False

varrList = []
varrListList = []

iarrList = []
iarrListList= []

normalList = []
normalListList = []

normalPointingListList = []
vertexPointingListList = []

gVertexArrayIndexed = np.array([])
gIndexArray = np.array([])
gVertexArrayIndexedList = []
gIndexArrayList = []
gNormalArrayList = []
gShaderNormalArrayList = []
gShaderVertexArrayList = []

wireframeMode = False
smoothMode = False

faceNormalList = []
faceNormalListList = []

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
    length = 3000
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-length,0.,0.]))
    glVertex3fv(np.array([length,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,-length,0.]))
    glVertex3fv(np.array([0.,length,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,-length]))
    glVertex3fv(np.array([0.,0.,length]))
    glEnd()

def drawRectGrid():
    glBegin(GL_LINES)
    glColor3ub(255,255,255)

    rows = 3000
    columns = 3000

    for i in range(rows):
        glVertex3f(i - rows / 2, 0, -columns)
        glVertex3f(i - rows / 2, 0, columns)    
    
    for i in range(columns):
        glVertex3f(-rows, 0, i - columns / 2)
        glVertex3f(rows, 0, i - columns / 2)
    
    glEnd()

def drop_callback(window, paths):
    global varrList, iarrList, normalList, gVertexArrayIndexed, gIndexArray, keyList, gVertexArrayIndexedList, gIndexArrayList, gNormalArrayList
    global varrListList, iarrListList, normalListList, normalPointingList, vertexPointingList, normalPointingListList, vertexPointingListList
    global gShaderNormalArrayList, gShaderVertexArrayList, faceNormalList, faceNormalListList

    totalNumberOfFaces = 0
    numberOfFacesWith3Vertices = 0
    numberOfFacesWith4Vertices = 0
    numberOfFacesWithMorethan4Vertices = 0
    
    isfirstOSymbol = True

    # Flushing previous data
    varrList = []
    iarrList = []
    normalList = []
    faceNormalList = []
    faceNormalListList = []

    normalPointingList = []
    vertexPointingList = []

    varrListList = []
    iarrListList = []
    normalListList = []

    normalPointingListList = []
    vertexPointingListList = []

    # taking the last among multiple files
    file = open(paths.pop(), 'r')
    currentKey = ''

    while True:

        line = file.readline()
        if not line: break

        # 'line' format
        # 'symbol(v, vn, f)' %(f, d), %(f, d), %(f, d)\n
        splitedLine = line.split()
        
        if len(splitedLine) == 0:
            continue
        
        symbol = splitedLine[0]
        
        if symbol == 'v':
            vertexTuple = (float(splitedLine[1]), float(splitedLine[2]), float(splitedLine[3]))
            varrList.append(vertexTuple)
        elif symbol == 'vn':
            vertexNomalTuple = (float(splitedLine[1]), float(splitedLine[2]), float(splitedLine[3]))
            normalList.append(vertexNomalTuple)
        elif symbol == 'f':
            totalNumberOfFaces += 1
            splitedLine.pop(0)
            verticeList = []
            normalvectorList = []

            for face in splitedLine:
                splitedFace = face.split('/')
            
                # appending vertices
                verticeList.append(int(splitedFace[0]) - 1)
                if len(splitedFace) == 3:
                    normalvectorList.append(int(splitedFace[2]) - 1)
                # format f %d / %d / %d
                # if len(splitedFace) == 3:        
                #     vertexPointingList.append(int(splitedFace[0]) - 1)
                #     normalPointingList.append(int(splitedFace[2]) - 1)
                    
            verticeTuple = tuple(verticeList)
            normalTuple = tuple(normalvectorList)

            if len(verticeTuple) == 3:
                numberOfFacesWith3Vertices += 1
                iarrList.append(verticeTuple)
                for index in verticeTuple:
                    vertexPointingList.append(index)
                if len(normalTuple) != 0:
                    for index in normalTuple:
                        normalPointingList.append(index)
                    normal1 = normalList[normalTuple[0]]
                    normal2 = normalList[normalTuple[1]]
                    normal3 = normalList[normalTuple[2]]
                    
                    normal1 = np.array(list(normal1), 'float32')
                    normal2 = np.array(list(normal2), 'float32')
                    normal3 = np.array(list(normal3), 'float32')
                    
                    newFaceNormal = (normal1 + normal2 + normal3)
                    newFaceUnitNormal = newFaceNormal / np.sqrt(np.dot(newFaceNormal, newFaceNormal))
                    faceNormalList.append(newFaceUnitNormal)
                    # faceNormalList.append(newFaceNormal)
            else:
                if len(verticeTuple) == 4:
                    numberOfFacesWith4Vertices += 1
                elif len(verticeTuple) > 4:
                    numberOfFacesWithMorethan4Vertices += 1
                # convex 만 가능한데 마음에 안들어..
                for i in range(1, len(verticeTuple) - 1):
                    tri_corner0 = verticeTuple[0]
                    tri_corner1 = verticeTuple[i]
                    tri_corner2 = verticeTuple[i + 1]
                    triTuple = (tri_corner0, tri_corner1, tri_corner2)
                    iarrList.append(triTuple)

                    vertexPointingList.append(verticeTuple[0])
                    vertexPointingList.append(verticeTuple[i])
                    vertexPointingList.append(verticeTuple[i + 1])

                    normalPointingList.append(normalTuple[0])
                    normalPointingList.append(normalTuple[i])
                    normalPointingList.append(normalTuple[i + 1])

                    normal1 = normalList[normalTuple[0]]
                    normal2 = normalList[normalTuple[i]]
                    normal3 = normalList[normalTuple[i + 1]]

                    normal1 = np.array(list(normal1), 'float32')
                    normal2 = np.array(list(normal2), 'float32')
                    normal3 = np.array(list(normal3), 'float32')

                    newFaceNormal = (normal1 + normal2 + normal3)
                    newFaceUnitNormal = newFaceNormal / np.sqrt(np.dot(newFaceNormal, newFaceNormal))
                    faceNormalList.append(newFaceUnitNormal)
                    # faceNormalList.append(newFaceNormal)

        elif symbol == 'o':
            if(isfirstOSymbol):
                isfirstOSymbol = False
                continue
            varrListList.append(varrList)
            iarrListList.append(iarrList)
            normalListList.append(normalList)
            faceNormalListList.append(faceNormalList)
            # print(faceNormalList)
            for index in range(len(vertexPointingList)):
                vertexPointingList[index] = varrList[vertexPointingList[index]]
            vertexPointingListList.append(np.array(vertexPointingList,'float32'))
            
            for index in range(len(normalPointingList)):
                normalPointingList[index] = normalList[normalPointingList[index]]
            normalPointingListList.append(np.array(normalPointingList, 'float32'))
            

            varrList = []
            iarrList = []
            normalList = []
           
            faceNormalList = []
            normalPointingList = []
            vertexPointingList = []
        else:
            # Not the parsing case
            continue


    varrListList.append(varrList)
    iarrListList.append(iarrList)
    normalListList.append(normalList)
    faceNormalListList.append(faceNormalList)
    # print()
    # print()
    # print()
    # print()
    # print(faceNormalList)
    for index in range(len(vertexPointingList)):
        vertexPointingList[index] = varrList[vertexPointingList[index]]
    vertexPointingListList.append(np.array(vertexPointingList,'float32'))
    
    for index in range(len(normalPointingList)):
        normalPointingList[index] = normalList[normalPointingList[index]]
    normalPointingListList.append(np.array(normalPointingList, 'float32'))

    
    # normalPointingListList.append(normalPointingList)
    # vertexPointingListList.append(vertexPointingList)

    # print("vertexListList: ", vertexPointingListList)
    # print("normalListList: ",normalPointingListList)
    # gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed(varrList, iarrList)
    gVertexArrayIndexedList, gIndexArrayList, gNormalArrayList = createVertexAndIndexArrayIndexedList(varrListList, iarrListList, normalListList)

    createGoraudShadingNormal()
    
    print('file name : ', file.name)
    print('totalNumberOfFaces : ', totalNumberOfFaces)
    print('numberOfFacesWith3Vertices : ', numberOfFacesWith3Vertices)
    print('numberOfFacesWith4Vertices : ', numberOfFacesWith4Vertices)
    print('numberOfFacesWithMorethan4Vertices : ', numberOfFacesWithMorethan4Vertices)
    file.close()

goraudVertexNormalList = []

def createGoraudShadingNormal():
    global faceNormalListList, iarrListList, varrListList, goraudVertexNormalList
    goraudVertexNormalList = []

    # print(len(varrListList))
    # print(len(faceNormalListList))

    for index1 in range(len(varrListList)):
        iarrList = iarrListList[index1]
        varrList = varrListList[index1]
        faceNormalList = faceNormalListList[index1]
        goraudVertexNormal = []
        for index2 in range(len(varrList)):
            faceNormals = []
            for index3 in range(len(iarrList)):
                # print(index3)
                # print(iarrList[index3])
                iarr = iarrList[index3]
                if index2 in iarr:
                    faceNormals.append(faceNormalList[index3])
            npNormals = []
            for normal in faceNormals:
                npNormals.append(normal)
            
            sumNormal = np.array([0,0,0],'float32')
        
            for normal in npNormals:
                sumNormal = sumNormal + normal
                
            sumUnitNormal = sumNormal / np.sqrt(np.dot(sumNormal, sumNormal))
            goraudVertexNormal.append(list(sumUnitNormal))
        # print(goraudVertexNormal)
        goraudVertexNormalList.append(np.array(goraudVertexNormal, 'float32'))

def createVertexAndIndexArrayIndexedList(varrListList, iarrListList, normalListList):
    vnpList = []
    inpList = []
    nnpList = []
    for list in varrListList:
        vnpList.append(np.array(list, 'float32'))
    for list in iarrListList:
        inpList.append(np.array(list))
    for list in normalListList:
        nnpList.append(np.array(list,  'float32'))
    
    # print(vnpList)
    # print(inpList)
    return vnpList, inpList, nnpList

def createVertexAndIndexArrayIndexed(varrList, iarrList):
    varr = np.array(varrList, 'float32')
    iarr = np.array(iarrList)
    return varr, iarr

def draw_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)



def render():
    global gCamAng, gCamHeight, panningPosX, panningPosY, currentZoomLevel, isOrthoEnabled
    global gVertexArrayIndexedList, gIndexArrayList, gNormalArrayList,isAnimateEnabled
    global vertexPointingListList, normalPointingListList, wireframeMode, goraudVertexNormalList, smoothMode
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if wireframeMode:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10000)
    
    if isOrthoEnabled:
        glLoadIdentity()
        glOrtho(-3,3, -3,3, -10000,10000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(0,0, currentZoomLevel)
    glTranslatef(panningPosX, panningPosY, 0)

    glRotatef(gCamHeight, 1, 0, 0)
    glRotatef(36.264, 1, 0, 0)
    glRotatef(gCamAng, 0, 1, 0)
    glRotatef(-45, 0, 1, 0)

    drawFrame()
    drawRectGrid()
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    # # glEnable(GL_NORMALIZE)
    glEnable(GL_RESCALE_NORMAL)

    glPushMatrix()

    lightPos = (3., 4., 5. ,1.)
    lightPos2 = (-3., 0., 0. ,1.)

    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos2)
    
    glPopMatrix()

    lightColor = (1., 1., 1., 1.)
    ambientLightColor = (.1, .1, .1, 1.)
    
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    
    objectColor = (1, 0., 1., 1)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    t = glfw.get_time()

    if not isAnimateEnabled :
        for i in range(len(gVertexArrayIndexedList)):
            if smoothMode:
                draw_glDrawElements_arguments(gVertexArrayIndexedList[i], gIndexArrayList[i], goraudVertexNormalList[i])
            # draw_glDrawElements_arguments(vertexPointingListList[i], gIndexArrayList[i], normalPointingListList[i])
            else:
                draw_glDrawArrays_arguments(vertexPointingListList[i], gIndexArrayList[i], normalPointingListList[i])
    else:
        if len(gVertexArrayIndexedList) != 3:
            glDisable(GL_LIGHTING)
            return
        
        glPushMatrix()
        # I
        glTranslatef(3 * np.sin(t), 0, 0)
        
        # moon drawing
        glPushMatrix()
        # IT
        # I
        glColor3ub(0, 255, 255)
        glScalef(.1, .1, .1)
        if smoothMode:
            draw_glDrawElements_arguments(gVertexArrayIndexedList[0], gIndexArrayList[0], goraudVertexNormalList[0])
        else:
            draw_glDrawArrays_arguments(vertexPointingListList[0], gIndexArrayList[0], normalPointingListList[0])
        

        glPopMatrix()
        # I

        # earth transformation
        glPushMatrix()
        # IT
        # I
        glRotatef(t*(180/np.pi), 0, 0, 1)
        glTranslatef(10, 0, 3)

        glPushMatrix()
        # ITRT
        # IT
        # I
        drawFrame()
        glColor3ub(0, 0, 0)
        # draw_glDrawElements_arguments(gVertexArrayIndexedList[1], gIndexArrayList[1], gNormalArrayList[1])
        
        objectColor = (0.0, 0.0, 1., 1)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

        if smoothMode:
            draw_glDrawElements_arguments(gVertexArrayIndexedList[1], gIndexArrayList[1], goraudVertexNormalList[1])
        else:
            draw_glDrawArrays_arguments(vertexPointingListList[1], gIndexArrayList[1], normalPointingListList[1])
        
        glPopMatrix()
        glPushMatrix()
        # ITRT
        # IT
        # I
        glRotatef(2 * t * (180/np.pi), 1, 0, 0)
        glTranslatef(2, 2, 2)
        glScalef(.5, .5, .5)
        drawFrame()
        glColor3ub(255, 255, 255)
        # draw_glDrawElements_arguments(gVertexArrayIndexedList[2], gIndexArrayList[2], gNormalArrayList[2])
        objectColor = (0.5, 0.5, 0.5, 1)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
        if smoothMode:
            draw_glDrawElements_arguments(gVertexArrayIndexedList[2], gIndexArrayList[2], goraudVertexNormalList[2])
        else:
            draw_glDrawArrays_arguments(vertexPointingListList[2], gIndexArrayList[2], normalPointingListList[2])
        
        
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()

        # for i in range(len(gVertexArrayIndexedList)):
        #     draw_glDrawElements_arguments(gVertexArrayIndexedList[i], gIndexArrayList[i])
    glDisable(GL_LIGHTING)

def draw_glDrawElements_arguments(varr, iarr, narr):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 3*narr.itemsize, narr)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    # glDrawArrays(GL_TRIANGLES, 0, int(varr.size/3))
    # glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def draw_glDrawArrays_arguments(varr, iarr, narr):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 3*narr.itemsize, narr)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 3))
    
def key_callback(window, key, scancode, action, mods):
    global isOrthoEnabled, isAnimateEnabled, wireframeMode, smoothMode
    if key==glfw.KEY_V and action==glfw.PRESS:
        isOrthoEnabled = not isOrthoEnabled
    elif key==glfw.KEY_H and action==glfw.PRESS:
        isAnimateEnabled = not isAnimateEnabled
        if isAnimateEnabled:
            drop_callback(window, ['obj/customobj.obj'])
    elif key==glfw.KEY_Z and action==glfw.PRESS:
        wireframeMode = not wireframeMode
    elif key==glfw.KEY_S and action==glfw.PRESS:
        smoothMode = not smoothMode
        
        
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
    window = glfw.create_window(1280,1280,"ClassAssignment2", None,None)
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
