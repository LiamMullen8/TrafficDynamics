import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")

    return


def update_cars(rand_prob, dt):
    
    for car in (Cars[::-1])[1:]:

        ##############################################
        # RULES OF MOTION
        
        # speedup
        if car.velocity != max_velocity:
            car.velocity += dt

        # randomize changing speed of cars bc of environ and such
        if car.velocity != 0:
           if random.random() < rand_prob:
               car.velocity -= dt
           else:
               car.velocity += dt

        # follow speed limit
        if car.velocity > max_velocity:
            car.velocity = max_velocity

        # dont hit each other
        if car.velocity > car.gap:
            car.velocity = car.gap

        # move the car to new position
        car.position += car.velocity
        ##############################################

        # update gap between cars
        car.gap = Cars[Cars.index(car)+1].position - (car.position + L)
        
    return


def display_stats():
    
    for car in Cars[:-1]:
        print(f"Car Stats: \n Position: {car.position} \n Velocity: {car.velocity} \n Gap: {car.gap}")
    print(f"End Wall: Position: {Cars[-1].position}\n")

def measure_density(x0, dx, t0):

    cars_in_interval = list(filter(lambda car: (x0-dx <= car.position <= x0+dx), Cars[:-1]))
    density = float(len(cars_in_interval)) / (2.0 * dx)
    print(f"{t0}: {cars_in_interval} \n density @ x0, t0: {(x0,t0)}: {density}")
    return density

def measure_flux(x0, t0, dt):

    cars_in_interval = list(filter(lambda car: ((car.position - car.velocity*dt) < x0 < (car.position + car.velocity*dt)), Cars[:-1]))
    flux = float(len(cars_in_interval)) / (2.0 * dt)
    print(f"flux @ x0,t0: {(x0,t0)}: {flux}")
    return flux


    
if __name__ == "__main__":

    L = float(input("Input Car Length: "))
    N = int(input("Input Number of Cars: "))
    dt = float(input("Enter timestep: "))
    M = float(input("Enter Max Velocity: "))
    EW = float(input("Enter End Wall Distance: "))
    D_range = (int(input("Enter x0 and dx for Density: ")), float(input("")))
    F_range = (int(input("Enter x0 and dt for Flux: ")), float(input("")))
    f = int(input("#frames:"))
    
    max_velocity = M #float(M * L) / dt

    Cars = []


    initialize_cars(L, N)


    ###################################################################################
    # # setup graph # #
    
    fig, (flux_ax, dens_ax, car_ax) = plt.subplots(nrows=3, ncols=1, figsize=(120, 10))

    car_ax.set_title("Car Positions")
    car_ax.set_xlabel("Time (t)")
    car_ax.set_ylabel("Position (x)")

    # set limit for x and y axis
    #car_ax.set_ylim(-EW / 2, EW+10)
    car_ax.set_xlim(0, f)

    # store car position after every time step
    x1, y1 = [0], [[car.position] for car in Cars[:-1]]

    # graph line for each car
    car_lines = [car_ax.plot(x1, car) for car in y1]


    # Working range for Density 
    car_ax.fill_between(np.arange(0,f+1), D_range[0]-D_range[1], D_range[0]+D_range[1], alpha=0.2, color='b')

    # Working range for flux
    # car_ax.fill_between(np.arange(0,f+1), where=D_range[0]-D_range[1], D_range[0]+D_range[1], alpha=0.2, color='b')
    
    Dens = dens_ax.plot([],[], lw=2, color='b')
    Dens_y = []
    
    dens_ax.set_xlim(0, f)
    dens_ax.set_xlabel("Time (t)")
    dens_ax.set_ylabel("Density (p rho)")
    dens_ax.set_title(f"Density at position x0={D_range[0]}, dx={D_range[1]}")

    Flux = flux_ax.plot([],[], lw=2, color='g')
    Flux_y = []

    flux_ax.set_xlim(0, f)
    flux_ax.set_xlabel("Time (t)")
    flux_ax.set_ylabel("Flux (J)")
    flux_ax.set_title(f"Flux at position x0={F_range[0]}, dt={F_range[1]}")
    ####################################################################################
    
    def animate(i):
        
        update_cars(.5, dt)
        #display_stats()

        ##########
        # add coords of each car to graph respective line
        x1.append(i*dt)

        for o in range(len(y1)):
            y1[o].append(Cars[o].position)
        ##########


        ##########
        # update each line of graph
        for L in range(len(car_lines)):
            car_lines[L][0].set_data(x1[:i],y1[L][:i])
        ##########

        # sort cars by pos so each can react to the car immediately in front
        #Cars[:-1] = sorted(Cars[:-1], key=lambda x: x.position)


        # math
        density = measure_density(x0=D_range[0], dx=D_range[1], t0=i*dt)
        #Dens_x.append(dt)
        Dens_y.append(density)
        
        flux = measure_flux(x0=F_range[0], t0=i*dt, dt=F_range[1])
        #Flux_x.append(dt)
        Flux_y.append(flux)

        Dens[0].set_data(x1[:i], Dens_y[:i])
        Flux[0].set_data(x1[:i], Flux_y[:i])
        
        car_ax.set_ylim(min(y1[0])-10, EW+10)     
        dens_ax.set_ylim(0, max(Dens_y)+.1)     
        flux_ax.set_ylim(0, max(Flux_y)+.1)     
        
    # animation driver    
    anim = FuncAnimation(fig, animate, frames=int(f//dt), interval=1, repeat=False)
    
    # save animation
    writervideo = animation.FFMpegWriter(fps=60) 
    anim.save('Noncolliding.mp4', writer=writervideo)
    plt.show()
