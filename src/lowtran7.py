# %%
# %matplotlib widget
import base64
import io
import pathlib

import ipyvuetify as v
import ipywidgets as widgets
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from controls import SpectralBandsControlPanel


parameters = {
    'model': 6,
    'range': 1,
    'haze': 1,
    'spectral_bands': [(3.0, 5.0), (8.0, 12.0)],
}


data = np.load(pathlib.Path().resolve() / 'lowtran7.npz')
xlambda = data['xlambda'][::-1]
Tcoeff = data['Tcoeff'][:,::-1]


output = widgets.Output()


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
        haze_idx = parameters['haze'] - 1
        data_idx = np.ravel_multi_index((model_idx, range_idx, haze_idx), (6, 7, 4))

        self.ax.clear()
        self.ax.plot(xlambda, Tcoeff[data_idx])

        for (idx, (lambda_min, lambda_max)) in enumerate(parameters['spectral_bands']):
            self.ax.fill_between(
                xlambda[np.logical_and(xlambda > lambda_min, xlambda < lambda_max)],
                Tcoeff[data_idx][np.logical_and(xlambda > lambda_min, xlambda < lambda_max)],
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
        model_idx = parameters['model'] - 1
        range_idx = parameters['range'] - 1
        haze_idx = parameters['haze'] - 1
        data_idx = np.ravel_multi_index((model_idx, range_idx, haze_idx), (6, 7, 4))

        spectral_bands = parameters['spectral_bands']

        values = [
            np.trapz(
                Tcoeff[data_idx][np.logical_and(xlambda > lambda_min, xlambda < lambda_max)],
                xlambda[np.logical_and(xlambda > lambda_min, xlambda < lambda_max)]
                ) / (lambda_max-lambda_min)
            for (lambda_min, lambda_max) in spectral_bands
            ]

        table = v.DataTable(
            style_='width: 100%',
            hide_default_footer=True,
            disable_sort=True,
            headers=[
                {'text': 'Parameter', 'value': 'parameter'},
                {'text': 'Value', 'value': 'value'},
            ],
            items=[
                {
                    'parameter': f'Band #{idx+1} average transmission',
                    'value': f'{value:.3f}',
                }
                for (idx, value) in enumerate(values)
            ],
        )
        self.widget.children = [table]


class Downloader():
    def __init__(self):
        self.widget0 = v.Btn(text=True, children=['Prepare Data Export'])
        self.widget0.on_event('click', self.prepare_download)
        self.widget = widgets.HBox([self.widget0])

        self.reset()

    def prepare_download(self, widget, event, data):
        model_idx = parameters['model'] - 1
        range_idx = parameters['range'] - 1
        haze_idx = parameters['haze'] - 1
        data_idx = np.ravel_multi_index((model_idx, range_idx, haze_idx), (6, 7, 4))

        with io.StringIO() as data_table:
            print('Wavelength (um),Transmission', file=data_table)
            np.savetxt(data_table, np.column_stack((xlambda, Tcoeff[data_idx])), fmt=['%.4f', '%.6f'], delimiter=',')
            payload = base64.b64encode(data_table.getvalue().encode()).decode()

        self.widget.children = [
            v.Btn(txt=True, children=[v.Icon(children=['mdi-download'])], href=f'data:text/csv;base64,{payload}', attributes={'download': 'lowtran7.csv'})
        ]

    def reset(self):
        self.widget.children = [self.widget0]


plt.ioff()

figure = Figure()
table = Table()
downloader = Downloader()


model = v.Select(
    label='Model',
    items=[
        {'text': 'Tropical Atmosphere', 'value': 1},
        {'text': 'Midlatitude Summer', 'value': 2},
        {'text': 'Midlatitude Winter', 'value': 3},
        {'text': 'Subarctic Summer', 'value': 4},
        {'text': 'Subarctic Winter', 'value': 5},
        {'text': '1976 US Standard', 'value': 6},
        ],
    value=parameters['model'],
    )

range = v.Select(
    label='Range (km)',
    items=[
        {'text': 0.5, 'value': 1},
        {'text': 1, 'value': 2},
        {'text': 2, 'value': 3},
        {'text': 5, 'value': 4},
        {'text': 10, 'value': 5},
        {'text': 20, 'value': 6},
        {'text': 50, 'value': 7},
        ],
    value=parameters['range'],
    )

haze = v.Select(
    label='Haze',
    items=[
        {'text': 'None', 'value': 1},
        {'text': 'Rural (23 km)', 'value': 2},
        {'text': 'Rural (5 km)', 'value': 3},
        {'text': 'Urban (5 km)', 'value': 4},
        ],
    value=parameters['haze'],
    )

spectral_bands_control_panel = SpectralBandsControlPanel(
    spectral_bands=parameters['spectral_bands'],
    lambda_min=np.min(xlambda),
    lambda_max=np.max(xlambda),
    )


def update():
    figure.update()
    table.update()
    downloader.reset()


@output.capture()
def update_model(widget, event, data):
    parameters.update({'model': data})
    update()


def update_range(widget, event, data):
    parameters.update({'range': data})
    update()


def update_haze(widget, event, data):
    parameters.update({'haze': data})
    update()


def update_wavelengths():
    parameters['spectral_bands'] = spectral_bands_control_panel.spectral_bands
    update()


model.on_event('change', update_model)
range.on_event('change', update_range)
haze.on_event('change', update_haze)
spectral_bands_control_panel.on_change(update_wavelengths)


v.Container(fluid=True, children=[
    v.Col(cols=12, md=12, children=[widgets.HTML(value='<h1 style="text-align: center">LOWTRAN7</h1>')]),
    v.Row(children=[
        v.Col(cols=12, md=6, children=[
            v.Card(
                class_='mb-4',
                outlined=True,
                children=[
                    v.CardTitle(children=['Parameters']),
                    v.CardText(children=[
                        model,
                        range,
                        haze,
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
                    v.CardActions(children=[
                        v.Spacer(),
                        downloader.widget,
                    ])
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
    #     v.Col(cols=12, md=12, children=[
    #         output
    #     ]),
    # ]),
])


# %% [markdown]
"""
## Description

This notebook computes transmission through atmosphere for different atmospheric models at a variety of ranges.
"""
