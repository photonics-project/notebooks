# %%
# %matplotlib widget
import ipyvuetify as v
import ipywidgets as widgets
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.special as sc

from controls import (
    DetectorFormatControlPanel,
    OpticsControlPanel,
    WavelengthsControlPanel
)


parameters = {
    'diameter': 1,
    'focal_length': 2,
    'fnumber': 2,
    'Hdim': 1280,
    'Vdim': 720,
    'pitch': 20,
    'wavelengths': [3.0, 5.0],
}


output = widgets.Output()


class Figure():
    def __init__(self):
        (fig, [ax1, ax2]) = plt.subplots(ncols=2, constrained_layout=True)

        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = True
        fig.canvas.toolbar_position = 'right'

        self.fig = fig
        self.ax1 = ax1
        self.ax2 = ax2

        self.update()

    @property
    def canvas(self):
        return self.fig.canvas

    def update(self):
        Npixels = 9
        fnumber = parameters['fnumber']
        pitch = parameters['pitch']
        xlambda = np.array(parameters['wavelengths'])

        blur_spots = 2*sc.jn_zeros(1, 1)[0]/np.pi*xlambda*fnumber/pitch

        self.ax1.clear()
        self.ax2.clear()

        for ax in [self.ax1, self.ax2]:
            ax.set_aspect('equal')
            ax.set_xticklabels([])
            ax.set_xticks(np.arange(Npixels+1))
            ax.set_yticklabels([])
            ax.set_yticks(np.arange(Npixels+1))
            ax.set_axisbelow(True)
            ax.grid(True)

        self.ax1.set_title(f'Blur spot = {blur_spots[0]*pitch:g} µm', color='red')
        self.ax2.set_title(f'Blur spot = {blur_spots[1]*pitch:g} µm', color='blue')

        circle1 = mpl.patches.Circle((0.5, 0.5), blur_spots[0]/Npixels/2, color='red', alpha=0.5, transform=self.ax1.transAxes)
        circle2 = mpl.patches.Circle((0.5, 0.5), blur_spots[1]/Npixels/2, color='blue', alpha=0.5, transform=self.ax2.transAxes)

        self.ax1.add_patch(circle1)
        self.ax2.add_patch(circle2)

        self.ax1.grid(True)
        self.ax2.grid(True)

        self.fig.canvas.draw()


class Table():
    def __init__(self):
        self.widget = v.Html(tag='div', class_='d-flex flex-row', children=[])

        self.update()

    def update(self):
        fnumber = parameters['fnumber']
        Hdim = parameters['Hdim']
        Vdim = parameters['Vdim']
        pitch = parameters['pitch']
        xlambda = np.array(parameters['wavelengths'])

        blur_spots = 2*sc.jn_zeros(1, 1)[0]/np.pi*xlambda*fnumber/pitch

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
                    'parameter': 'Chip Width',
                    'value': f'{Hdim*(pitch/1e3):g}',
                    'units': 'mm',
                },
                {
                    'parameter': 'Chip Height',
                    'value': f'{Vdim*(pitch/1e3):g}',
                    'units': 'mm',
                },
                {
                    'parameter': 'Chip Area',
                    'value': f'{Hdim*Vdim*(pitch/1e3)**2:g}',
                    'units': 'mm²',
                },
                {
                    'parameter': 'Blur Spot (Wavelength #1)',
                    'value': f'{blur_spots[0]*pitch:g}',
                    'units': 'µm',
                },
                {
                    'parameter': 'Blur Spot (Wavelength #2)',
                    'value': f'{blur_spots[1]*pitch:g}',
                    'units': 'µm',
                },
            ],
        )
        self.widget.children = [table]


plt.ioff()

figure = Figure()

table = Table()

optics_control_panel = OpticsControlPanel(
    diameter=parameters['diameter'],
    focal_length=parameters['focal_length'],
)
detector_format_control_panel = DetectorFormatControlPanel(
    Hdim=parameters['Hdim'],
    Vdim=parameters['Vdim'],
    pitch=parameters['pitch'],
)
wavelengths_control_panel = WavelengthsControlPanel(xlambda=parameters['wavelengths'])


def update():
    figure.update()
    table.update()


def update_optics():
    parameters['diameter'] = optics_control_panel.diameter
    parameters['focal_length'] = optics_control_panel.focal_length
    parameters['fnumber'] = optics_control_panel.fnumber
    update()


def update_detector_format():
    parameters['Hdim'] = detector_format_control_panel.Hdim
    parameters['Vdim'] = detector_format_control_panel.Vdim
    parameters['pitch'] = float(detector_format_control_panel.pitch)
    update()


def update_wavelengths():
    parameters['wavelengths'] = wavelengths_control_panel.xlambda
    update()


optics_control_panel.on_change(update_optics)
detector_format_control_panel.on_change(update_detector_format)
wavelengths_control_panel.on_change(update_wavelengths)


v.Container(children=[
    v.Row(children=[
        v.Col(cols=12, md=6, children=[
            v.Card(
                class_='mb-4',
                outlined=True,
                children=[
                    v.CardTitle(children=['Optics']),
                    v.CardText(children=[
                        optics_control_panel.widget,
                    ]),
            ]),
            v.Card(
                class_='mb-4',
                outlined=True,
                children=[
                    v.CardTitle(children=['Wavelengths']),
                    v.CardText(children=[
                        wavelengths_control_panel.widget,
                    ]),
            ]),
            v.Card(
                class_='mb-4',
                outlined=True,
                children=[
                    v.CardTitle(children=['Detector']),
                    v.CardText(children=[
                        detector_format_control_panel.widget,
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

# %%
