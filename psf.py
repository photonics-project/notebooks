# %%
# %matplotlib widget
import ipyvuetify as v
import ipywidgets as widgets
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.special

from controls import OpticsControlPanel, WavelengthsControlPanel


parameters = {
    'diameter': 1,
    'focal_length': 2,
    'wavelengths': [3, 5],
}


def psf(x):
    return (2*scipy.special.jv(1, x)/x)**2


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

        self.ax.set_xlabel('Distance (µm)')
        self.ax.set_ylabel(R'PSF')
        self.ax.set_yscale('log')

        self.ax.grid(True)

        self.fig.canvas.draw()

    def plot(self):
        Da = parameters['diameter']
        focal_length = parameters['focal_length']
        xlambda = parameters['wavelengths']

        self.ax.clear()

        uu = np.linspace(0.1, 10, 100)

        for idx in range(len(xlambda)):
            xx = 1/np.pi * xlambda[idx] * focal_length/Da * uu
            self.ax.plot(xx, psf(uu))


plt.ioff()

figure = Figure()

optics_control_panel = OpticsControlPanel(diameter=parameters['diameter'], focal_length=parameters['focal_length'])
wavelengths_control_panel = WavelengthsControlPanel(xlambda=parameters['wavelengths'])
output = widgets.Output(layout={'border': '1px solid black'})


# @output.capture()
def update_optics():
    parameters['diameter'] = optics_control_panel.diameter
    parameters['focal_length'] = optics_control_panel.focal_length
    # print(parameters, optics_control_panel.fnumber)
    figure.update()

# @output.capture()
def update_wavelengths():
    parameters['wavelengths'] = wavelengths_control_panel.xlambda
    # print(parameters)
    figure.update()

optics_control_panel.on_change(update_optics)
wavelengths_control_panel.on_change(update_wavelengths)


v.Container(fluid=True, children=[
    v.Row(children=[
        v.Col(cols=12, md=6, children=[
            optics_control_panel.widget,
            v.Card(
                outlined=True,
                children=[
                    v.CardTitle(children=['Wavelengths']),
                    v.CardText(children=[
                        wavelengths_control_panel.widget,
                    ]),
            ]),
        ]),
        v.Col(cols=12, md=6, children=[
            v.Card(
                outlined=True,
                children=[
                    v.CardTitle(children=['Figure']),
                    v.CardText(children=[
                        figure.canvas,
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


# %% [markdown]
"""
## Description

This notebook computes the point spread function associated with a given optical chain.
"""
