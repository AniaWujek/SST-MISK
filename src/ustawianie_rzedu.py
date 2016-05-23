#!/usr/bin/env python3
""" Test for wrep API """
from wrep import Simulation, Robot, vrep
import time
import sys
import math

if len(sys.argv) < 5:
	print("3 args requiered: map width, map height, robot count, robot number")
	quit()


#tu sobie liczymy, jak na poczatku powinny byc rozstawione roboty
# ---------------------------
# |                         |
# |                         |
# |                         |
# |                         |
# |          punkt          |
# |          (0,0)          | map_height
# |                         |
# |                         |
# |              max_dist   |
# |               |   |     |
# |               o   o   o |
# ---------------------------
          #map_width

#szerokosc mapy, dla labirynt_do_pokonywania_przeszkod3 to = 45          
map_width = int(sys.argv[1])

#wysokosc mapy, dla labirynt_do_pokonywania_przeszkod3 to = 45       
map_height = int(sys.argv[2])

#ile robotow, dla labirynt_do_pokonywania_przeszkod3 to = 2      
robot_count = int(sys.argv[3])

#numerek naszego robota
robot_number = int(sys.argv[4])

#zasieg radiowy
max_range = 1

#max. odleglosc, na jaka pozwalamy im odjechac od siebie
max_dist = 2*max_range*0.7

#szerokosc calego szerego robotow
row_width = (robot_count + 0.5)*max_dist

#startowe pozycje, ktore maja zajac
start_positions = []
y = -map_height / 2.0 + 0.5*max_dist
x = map_width / 2.0 - 0.5*max_dist
for i in range(robot_count):
	start_positions.append((x,y))
	x = x - max_dist


#tworzymy robota
sim = Simulation(port_number=19999)

robot = Robot(sim, "Pioneer_p3dx#{nn}".format(nn=robot_number))

for i in range(1, 17):
    robot.add_sensor(
        name="Pioneer_p3dx_ultrasonicSensor{n}#{nn}".format(n=i,nn=robot_number),
        sensor_type="proximity",
        key="proximity-{n}".format(n=i))

robot.add_motor(
    name="Pioneer_p3dx_leftMotor#{nn}".format(nn=robot_number),
    key="left")

robot.add_motor(
    name="Pioneer_p3dx_rightMotor#{nn}".format(nn=robot_number),
    key="right")

robot.add_sensor(
    name=None,
    sensor_type="position",
    key="position",
    component=robot)
    
robot.add_sensor(
    name=None,
    sensor_type="orientation",
    key="orientation",
    component=robot)
    
#zeby czujniki zaczely dzialac poprawnie
robot.sensors["orientation"].read()
robot.sensors["position"].read()
time.sleep(0.5)
    
#zadana pozycja i aktualna pozycja
desired_p = start_positions[robot_number]
current_p = (robot.sensors["position"].read().pos[0], robot.sensors["position"].read().pos[1])

print("I want to robot be in position:")
print(desired_p)
print("And orientation:")
print(math.pi/2.0)

#zadana orientacja i aktualna orientacja
#uwaga, vrep jakos dziwnie to liczy - w vrepie orientacja jest w stopniach, a w pythonie
#odbieramy ja w radianach
#poza tym zrobione jest tak domyslnie:

#            0
#           
#     1/4 pi    -1/4 pi
#   
#1/2 pi              -1/2 pi
#
#     3/4 pi    -3/4 pi
#   
#           pi
# co jest dla mnie jakos malo intuicyjne, bo w tym przypadku pi = -pi
# dlatego zmieniam na takie:
#            0
#           
#     1/4 pi     7/4 pi
#   
#1/2 pi              3/2 pi
#
#     3/4 pi    5/4 pi
#   
#           pi
# czyli tak, że 0 = 2*pi
# jesli to glupie i uznacie, ze jednak vrep jest madrzejszy, to nie wahajcie sie tego zmienic :)




