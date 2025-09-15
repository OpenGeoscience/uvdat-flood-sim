import numpy

import matplotlib.pyplot as plt
import matplotlib.animation as ani

from constants import OUTPUTS_FOLDER

def animate(results):
    OUTPUTS_FOLDER.mkdir(parents=True, exist_ok=True)
    n_frames = results.shape[0]
    vmin, vmax = numpy.min(results), numpy.max(results)

    fig, ax = plt.subplots()
    im = ax.imshow(
        results[0],
        cmap='viridis',
        vmin=vmin,
        vmax=vmax,
    )

    def update(i):
        ax.set_title(f'Hour={i + 1}')
        im.set_data(results[i])
        return im

    animation = ani.FuncAnimation(fig, update, n_frames, interval=1000)
    animation.save(
        OUTPUTS_FOLDER / 'animation.gif',
        writer=ani.PillowWriter(fps=2)
    )

    plt.colorbar(im, label='Flood depth (m)')
    plt.show()
