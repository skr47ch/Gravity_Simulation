import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from tkinter import Tk, colorchooser

def calculate_gravitational_field(mass_position, mass, x, y):
    dx = x - mass_position[0]
    dy = y - mass_position[1]
    r = np.sqrt(dx**2 + dy**2)
    r_cubed = r**3
    with np.errstate(divide='ignore', invalid='ignore'):  # Suppress divide by zero warning
        fx = np.where(r > 0, -mass * dx / r_cubed, 0)
        fy = np.where(r > 0, -mass * dy / r_cubed, 0)
    return fx, fy

def plot_gravitational_field_lines(mass_position, mass, object_size, grid_density, object_color, ax):
    x = np.linspace(-10, 10, grid_density)
    y = np.linspace(-10, 10, grid_density)
    X, Y = np.meshgrid(x, y)

    fx, fy = calculate_gravitational_field(mass_position, mass, X, Y)

    ax.clear()
    ax.plot(X, Y, 'k-', linewidth=0.5)  # Plotting the grid lines

    scaled_fx = fx * 0.2  # Scaling factor to control the movement of grid lines
    scaled_fy = fy * 0.2

    # Updating the grid points based on gravitational field
    updated_x = X + scaled_fx
    updated_y = Y + scaled_fy

    # ax.plot(updated_x, updated_y, 'k-', linewidth=0.5)  # Plotting the updated grid lines
    ax.plot(updated_x.T, updated_y.T, 'k-', linewidth=0.5)  # Plotting the updated horizontal grid lines

    ax.plot(mass_position[0], mass_position[1], 'o', markersize=object_size, color=object_color)  # Adjusting marker size and color
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Gravitational Field Lines')

    plt.draw()

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.5)  # Adjust the subplot to make space for widgets
plt.ion()  # Enable interactive mode

mass_position = [0, 0]
mass = 1.0  # Initial mass value
object_size = 5.0  # Initial object size
grid_density = 20  # Initial grid density
object_color = 'red'  # Initial object color

plot_gravitational_field_lines(mass_position, mass, object_size, grid_density, object_color, ax)

def update_mass(val):
    global mass
    mass = mass_slider.val
    plot_gravitational_field_lines(mass_position, mass, object_size, grid_density, object_color, ax)

def update_object_size(val):
    global object_size
    object_size = object_size_slider.val
    plot_gravitational_field_lines(mass_position, mass, object_size, grid_density, object_color, ax)

def update_grid_density(val):
    global grid_density
    grid_density = int(grid_density_slider.val)
    plot_gravitational_field_lines(mass_position, mass, object_size, grid_density, object_color, ax)

def select_object_color(event):
    global object_color
    color = colorchooser.askcolor(title='Select Object Color', initialcolor=object_color)
    if color[0] is not None:
        object_color = color[1]
        plot_gravitational_field_lines(mass_position, mass, object_size, grid_density, object_color, ax)

mass_slider_ax = plt.axes([0.25, 0.4, 0.65, 0.03])
mass_slider = Slider(mass_slider_ax, 'Mass', 0.1, 5.0, valinit=mass)
mass_slider.on_changed(update_mass)

object_size_slider_ax = plt.axes([0.25, 0.35, 0.65, 0.03])
object_size_slider = Slider(object_size_slider_ax, 'Object Size', 1.0, 10.0, valinit=object_size)
object_size_slider.on_changed(update_object_size)

grid_density_slider_ax = plt.axes([0.25, 0.3, 0.65, 0.03])
grid_density_slider = Slider(grid_density_slider_ax, 'Grid Density', 10, 50, valinit=grid_density, valstep=1)
grid_density_slider.on_changed(update_grid_density)

color_button_ax = plt.axes([0.25, 0.25, 0.15, 0.05])
color_button = Button(color_button_ax, 'Object Color')
color_button.on_clicked(select_object_color)

def on_button_press(event):
    if event.inaxes == ax:
        fig.canvas.toolbar.pan()

def on_button_release(event):
    if event.inaxes == ax:
        fig.canvas.toolbar.pan()

def on_mouse_move(event):
    if event.inaxes == ax and event.button == 1:
        mass_position[0] = event.xdata
        mass_position[1] = event.ydata
        plot_gravitational_field_lines(mass_position, mass, object_size, grid_density, object_color, ax)

fig.canvas.mpl_connect('button_press_event', on_button_press)
fig.canvas.mpl_connect('button_release_event', on_button_release)
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

plt.show()  # Display the plot

while plt.fignum_exists(fig.number):
    plt.pause(0.1)
