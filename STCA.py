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
    Cars.append(Car(length=car_length, position=50, velocity=0, gap=0))

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
            car.velocity += 1

        # dont hit each other
        if car.velocity > car.gap:
            car.velocity = car.gap

        # randomize changing speed of cars bc of environ and such
        if car.velocity != 0:
           if random.random() < rand_prob:
               car.velocity -= 1
            
        # move the car to new position
        car.position += car.velocity

        # update gap between cars
        car_ahead = Cars[Cars.index(car) + 1]
        car.gap = car_ahead.position - car.position
        
    return
    
def display_stats():
    for car in Cars[:-1]:
        print(f"Car Stats: \n Position: {car.position} \n Velocity: {car.velocity} \n Gap: {car.gap}")

    print(f"End Wall: Position: {Cars[-1].position}")
    
    return
         

if __name__ == "__main__":

    Cars = []

    L = int(input("Input Car Length: "))
    N = int(input("Input Number of Cars: "))
    dt = float(input("Enter timestep: "))
    M = int(input("Enter Max Segments in given timestep: "))

    max_velocity = float(M * L) / dt

    initialize_cars(L, N)

    T = int(input("Enter Number of timesteps: "))

    # subplots() function you can draw
    # multiple plots in one figure
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(100, 10))
    # set limit for x and y axis
    axes.set_ylim(0, 60)
    axes.set_xlim(0, 20)

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
        update_cars(0, dt)

        for car in y1:
            axes.plot(x1, car, color="red")


    # set ani variable to call the
    # function recursively
    anim = FuncAnimation(fig, animate)
    plt.show()

