# %%
# %matplotlib widget
from pathlib import Path

import ipywidgets as widgets
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from controls import SpectralBandsControlPanel


parameters = {
    'model': 6,
    'range': 1,
    'spectral_bands': [(3.0, 5.0), (8.0, 12.0)],
}


data = np.load(Path().resolve() / 'lowtran/lowtran7.npz')
xlambda = data['xlambda']
Tcoeff = data['Tcoeff']


class Figure():
    def __init__(self):
        (fig, ax) = plt.subplots(constrained_layout=True)

        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = True
        fig.canvas.toolbar_position = 'right'

        self.fig = fig
        self.ax = ax

        self.update()

    @property
    def canvas(self):
        return self.fig.canvas

    def update(self):
        self.plot()

        self.ax.set_xlabel('Wavelength (µm)')
        self.ax.set_ylabel('Transmission')

        self.ax.set_xlim([0.2, 25])
        self.ax.set_ylim([0, 1])

        self.ax.grid(True)

        self.fig.canvas.draw()

    def plot(self):
        model_idx = parameters['model'] - 1
        range_idx = parameters['range'] - 1
        data_idx = np.ravel_multi_index((model_idx, range_idx), (6, 7))

        self.ax.clear()
        self.ax.plot(xlambda, Tcoeff[data_idx])

        # for (idx, (lambda_min, lambda_max)) in enumerate(parameters['spectral_bands']):
        #     self.ax.fill_between(
        #         xlambda[np.logical_and(xlambda > lambda_min, xlambda < lambda_max)],
        #         Tcoeff[data_idx][np.logical_and(xlambda > lambda_min, xlambda < lambda_max)],
        #         color='none',
        #         hatch='///',
        #         edgecolor=f'C{idx}',
        #         alpha=0.5
        #         )


plt.ioff()

figure = Figure()


model = widgets.Dropdown(
    options=[
        ('Tropical Atmosphere', 1),
        ('Midlatitude Summer', 2),
        ('Midlatitude Winter', 3),
        ('Subarctic Summer', 4),
        ('Subarctic Winter', 5),
        ('1976 US Standard', 6),
        ],
    value=parameters['model'],
    description='Model:',
    )

range = widgets.Dropdown(
    options=[
        (0.5, 1),
        (1, 2),
        (2, 3),
        (5, 4),
        (10, 5),
        (20, 6),
        (50, 7),
        ],
    value=parameters['range'],
    description='Range (km):',
    )

spectral_bands_control_panel = SpectralBandsControlPanel(spectral_bands=parameters['spectral_bands'])


def update_model(change):
    parameters.update({'model': change.new})
    figure.update()


def update_range(change):
    parameters.update({'range': change.new})
    figure.update()


def update_wavelengths():
    parameters['spectral_bands'] = spectral_bands_control_panel.spectral_bands
    figure.update()


def add_spectral_band():
    parameters['spectral_bands'] = spectral_bands_control_panel.spectral_bands
    figure.update()


def remove_spectral_band():
    parameters['spectral_bands'] = spectral_bands_control_panel.spectral_bands
    figure.update()


model.observe(update_model, names='value')
range.observe(update_range, names='value')
spectral_bands_control_panel.on_change(update_wavelengths)
spectral_bands_control_panel.on_add_spectral_band(add_spectral_band)
spectral_bands_control_panel.on_remove_spectral_band(remove_spectral_band)


widgets.AppLayout(
    header=None,
    left_sidebar=None,
    center=widgets.VBox([
        widgets.HTML(value='<h1 style="text-align: center">LOWTRAN7</h1>'),
        model,
        range,
        # spectral_bands_control_panel.widget_container,
        figure.canvas,
        ]),
    right_sidebar=None,
    footer=None,
    width='50%',
    )
