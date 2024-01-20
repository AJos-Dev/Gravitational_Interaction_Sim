import pygame
import pygame.gfxdraw
import math

pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Interacting Gravitational Objects")

class object():
    def __init__(self, mass, radius, initial_x, initial_y, initial_vel_x, initial_vel_y):
        self.mass = mass
        self.radius = radius
        self.x = initial_x
        self.y = initial_y
        self.vel_x = initial_vel_x
        self.vel_y = initial_vel_y

dt = 1/60

#a = object(50000, 10, 500, 500, 0, 0)
#b = object(10000, 10, 600, 500, 0, 20)

a = object(50000, 20, 500, 500, 0, 0)
b = object(10000, 10, 600, 600, -10, 10)
pixel_coords_a = []
pixel_coords_b = []

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
        b_inst_acc_y = - b_inst_acc_y`  `
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

    pygame.draw.circle(win, (255, 255, 255), (a.x, a.y), a.radius)
    pygame.draw.circle(win, (255, 255, 255), (b.x, b.y), b.radius)
    
    for i in range(len(pixel_coords_a)):
        pygame.gfxdraw.pixel(win, round(pixel_coords_a[i][0]), round(pixel_coords_a[i][1]), (255, 0, 0))
        pygame.gfxdraw.pixel(win, round(pixel_coords_b[i][0]), round(pixel_coords_b[i][1]), (0, 255, 0))
    #Dots instead of lines help visualise Keplers Second law
    pygame.display.update()
    clock.tick(480)

#WORKS!
    
#Old code for nostalgia
'''
    for curr_obj in range(len_objects):
        next_obj = (curr_obj+1)%len_objects
        
        if objects[next_obj].x - objects[curr_obj].x == 0:
            s_x = 0
        else:
            s_x = ((objects[next_obj].mass) * dt**2 )/abs(objects[next_obj].x - objects[curr_obj].x) * (objects[next_obj].x - objects[curr_obj].x) 
        objects[curr_obj].x += round(s_x)
        if objects[next_obj].y - objects[curr_obj].y == 0:
            s_y = 0
        else:
            s_y =((objects[next_obj].mass) * dt**2 )/abs(objects[next_obj].y - objects[curr_obj].y) * (objects[next_obj].y - objects[curr_obj].y) 
            s_y += objects[curr_obj].inst_vel * dt
        objects[curr_obj].y += round(s_y)
        if objects[next_obj].x - objects[curr_obj].x == 0: 
            instantaneous_acceleration_x = 0
        else:
            instantaneous_acceleration_x =  objects[next_obj].mass /(abs(objects[next_obj].x - objects[curr_obj].x) * (objects[next_obj].x - objects[curr_obj].x))
        if objects[next_obj].y - objects[curr_obj].y == 0:
            instantaneous_acceleration_y = 0
        else:
            instantaneous_acceleration_y =  objects[next_obj].mass /(abs(objects[next_obj].y - objects[curr_obj].y) * (objects[next_obj].y - objects[curr_obj].y))
        objects[curr_obj].vel_x += instantaneous_acceleration_x * dt
        objects[curr_obj].vel_y += instantaneous_acceleration_y * dt
        objects[curr_obj].x += objects[curr_obj].vel_x * dt
        objects[curr_obj].y += objects[curr_obj].vel_y * dt
        pygame.draw.circle(win, (255, 255, 255), (objects[curr_obj].x, objects[curr_obj].y), objects[curr_obj].radius)
'''