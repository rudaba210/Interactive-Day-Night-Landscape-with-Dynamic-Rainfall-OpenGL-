from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


width, height = 500, 500
rain_drops = []
rain_speed = 4
rain_dx = 0  # Horizontal drift of rain
is_night = False


for _ in range(100):
    x = random.randint(0, width)          # Generate rain drops
    y = random.randint(height, height + 500)
    rain_drops.append([x, y])

def triangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

def rectangle(x, y, w, h):
    triangle(x, y, x + w, y, x + w, y + h)
    triangle(x, y, x + w, y + h, x, y + h)

def hills():
    glColor3f(0.0, 0.6, 0.0)
    hill_base_y = 150
    hill_heights = [220, 180, 200, 170, 210, 190, 180]
    hill_width = 80
    for i in range(len(hill_heights)):
        x1 = i * hill_width
        x2 = x1 + hill_width
        peak_x = (x1 + x2) / 2
        peak_y = hill_heights[i]
        triangle(x1, hill_base_y, x2, hill_base_y, peak_x, peak_y)

def field():
    glColor3f(0.8, 0.6, 0.4)
    rectangle(0, 0, width, 150)

def house():
    glColor3f(1.0, 1.0, 1.0)
    rectangle(150, 150, 200, 150)

    glColor3f(0.0, 0.0, 0.5)
    triangle(130, 300, 370, 300, 250, 420)

    glColor3f(0.5, 0.5, 0.5)
    rectangle(230, 150, 40, 75)

    glColor3f(0.0, 1.0, 1.0)
    rectangle(170, 200, 30, 50)
    rectangle(300, 200, 30, 50)

def rain():
    glColor3f(0.4, 0.7, 1.0)
    glBegin(GL_LINES)
    for drop in rain_drops:
        glVertex2f(drop[0], drop[1])
        glVertex2f(drop[0] + rain_dx, drop[1] - 10)
    glEnd()

def iterate():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def update_rain():
    for drop in rain_drops:
        drop[0] += rain_dx
        drop[1] -= rain_speed
        if drop[1] < 0 or drop[0] < 0 or drop[0] > width:
            drop[0] = random.randint(0, width)
            drop[1] = random.randint(height, height + 300)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    
    if is_night:                            
        glClearColor(0.0, 0.0, 0.2, 1.0)    # Background color
    else:
        glClearColor(0.5, 0.8, 1.0, 1.0)

    hills()
    field()
    house()
    rain()
    glutSwapBuffers()

def animate():
    update_rain()
    glutPostRedisplay()

def keyboard(key, x, y):
    global is_night
    if key == b'n':
        is_night = True
    elif key == b'd':
        is_night = False

def special_keys(key, x, y):
    global rain_dx
    if key == GLUT_KEY_LEFT:
        rain_dx -= 0.5
    elif key == GLUT_KEY_RIGHT:
        rain_dx += 0.5


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"OpenGL House with Rain and Direction Control")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
glutMainLoop()
