# %%
# %matplotlib widget
import colour
import ipywidgets as widgets
import matplotlib.pyplot as pyplot
import numpy as np
import scipy.integrate


parameters = {
    'temperature': 300,
    'lambda_min': 3,
    'lambda_max': 5,
}


class BlackbodyFigure():
    def __init__(self, parameters):
        self.parameters = parameters

        temperature = parameters['temperature']
        lambda_min = parameters['lambda_min']
        lambda_max = parameters['lambda_max']
        spectral_band = [lambda_min, lambda_max]

        (fig, ax) = pyplot.subplots()

        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = True
        fig.canvas.toolbar_position = 'right'
        # fig.suptitle('Spectral Radiant Sterance')

        ax.set_xlabel('Wavelength')
        ax.set_ylabel(R'Spectral Radiant Sterance (W cm$^{-2}$ $\mu$m$^{-1}$ sr$^{-1}$)')
        ax.grid(True)

        self.fig = fig
        self.ax = ax

        self.plot = ax.plot(np.linspace(1, 15, 101), blackbody_spectral_radiant_sterance(temperature, np.linspace(1, 15, 101)))
        # self.lambda_min_line = self.ax.axvline(parameters['lambda_min'], color='black', linestyle='dashed')
        # self.lambda_max_line = self.ax.axvline(parameters['lambda_max'], color='black', linestyle='dashed')
        self.spectral_band_area = ax.fill_between(np.linspace(*spectral_band), blackbody_spectral_radiant_sterance(temperature, np.linspace(*spectral_band)), color='C0', alpha=0.5)
        self.fig.tight_layout()

    @property
    def canvas(self):
        return self.fig.canvas

    def update_plot(self):
        temperature = parameters['temperature']
        lambda_min = parameters['lambda_min']
        lambda_max = parameters['lambda_max']
        spectral_band = [lambda_min, lambda_max]

        self.plot[0].set_data(np.linspace(1, 15, 101), blackbody_spectral_radiant_sterance(temperature, np.linspace(1, 15, 101)))

        self.ax.relim()
        self.ax.autoscale_view()

        # self.lambda_min_line.remove()
        # self.lambda_max_line.remove()
        # self.lambda_min_line = self.ax.axvline(lambda_min, color='black', linestyle='dashed')
        # self.lambda_max_line = self.ax.axvline(lambda_max, color='black', linestyle='dashed')
        self.spectral_band_area.remove()
        self.spectral_band_area = self.ax.fill_between(np.linspace(*spectral_band), blackbody_spectral_radiant_sterance(temperature, np.linspace(*spectral_band)), color='C0', alpha=0.5)

        self.fig.tight_layout()
        self.fig.canvas.draw()


class BlackbodyTable():
    def __init__(self, parameters):
        self.parameters = parameters

        self.widget = widgets.HTML(value='')

        self.update_table()

    def update_table(self):
        temperature = parameters['temperature']
        lambda_min = parameters['lambda_min']
        lambda_max = parameters['lambda_max']
        spectral_band = [lambda_min, lambda_max]

        Le = lambda x: blackbody_spectral_radiant_sterance(temperature, x)

        self.widget.value = f'''
            <table style="width: 100%; border: solid; text-align: left">
              <thead>
                <th>Parameter</th>
                <th>Value</th>
                <th>Units</th>
              </thead>
              <tr>
                <td>In-band radiant sterance</td>
                <td>{scipy.integrate.quad(lambda x: Le(x), lambda_min, lambda_max)[0]:g}</td>
                <td>W cm<sup>-2</sup> sr<sup>-1</sup></td>
              </tr>
            </table>
            '''.strip()


def blackbody_spectral_radiant_sterance(temperature, wavelength):
    return colour.colorimetry.blackbody.blackbody_spectral_radiance(wavelength*1e-6,temperature)/1e6/1e4


pyplot.ioff()

blackbody_figure = BlackbodyFigure(parameters)
blackbody_table = BlackbodyTable(parameters)


temperature = widgets.FloatSlider(
    description='Temperature (K)',
    value=300, min=0, max=3000, step=1,
    layout={'width': '50%'},
    style = {'description_width': 'initial'},
    )
temperature1 = widgets.FloatText(
    value=300,
    layout={'width': '25%'},
    )
spectral_band = widgets.FloatRangeSlider(
    description='Spectral Band (µm)',
    value=[3, 5],
    min=1,
    max=15,
    step=0.1,
    readout=True,
    readout_format='.1f',
    layout={'width': '50%'},
    style={'description_width': 'initial'},
    )
output = widgets.Output(layout={'border': '1px solid black'})


@output.capture()
def update_temperature(change):
    blackbody_figure.parameters.update({'temperature': change.new})
    blackbody_figure.update_plot()
    blackbody_table.update_table()


@output.capture()
def update_spectral_band(change):
    blackbody_figure.parameters.update({'lambda_min': change.new[0]})
    blackbody_figure.parameters.update({'lambda_max': change.new[1]})
    blackbody_figure.update_plot()
    blackbody_table.update_table()


temperature.observe(update_temperature, names='value')
spectral_band.observe(update_spectral_band, names='value')

widgets.link((temperature, 'value'), (temperature1, 'value'))

widgets.AppLayout(
    header=None,
    left_sidebar=None,
    center=widgets.VBox([
        widgets.HTML(value='<h1 style="text-align: center">Blackbody</h1>'),
        widgets.HBox([temperature, temperature1]),
        spectral_band,
        blackbody_table.widget,
        blackbody_figure.canvas,
        ]),
    right_sidebar=None,
    footer=None,
    width='50%',
    )

# widgets.AppLayout(
#     center=widgets.VBox([
#         widgets.HTML(value='<h1 style="text-align: center">Blackbody</h1>'),
#         widgets.HBox([temperature, temperature1]),
#         spectral_band,
#         ], layout=widgets.Layout(border='solid')),
#     center=blackbody_figure.canvas,
#     footer=output,
#     pane_widths=[2, 2, 0],
#     layout=widgets.Layout(border='solid'),
#     )
