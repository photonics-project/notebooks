# %%
# %matplotlib widget
import colour
import ipyvuetify as v
import ipywidgets as widgets
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate

from controls import (
    MyFloatSlider,
    MyFloatRangeSlider,
    SpectralBandsControlPanel,
)


parameters = {
    'temperature': 300,
    'spectral_bands': [(3.0, 5.0), (8.0, 12.0)],
    'figure_xlim': [0.2, 30],
}


output = widgets.Output()


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

        self.ax.set_xlabel('Wavelength (µm)')
        self.ax.set_ylabel(R'Spectral Radiant Sterance (W cm$^{-2}$ µm$^{-1}$ sr$^{-1}$)')

        self.ax.set_xlim(parameters['figure_xlim'])

        self.ax.grid(True)

        self.fig.canvas.draw()

    def plot(self):
        temperature = parameters['temperature']

        self.ax.clear()
        xlambda = np.linspace(0.2, 30, 150)
        self.ax.plot(xlambda, blackbody_spectral_radiant_sterance(temperature, xlambda), color='black')
        for (idx, (lambda_min, lambda_max)) in enumerate(parameters['spectral_bands']):
            xlambda = np.linspace(lambda_min, lambda_max)
            self.ax.fill_between(
                xlambda,
                blackbody_spectral_radiant_sterance(temperature, xlambda),
                label=f'Band #{idx+1}',
                color='none',
                hatch='///',
                edgecolor=f'C{idx}',
                alpha=0.5
                )
        self.ax.legend()


class Table():
    def __init__(self):
        self.widget = v.Html(tag='div', class_='d-flex flex-row', children=[])

        self.update()

    def update(self):
        temperature = parameters['temperature']
        spectral_bands = parameters['spectral_bands']

        values = [
            scipy.integrate.quad(
                lambda x: blackbody_spectral_radiant_sterance(temperature, x),
                lambda_min, lambda_max
            )[0]
            for (lambda_min, lambda_max) in spectral_bands
        ]

        table = v.DataTable(
            style_='width: 100%',
            hide_default_footer=True,
            disable_sort=True,
            headers=[
                {'text': 'Parameter', 'value': 'parameter'},
                {'text': 'Value', 'value': 'value'},
                {'text': 'Units', 'value': 'units'},
            ],
            items=[
                {
                    'parameter': f'Band #{idx+1} radiant sterance',
                    'value': f'{value:g}',
                    'units': 'W cm⁻² sr⁻¹',
                }
                for (idx, value) in enumerate(values)
            ],
        )
        self.widget.children = [table]


def blackbody_spectral_radiant_sterance(temperature, wavelength):
    return colour.colorimetry.blackbody.blackbody_spectral_radiance(wavelength*1e-6, temperature)/1e6/1e4


plt.ioff()

figure = Figure()
table = Table()


temperature = MyFloatSlider(
    label='Temperature (K)',
    value=300,
    min=0,
    max=3000,
    step=1,
)

spectral_bands_control_panel = SpectralBandsControlPanel(spectral_bands=parameters['spectral_bands'])

figure_xlim = MyFloatRangeSlider(
    label='xlim',
    value=parameters['figure_xlim'],
    min=0.2,
    max=30,
    step=0.1,
)


def update_temperature(change):
    parameters.update({'temperature': change.new})
    figure.update()
    table.update()


def update_wavelengths():
    parameters['wavelengths'] = spectral_bands_control_panel.spectral_bands
    figure.update()
    table.update()


def update_xlim(change):
    parameters.update({'figure_xlim': change.new})
    figure.update()


temperature.observe(update_temperature, names='value')
spectral_bands_control_panel.on_change(update_wavelengths)
figure_xlim.observe(update_xlim, names='value')


v.Container(fluid=True, children=[
    v.Row(children=[
        v.Col(cols=12, md=12, children=[widgets.HTML(value='<h1 style="text-align: center">Blackbody</h1>')]),
        v.Col(cols=12, md=6, children=[
            v.Card(
                class_='mb-4',
                outlined=True,
                children=[
                    v.CardTitle(children=['Parameters']),
                    v.CardText(children=[
                        temperature,
                    ]),
            ]),
            v.Card(
                class_='mb-4',
                outlined=True,
                children=[
                    v.CardTitle(children=['Spectral Bands']),
                    v.CardText(children=[
                        spectral_bands_control_panel.widget,
                    ]),
            ]),
            v.Card(
                class_='mb-4',
                outlined=True,
                children=[
                    v.CardTitle(children=['Results']),
                    v.CardText(children=[
                        table.widget,
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
                        figure_xlim,
                    ]),
            ]),
        ]),
    ]),
    # v.Row(children=[
    #     v.Col(cols=12, md=12, children=[
    #         output
    #     ]),
    # ]),
])


# %% [markdown]
"""
## Description

This notebook computes the blackbody spectrum.
$$
B_\lambda(\lambda,T)=\frac{2hc^2}{\lambda^5}\frac{1}{e^{hc/(\lambda k_\mathrm{B}T)}-1}
$$
"""
