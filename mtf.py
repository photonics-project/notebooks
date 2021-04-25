# %%
# %matplotlib widget
import ipywidgets as widgets
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from controls import WavelengthsControlPanel


parameters = {
    'fnumber': 2,
    'pixel_pitch': 12,
    'wavelengths': [3, 5],
}


def optics_mtf(fnumber, xlambda, freq):
    freq_cutoff = 1/xlambda/fnumber
    xx = freq/freq_cutoff

    return np.piecewise(xx, [xx<=1, xx>1], [lambda x: 2/np.pi*(np.arccos(x)-x*np.sqrt(1-x**2)), 0])


def pixel_mtf(pitch, freq):
    xx = freq*pitch
    mtf = np.abs(np.sinc(xx))

    return mtf


class Figure():
    def __init__(self):
        fig = plt.figure(constrained_layout=True)
        gridspec = mpl.gridspec.GridSpec(nrows=2, ncols=2, figure=fig)
        ax1 = fig.add_subplot(gridspec[0, 0])
        ax2 = fig.add_subplot(gridspec[0, 1])
        ax3 = fig.add_subplot(gridspec[1, :])

        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = True
        fig.canvas.toolbar_position = 'right'

        self.fig = fig
        self.ax1 = ax1
        self.ax2 = ax2
        self.ax3 = ax3

        self.update()

    @property
    def canvas(self):
        return self.fig.canvas

    @property
    def axes(self):
        return (self.ax1, self.ax2, self.ax3)

    def update(self):
        self.plot_optics_mtf()
        self.plot_pixel_mtf()
        self.plot_composite_mtf()

        for ax in self.axes:
            ax.set_ylabel('MTF')
            ax.set_xlabel('Spatial Frequency (lp/mm)')
            ax.grid(True)

        self.ax1.legend()
        self.ax3.legend()

        self.fig.canvas.draw()

    def plot_optics_mtf(self):
        fnumber = parameters['fnumber']
        pixel_pitch = parameters['pixel_pitch']
        xlambda = parameters['wavelengths']

        self.ax1.clear()
        self.ax1.set_title('Optics MTF')
        for (idx, xx) in enumerate(xlambda):
            freq = 2/pixel_pitch*np.linspace(0, 1, 101)
            mtf = optics_mtf(fnumber, xx, freq)
            self.ax1.plot(freq*1000, mtf, label=f'$\lambda_{idx}$')

    def plot_pixel_mtf(self):
        pixel_pitch = parameters['pixel_pitch']

        freq = 2/pixel_pitch*np.linspace(0, 1, 201)

        mtf = pixel_mtf(pixel_pitch, freq)

        self.ax2.clear()
        self.ax2.set_title('Pixel MTF')
        self.ax2.plot(freq*1000, mtf)

    def plot_composite_mtf(self):
        fnumber = parameters['fnumber']
        pixel_pitch = parameters['pixel_pitch']
        xlambda = parameters['wavelengths']

        self.ax3.clear()
        self.ax3.set_title('Composite MTF')
        for (idx, xx) in enumerate(xlambda):
            freq = 2/pixel_pitch*np.linspace(0, 1, 101)
            mtf = optics_mtf(fnumber, xx, freq) * pixel_mtf(pixel_pitch, freq)
            self.ax3.plot(freq*1000, mtf, label=f'$\lambda_{idx}$')


plt.ioff()

figure = Figure()

fnumber = widgets.FloatSlider(
    description='Optics f/#',
    value=parameters['fnumber'],
    min=1,
    max=8,
    step=0.1,
    style = {'description_width': 'initial'},
    )

pixel_pitch = widgets.FloatSlider(
    description='Pixel Pitch (µm)',
    value=parameters['pixel_pitch'],
    min=2,
    max=100,
    step=1,
    style = {'description_width': 'initial'},
    )

wavelengths_control_panel = WavelengthsControlPanel(xlambda=parameters['wavelengths'])


def update_fnumber(change):
    parameters.update({'fnumber': change.new})
    figure.update()


def update_pixel_pitch(change):
    parameters.update({'pixel_pitch': change.new})
    figure.update()


def update_wavelengths():
    parameters['wavelengths'] = wavelengths_control_panel.xlambda
    figure.update()


def add_wavelength():
    parameters['wavelengths'] = wavelengths_control_panel.xlambda
    figure.plot_optics_mtf()
    figure.update()


def remove_wavelength():
    parameters['wavelengths'] = wavelengths_control_panel.xlambda
    figure.plot_optics_mtf()
    figure.update()


fnumber.observe(update_fnumber, names='value')
pixel_pitch.observe(update_pixel_pitch, names='value')
wavelengths_control_panel.on_change(update_wavelengths)
wavelengths_control_panel.on_add_wavelength(add_wavelength)
wavelengths_control_panel.on_remove_wavelength(remove_wavelength)


widgets.AppLayout(
    header=None,
    left_sidebar=None,
    center=widgets.VBox([
        widgets.HTML(value='<h1 style="text-align: center">Modulation Transfer Function</h1>'),
        fnumber,
        pixel_pitch,
        wavelengths_control_panel.widget_container,
        figure.canvas,
        ]),
    right_sidebar=None,
    footer=None,
    width='50%',
    )
