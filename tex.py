import sys
import subprocess
import datetime
import os
import tempfile

import matplotlib
matplotlib.use("Agg")

if sys.platform == "win32":
    _orig_popen = subprocess.Popen

    def _hidden_popen(*args, **kwargs):
        kwargs.setdefault("creationflags", subprocess.CREATE_NO_WINDOW)
        return _orig_popen(*args, **kwargs)

    subprocess.Popen = _hidden_popen

import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True

def render_tex(author: str, code: str, i: int) -> str:
    try:
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')

        text = ax.text(0, 0, code, fontsize=18, ha='left', va='bottom')

        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        bbox = text.get_window_extent(renderer=renderer)

        px = 2
        py = 6
        bbox = bbox.expanded((bbox.width+2*px) / bbox.width, (bbox.height+2*py) / bbox.height)

        fig.set_size_inches(bbox.width / fig.dpi,bbox.height / fig.dpi)
        text.set_position((-bbox.x0 / fig.dpi, -bbox.y0 / fig.dpi))

        timestamp = datetime.datetime.now().strftime('%H%M%S')
        png_name = f"{author}_{timestamp}_{i}.png"
        save_path = os.path.join(tempfile.gettempdir(), png_name)

        plt.savefig(save_path, dpi=300, transparent=False, pad_inches=0)
        plt.close(fig)

        return (True, save_path)

    except Exception as e:
        return (False, str(e))