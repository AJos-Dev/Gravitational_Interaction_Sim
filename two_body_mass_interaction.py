import pygame
import pygame.gfxdraw
import math

win_x = 1000
win_y = 1000

pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption("Interacting Gravitational Objects")

class object():
    def __init__(self, mass, radius, initial_x, initial_y, initial_vel_x, initial_vel_y):
        self.mass = mass
        self.radius = radius
        self.x = initial_x
        self.y = initial_y
        self.vel_x = initial_vel_x
        self.vel_y = initial_vel_y
    
class masslets():
    def __init__(self, initial_x, initial_y, initial_vel_x, initial_vel_y):
        self.x = initial_x
        self.y = initial_y
        self.vel_x = initial_vel_x
        self.vel_y = initial_vel_y

dt = 1/60

#a = object(50000, 10, 500, 500, 0, 0)
#b = object(10000, 10, 600, 500, 0, 20)

a = object(10000, 10, 400, 500, 0, 0)
b = object(10000, 10, 600, 600, 0, 0)
pixel_coords_a = []
pixel_coords_b = []
masslets_a_list=[]
masslets_b_list=[]


r = 50
for i in range(win_x):
    for j in range(win_y):
        if (((i-a.x)**2 + (j-a.y)**2) <= r**2 and ((i-a.x)**2 + (j-a.y)**2) >= a.radius**2) and (((i-j) %10) + ((i+j) % 10)) == 0:
            masslets_a_list.append(masslets(i, j, a.vel_x, a.vel_y))
        elif (((i-b.x)**2 + (j-b.y)**2) <= r**2 and ((i-b.x)**2 + (j-b.y)**2) >= b.radius**2) and (((i-j) % 10) + ((i+j) % 10)) == 0:
            masslets_b_list.append(masslets(i, j, b.vel_x, b.vel_y))
         

run = True
counter = 0
while run:
    counter +=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = True
                while paused:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            paused = False
                            run = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                paused = False
    win.fill((0, 0, 0))
    #Stuff happens
    if math.sqrt((b.y-a.y)**2 + (b.x-a.x)**2) <= (a.radius + b.radius):
        run = False

    if (b.x-a.x) == 0:
        theta = 3.14159265358979323846264338327950/2
    else:
        theta = math.atan((b.y-a.y)/(b.x-a.x))
    a_inst_acc_x, a_inst_acc_y = (b.mass / ((b.y-a.y)**2 + (b.x-a.x)**2)) * math.cos(theta) , (b.mass / ((b.y-a.y)**2 + (b.x-a.x)**2)) * math.sin(theta)
    b_inst_acc_x, b_inst_acc_y = (a.mass / ((b.y-a.y)**2 + (b.x-a.x)**2)) * math.cos(theta) , (a.mass / ((b.y-a.y)**2 + (b.x-a.x)**2)) * math.sin(theta)

    if (b.x-a.x)>0:
        b_inst_acc_x = - b_inst_acc_x
        b_inst_acc_y = - b_inst_acc_y
    elif (b.x-a.x)<0:
        a_inst_acc_x = -a_inst_acc_x

        a_inst_acc_y = -a_inst_acc_y


    a.vel_x += a_inst_acc_x * dt
    a.vel_y += a_inst_acc_y * dt 
    a.x += a.vel_x * dt
    a.y += a.vel_y * dt
    if counter % 20 == 0:
        pixel_coords_a.append([a.x, a.y])

    b.vel_x += b_inst_acc_x * dt
    b.vel_y += b_inst_acc_y * dt 
    b.x += b.vel_x * dt
    b.y += b.vel_y * dt
    if counter % 20 == 0:
        pixel_coords_b.append([b.x, b.y])

    for i in range(len(masslets_a_list)):
        if (b.x - masslets_a_list[i].x) == 0:
            theta = 3.14159265358979323846264338327950/2
        else:
            theta = math.atan((b.y- masslets_a_list[i].y)/(b.x- masslets_a_list[i].x))
        masslet_a_x_acceleration, masslet_a_y_acceleration = (b.mass / ((b.y-masslets_a_list[i].y)**2 + (b.x-masslets_a_list[i].x)**2)) * math.cos(theta), (b.mass / ((b.y-masslets_a_list[i].y)**2 + (b.x-masslets_a_list[i].x)**2)) * math.sin(theta)
        masslets_a_list[i].vel_x += masslet_a_x_acceleration * dt
        masslets_a_list[i].vel_y += masslet_a_y_acceleration * dt
        masslets_a_list[i].x += masslets_a_list[i].vel_x * dt
        masslets_a_list[i].y += masslets_a_list[i].vel_y * dt
        #do the same for masslet_b_list[i] here:

    for i in masslets_a_list:
        pygame.draw.circle(win, (255, 0, 0), (i.x, i.y), 1)
    for i in masslets_b_list:
        pygame.draw.circle(win, (0, 255, 0), (i.x, i.y), 1)

    pygame.draw.circle(win, (255, 255, 255), (a.x, a.y), a.radius)
    pygame.draw.circle(win, (255, 255, 255), (b.x, b.y), b.radius)
    
    #for i in range(len(pixel_coords_a)):
    #    pygame.gfxdraw.pixel(win, round(pixel_coords_a[i][0]), round(pixel_coords_a[i][1]), (255, 0, 0))
    #    pygame.gfxdraw.pixel(win, round(pixel_coords_b[i][0]), round(pixel_coords_b[i][1]), (0, 255, 0))
    #Dots instead of lines help visualise Keplers Second law
    pygame.display.update()
    clock.tick(240)