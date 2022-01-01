import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib
from matplotlib.animation import FuncAnimation

class Car:
    def __init__(self, length, position, velocity, gap):
        self.length = length        # 
        self.position = position    #
        self.velocity = velocity    # for each time step, car can move m segments up to M. (this is its velocity)
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

        # update gap between cars
        car.gap = Cars[Cars.index(car)+1].position - (car.position+1)
        
    return


def display_stats():
    for car in Cars[:-1]:
        print(f"Car Stats: \n Position: {car.position} \n Velocity: {car.velocity} \n Gap: {car.gap}")
    print(f"End Wall: Position: {Cars[-1].position}")

def measure_density(x0, dx, t0):

    cars_in_interval = list(filter(lambda car: (x0-dx <= car.position <= x0+dx), Cars))
    density = len(cars_in_interval) / (2 * dx)
    print(f"density @ x0, t0: {(x0,t0)}: {density}")

def measure_flux(x0, t0, dt):

    cars_in_interval = list(filter(lambda car: ((car.position - car.velocity*dt) < x0 < (car.position + car.velocity*dt)), Cars))
    flux = len(cars_in_interval) / 2*dt
    print(f"flux @ x0,t0: {(x0,t0)}: {flux}")


    
if __name__ == "__main__":

    Cars = []

    L = int(input("Input Car Length: "))
    N = int(input("Input Number of Cars: "))
    dt = float(input("Enter timestep: "))
    M = int(input("Enter Max Segments in given timestep: "))
    EW = int(input("Enter End Wall Distance: "))

    #    max_velocity = float(M * L) / dt
    max_velocity = M

    initialize_cars(L, N)

    # subplots() function you can draw
    # multiple plots in one figure
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(120, 10))
    # set limit for x and y axis
    axes.set_ylim(-100, EW+10)
    axes.set_xlim(0, 500)

    # style for plotting line
    plt.style.use("ggplot")

    # create 5 list to get store element
    # after every iteration
    x1, y1 = [], [[] for _ in range(N)]
    
    def animate(i):
        print("____________________________________")

        x1.append(i)

        for o in range(len(y1)):
            y1[o].append(Cars[o].position)
                
        display_stats()
        update_cars(.3, dt)
        measure_density(x0=25, dx=10, t0=i)
        measure_flux(x0=25, t0=i, dt=3)
        
        for car in y1:
            axes.plot(x1, car)


    # set ani variable to call the
    # function recursively
    anim = FuncAnimation(fig, animate,frames=100, interval=1, repeat=False)
    plt.show()

