import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib
from matplotlib import style
from matplotlib.animation import FuncAnimation

class Car:
    def __init__(self, length, position, velocity, gap):
        self.length = length        # length of care/each cell
        self.position = position    # distance from origin
        self.velocity = velocity    # for each time step, car can move m segments up to M.
        self.gap = gap              # num of cells between this car and the next

        
def initialize_cars(car_length, num_cars):
    
    for i in range(0, num_cars):
        Cars.append(Car(length=car_length, position=i, velocity=0, gap=0))

    # END WALL
    Cars.append(Car(length=car_length, position=EW, velocity=0, gap=0))

    #set initial gap to end wall
    Cars[-2].gap = Cars[-1].position - Cars[-2].position

    for i in range(0, num_cars):
        print(f"Initial Car {i} Stats: \n Length: {Cars[i].length} \n Position: {Cars[i].position} \n Velocity: {Cars[i].velocity} \n Gap: {Cars[i].gap}")
    print(f"END WALL: Position: {Cars[num_cars].position}")

    return


def update_cars(rand_prob, dt):
    
    for car in (Cars[::-1])[1:]:

        ##############################################
        # 4 RULES OF MOTION
        
        # speedup
        if car.velocity != max_velocity:
            car.velocity += dt

        # dont hit each other
        if car.velocity > car.gap:
            car.velocity = car.gap

        # randomize changing speed of cars bc of environ and such
        if car.velocity != 0:
           if random.random() < rand_prob:
               car.velocity -= random.random()
    
        # move the car to new position
        car.position += car.velocity
        ##############################################
        
        # update gap between cars
        car.gap = Cars[Cars.index(car)+1].position - (car.position+1)
        
    return


def display_stats():
    
    for car in Cars[:-1]:
        print(f"Car Stats: \n Position: {car.position} \n Velocity: {car.velocity} \n Gap: {car.gap}")
    print(f"End Wall: Position: {Cars[-1].position}")

def measure_density(x0, dx, t0):

    cars_in_interval = list(filter(lambda car: (x0-dx <= car.position <= x0+dx), Cars[:-1]))
    density = len(cars_in_interval) / (2 * dx)
    print(f"density @ x0, t0: {(x0,t0)}: {density}")

def measure_flux(x0, t0, dt):

    cars_in_interval = list(filter(lambda car: ((car.position - car.velocity*dt) < x0 < (car.position + car.velocity*dt)), Cars[:-1]))
    flux = len(cars_in_interval) / 2*dt
    print(f"flux @ x0,t0: {(x0,t0)}: {flux}")


    
if __name__ == "__main__":

    L = float(input("Input Car Length: "))
    N = int(input("Input Number of Cars: "))
    dt = float(input("Enter timestep: "))
    M = float(input("Enter Max Velocity: "))
    EW = float(input("Enter End Wall Distance: "))
    max_velocity = float(M * L) / dt

    Cars = []



    initialize_cars(L, N)

    # setup graph
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(120, 10))

    axes.set_xlabel("Time (t)")
    axes.set_ylabel("Position (x)")

    # set limit for x and y axis
    axes.set_ylim(-100, EW+10)
    axes.set_xlim(0, 500)


    # store car position after every time step
    x1, y1 = [0], [[car.position] for car in Cars[:-1]]

    # graph line for each car
    P = [axes.plot(x1, car) for car in y1]

    
    def animate(i):

        ##########
        # add coords of each car to graph respective line
        x1.append(i)

        for o in range(len(y1)):
            y1[o].append(Cars[o].position)
        ##########

        display_stats()
        update_cars(.3, dt)

        ##########
        # update each line of graph
        for L in range(len(P)):
            P[L][0].set_data(x1[:i],y1[L][:i])
        ##########
        
        # sort cars by pos so each can react to the car immediately in front
        Cars.sort(key=lambda x: x.position)

        # math
        measure_density(x0=25, dx=10, t0=i)
        measure_flux(x0=50, t0=i, dt=2.5)

        
    anim = FuncAnimation(fig, animate, frames=int(input("#frames:")), interval=1, repeat=False)
    plt.show()
