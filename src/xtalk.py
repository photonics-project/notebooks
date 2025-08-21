# ---
# jupyter:
#   kernelspec:
#     name: python3
#     display_name: Python 3
#     language: python
# ---


# %%
# %matplotlib widget
import io
import itertools

import ipyvuetify as v
import ipywidgets as widgets
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.integrate

from controls import (
    MyFloatSlider,
)


parameters = {
    'data': None,
    'pixel_pitch': 12,
    'sigma': 5,
}


class Figure():
    def __init__(self):
        (fig, ax) = plt.subplots()

        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = True
        fig.canvas.toolbar_position = 'right'

        self.fig = fig
        self.ax = ax

        self.update()

        self.fig.tight_layout()

    @property
    def canvas(self):
        return self.fig.canvas

    def update(self):
        self.plot()

        self.ax.set_xlabel('Spatial Frequency (lp/mm)')
        self.ax.set_ylabel('MTF')

        self.ax.grid(True)
        self.ax.legend(loc='lower left')

        self.fig.canvas.draw_idle()

    def plot(self):
        data = parameters['data']
        pixel_pitch = parameters['pixel_pitch']
        sigma = parameters['sigma']

        frequency = np.linspace(0, 1/pixel_pitch, 20)

        self.ax.clear()

        self.ax.axvline(1000/pixel_pitch/2, color='black', linestyle='dashed')

        pixel_mtf = np.sinc(frequency*pixel_pitch)
        diffusion_mtf = np.abs(np.exp(-2*np.pi**2*frequency**2*sigma**2))
        self.ax.plot(frequency*1000, pixel_mtf, color='black', label='Ideal')
        self.ax.plot(frequency*1000, diffusion_mtf, color='blue', label='Diffusion')
        self.ax.plot(frequency*1000, pixel_mtf*diffusion_mtf, color='green', label='Fit')

        if data is not None:
            self.ax.plot(data['frequency'], data['mtf'], '.', markersize=8, color='red', label='Data')

        self.ax.set_xlim(0, 1000/pixel_pitch)


class Figure2():
    def __init__(self):
        (fig, ax) = plt.subplots()

        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = True
        fig.canvas.toolbar_position = 'right'

        self.fig = fig
        self.ax = ax

        self.update()

        self.fig.tight_layout()

    @property
    def canvas(self):
        return self.fig.canvas

    def update(self):
        self.plot()

        self.fig.canvas.draw_idle()

    def plot(self):
        Npixels = 5
        pixel_pitch = parameters['pixel_pitch']
        sigma = parameters['sigma']

        yi = xi = np.linspace(-Npixels/2*pixel_pitch, +Npixels/2*pixel_pitch, Npixels+1)
        xlim = np.array(list(itertools.pairwise(xi)))
        ylim = np.array(list(itertools.pairwise(yi)))
        bbox = np.array(list(itertools.product(xlim, ylim)))
        bbox = np.transpose(bbox, axes=(0, 2, 1))

        integrals = np.zeros(Npixels**2)

        self.ax.clear()

        for (idx, box) in enumerate(bbox):
            xy = (box[0, 0], box[0, 1])
            width = box[1, 0] - box[0, 0]
            height = box[1, 1] - box[0, 1]
            [cx, cy] = (box[0] + box[1])/2

            integrals[idx] = scipy.integrate.dblquad(lambda y, x: 1/(2*np.pi*sigma**2)*np.exp(-1/2*(x**2+y**2)/sigma**2), *box.T.flatten())[0]

            self.ax.add_patch(mpl.patches.Rectangle(xy, width, height, edgecolor='black', facecolor='white'))
            self.ax.annotate(f'{integrals[idx]:.2g}', (cx, cy), ha='center', va='center')

        self.ax.set_axis_off()
        self.ax.set_aspect('equal')
        self.ax.set_xlim(xi[0], xi[-1])
        self.ax.set_ylim(yi[0], yi[-1])


plt.ioff()

figure = Figure()
figure2 = Figure2()


uploader = widgets.FileUpload(
    accept='.csv',
    multiple=False,
)

pixel_pitch = MyFloatSlider(
    label='Pixel Pitch (µm)',
    value=parameters['pixel_pitch'],
    min=1,
    max=100,
    step=1,
    )

sigma = MyFloatSlider(
    label='Diffusion Sigma (µm)',
    value=parameters['sigma'],
    min=0,
    max=20,
    step=0.1,
    )


def upload(change):
    df = pd.read_csv(io.BytesIO(change.new[0]['content'].tobytes()))
    parameters['data'] = df
    parameters.update({'fnumber': change.new})
    figure.update()
    figure2.update()


def update_pixel_pitch(change):
    parameters.update({'pixel_pitch': change.new})
    figure.update()
    figure2.update()


def update_sigma(change):
    parameters.update({'sigma': change.new})
    figure.update()
    figure2.update()


uploader.observe(upload, names='value')
pixel_pitch.observe(update_pixel_pitch, names='value')
sigma.observe(update_sigma, names='value')


v.Container(fluid=True, children=[
    v.Row(children=[
        v.Col(cols=12, md=6, children=[
            v.Card(
                class_='mb-4',
                outlined=True,
                children=[
                    v.CardTitle(children=['Parameters']),
                    v.CardText(children=[
                        widgets.HBox([widgets.Label("MTF data:"), uploader]),
                        pixel_pitch,
                        sigma,
                    ]),
            ]),
        ]),
        v.Col(cols=12, md=6, children=[
            v.Card(
                class_='mb-4',
                outlined=True,
                children=[
                    v.CardTitle(children=['Figure']),
                    v.CardText(children=[
                        figure.canvas,
                        figure2.canvas,
                    ]),
            ]),
        ]),
    ]),
    # v.Row(children=[
    #     v.Col(cols=12, md=6, children=[
    #         output
    #     ]),
    # ]),
])
