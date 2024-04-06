""" Visualization function for the membrane

"""
import cv2
import io
import imageio
import matplotlib.pyplot as plt
import numpy as np

from pygifsicle import optimize
from tqdm import tqdm
from typing import Tuple

from membrane import CircularMembrane, RectangularMembrane

def animate_membrane(
    filename:str,
    membrane:CircularMembrane|RectangularMembrane,
    N:int = 400,
    video_size:Tuple[int, int] = (800,600),
    video_dpi:int = 128,
    framerate:int = 30,
    runtime:float = 5, #s
    periods:int = 2
):
    """ Animate a membrane.
    """
    # Use the gif functionality if the file extension ends with .gif
    gif = filename.endswith(".gif")
    # Check if the membrane is circular or rectangular
    circular = isinstance(membrane, CircularMembrane)

    if circular:
        a = membrane.get_radius()
        r = np.linspace(0, a, N)
        theta = np.linspace(0, 2*np.pi, N)
        R, Theta = np.meshgrid(r, theta)
    else:
        a, b = membrane.get_dimensions()
        X = np.linspace(0, a, N)
        Y = np.linspace(0, b, N)
        X, Y = np.meshgrid(X, Y)
    
    amp = membrane.get_amplitude()
    tf = membrane.get_period()
    T = np.linspace(0, tf*periods, int(framerate*runtime))

    if gif:
        frames = []
    else:
        video_writer = cv2.VideoWriter(
            f"anim/{filename}", cv2.VideoWriter_fourcc(*"H264"), framerate,
            video_size
        )
    # Compute the figure size
    inches_x = video_size[0] / video_dpi
    inches_y = video_size[1] / video_dpi

    for t in tqdm(T):
        if circular:
            Z = membrane.evaluate(R, Theta, t)
            # Convert to cartesian coordinates
            X, Y = R*np.cos(Theta), R*np.sin(Theta)
        else:
            Z = membrane.evaluate(X, Y, t)

        fig = plt.figure(figsize=[inches_x, inches_y])
        ax = fig.add_subplot(projection='3d')

        ax.plot_surface(X, Y, Z, cmap='plasma', vmin=-amp*1.1, vmax=amp*1.1)
        ax.set_zlim(-amp*1.1, amp*1.1)
        ax.set_aspect('equal', adjustable='box')
        
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        m, n = membrane.get_wave_numbers()
        plt.title(
            f"{'Circular' if circular else 'Rectangular'} Membrane, ({m},{n}) Mode"
        )

        # Save the figure to a buffer
        io_buf = io.BytesIO()
        fig.savefig(io_buf, format='raw', dpi=video_dpi)

        # Convert buffer to uint8 RGB array
        io_buf.seek(0)
        img_arr = np.frombuffer(io_buf.getvalue(), dtype=np.uint8) \
                    .reshape(video_size[1], video_size[0], -1)
        io_buf.close()

        # Close the plot to prevent it from showing in the notebook
        plt.close()

        if gif:
            # Add the image to the frame list
            frames.append(img_arr)
        else:
            # Convert image data and write
            cv_img = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)
            video_writer.write(cv_img)
    
    if gif:
        # Export and optimize the gif
        imageio.mimsave(
            f"anim/{filename}",
            frames,
            fps=framerate,
            loop=int(2**15-1)
        )
        optimize(f"anim/{filename}")
    else:
        # Release the cv2 video writer
        video_writer.release()

def plot_membrane_peak(
    filename:str,
    membrane:CircularMembrane|RectangularMembrane,
    plot_dpi:int = 400,
    N:int = 400
):
    # Check if the membrane is circular or rectangular
    circular = isinstance(membrane, CircularMembrane)

    if circular:
        a = membrane.get_radius()
        r = np.linspace(0, a, N)
        theta = np.linspace(0, 2*np.pi, N)
        R, Theta = np.meshgrid(r, theta)
    else:
        a, b = membrane.get_dimensions()
        X = np.linspace(0, a, N)
        Y = np.linspace(0, b, N)
        X, Y = np.meshgrid(X, Y)

    amp = membrane.get_amplitude()
    t = membrane.get_period()/4.

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    if circular:
            Z = membrane.evaluate(R, Theta, t)
            # Convert to cartesian coordinates
            X, Y = R*np.cos(Theta), R*np.sin(Theta)
    else:
        Z = membrane.evaluate(X, Y, t)

    ax.plot_surface(X, Y, Z, cmap='plasma', vmin=-amp*1.1, vmax=amp*1.1)
    ax.set_zlim(-amp*1.1, amp*1.1)
    ax.set_aspect('equal', adjustable='box')
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    m, n = membrane.get_wave_numbers()
    plt.title(
        f"{'Circular' if circular else 'Rectangular'} Membrane, ({m},{n}) Mode"
    )

    fig.savefig(f"output/{filename}", dpi=plot_dpi, bbox_inches='tight')