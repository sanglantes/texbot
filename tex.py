import datetime
import os
import tempfile

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox

plt.rcParams['text.usetex'] = True

def render_tex(author: str, code: str, i: int):
    try:
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')

        text = ax.text(
            0, 0,
            code,
            fontsize=12,
            ha='left',
            va='bottom',
            wrap=True
        )

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        bbox = text.get_window_extent(renderer=renderer)
        bbox = bbox.transformed(fig.dpi_scale_trans.inverted())

        pad = 5 / fig.dpi

        bbox = Bbox.from_extents(
            bbox.x0 - pad,
            bbox.y0 - pad,
            bbox.x1 + pad,
            bbox.y1 + pad
        )

        timestamp = datetime.datetime.now().strftime('%H%M%S')
        png_name = f"{author}_{timestamp}_{i}.png"
        save_path = os.path.join(tempfile.gettempdir(), png_name)

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches=bbox,
            pad_inches=0
        )
        plt.close(fig)

        return (True, save_path)

    except Exception as e:
        return (False, str(e))