#interesuje nas 3 skladowa orientacji, bo nie bedziemy robic fikolkow ani beczek
current_o = robot.sensors["orientation"].read().ori[2]
if current_o < 0:
	current_o = math.pi + (math.pi + current_o)

#jak dokladnie ma sie ustawic
precision_p = 0.1
precision_o = 0.05



v_max_o = 5

	

#max. predkosc podczas obrotu
v_max_p = 2

#aktualna roznica miedzy pozycjami zadana a aktualna
d_p = (desired_p[0] - current_p[0],desired_p[1] - current_p[1])
desired_o = math.atan2(-d_p[1], -d_p[0])+math.pi
d_o = desired_o - current_o

while abs(d_p[0]) > precision_p or abs(d_p[1]) > precision_p:
	k_p = math.sqrt(math.pow(d_p[0], 2) + math.pow(d_p[1], 2))
	v_p = min(v_max_p, k_p*v_max_p)
	desired_o = math.atan2(-d_p[1], -d_p[0])+math.pi
	k_o = min([abs(d_o), 2*math.pi-abs(d_o)])/(2*math.pi)
	v_o = k_o*v_max_o
	if d_o < -math.pi:
		v_right = -v_o 
		v_left = v_o
	elif d_o < 0:
		v_right = v_o 
		v_left = -v_o
	elif d_o < math.pi:
		v_right = -v_o 
		v_left = v_o
	else:
		v_right = v_o 
		v_left = -v_o
		
	robot.motors["left"].velocity = v_right+v_p
	robot.motors["right"].velocity = v_left+v_p
	
	#taki okres probkowania dziala
	time.sleep(0.1)
	current_o = robot.sensors["orientation"].read().ori[2]
	if current_o < 0:
		current_o = math.pi + (math.pi + current_o)
	d_o = desired_o - current_o
	current_p = (robot.sensors["position"].read().pos[0], robot.sensors["position"].read().pos[1])
	d_p = (desired_p[0] - current_p[0],desired_p[1] - current_p[1])

#stop robot
robot.motors["left"].velocity = 0.0
robot.motors["right"].velocity = 0.0

#jak sie nie da tutaj sleepa to sie silniki nie zatrzymuja
time.sleep(0.5)
	



# ***************************************
# ustawienie tylko orientacji
# ***************************************

# skoro mapa jest prostokatna i chcemy jechac takim rzedem, to kierunek mozna hardkodowac
desired_o = math.pi/2.0;

#max. predkosc podczas obrotu
v_max = 5

#aktualna roznica miedzy orientacjami zadana a aktualna
d_o = desired_o - current_o

while abs(d_o) > precision_o:
	#taki sobie regulator P - dziala
	k = min([abs(d_o), 2*math.pi-abs(d_o)])/(2*math.pi)
	#print(d_o)
	v = k*v_max
	#ify stad, ze chcemy obracac sie krotsza droga
	# pewnie da sie to zrobic ladniej, ale tak dziala
	if d_o < -math.pi:
		v_right = -v 
		v_left = v
	elif d_o < 0:
		v_right = v 
		v_left = -v
	elif d_o < math.pi:
		v_right = -v 
		v_left = v
	else:
		v_right = v 
		v_left = -v
		
	robot.motors["left"].velocity = v_right
	robot.motors["right"].velocity = v_left
	
	#taki okres probkowania dziala
	time.sleep(0.1)
	current_o = robot.sensors["orientation"].read().ori[2]
	if current_o < 0:
		current_o = math.pi + (math.pi + current_o)
	d_o = desired_o - current_o

#stop robot
robot.motors["left"].velocity = 0.0
robot.motors["right"].velocity = 0.0

#jak sie nie da tutaj sleepa to sie silniki nie zatrzymuja
time.sleep(0.5)

current_o = robot.sensors["orientation"].read().ori[2]
if current_o < 0:
	current_o = math.pi + (math.pi + current_o)
current_p = (robot.sensors["position"].read().pos[0], robot.sensors["position"].read().pos[1])
print("*******************")
print("Robot is in position:")
print(desired_p)
print("And orientation:")
print(current_o)



sim.close()
