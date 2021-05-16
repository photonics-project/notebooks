import functools
from typing import List, Tuple

import ipywidgets as widgets


class WavelengthsControlPanel():
    def __init__(self, *, xlambda: List[float]=[3.0, 5.0], Nmax=10, lambda_min=0.2, lambda_max=30):
        self.xlambda = xlambda
        self.Nmax = Nmax
        self.lambda_min = lambda_min
        self.lambda_max = lambda_max

        self._widget_container = widgets.VBox([])
        self.on_change_handler = type(None)
        self.on_add_wavelength_handler = type(None)
        self.on_remove_wavelength_handler = type(None)

        self.update_widgets()

    def add_wavelength(self, xlambda):
        self.xlambda.append(xlambda)
        self.update_widgets()
        self.on_add_wavelength_handler()

    def remove_wavelength(self, idx):
        self.xlambda.pop(idx)
        self.update_widgets()
        self.on_remove_wavelength_handler()

    def update_wavelength(self, idx, change):
        self.xlambda[idx] = change.new
        self.on_change_handler()

    def add_slider(self, ni):
        button = widgets.Button(description='Add Wavelength', button_style='success', disabled=(ni>=self.Nmax))
        button.on_click(lambda button: self.add_wavelength(5))
        return button

    def remove_slider(self, idx, ni):
        button = widgets.Button(description='', icon='trash', button_style='danger', disabled=(idx==0 and ni==1))
        button.on_click(lambda button: self.remove_wavelength(idx))
        return button

    def update_widgets(self):
        sliders = [
            widgets.HBox([
                widgets.FloatSlider(
                    description=f'$\lambda_{{{idx+1}}}$ (µm)',
                    value=xx,
                    min=self.lambda_min,
                    max=self.lambda_max,
                    step=0.1,
                    readout=True,
                    layout={'width': '50%'},
                    style = {'description_width': 'initial'},
                ),
                self.remove_slider(idx, len(self.xlambda)),
            ])
            for (idx, xx) in enumerate(self.xlambda)
        ]
        self._widget_container.children = sliders + [self.add_slider(len(self.xlambda))]

        for (idx, slider) in enumerate(sliders):
            slider.children[0].observe(functools.partial(self.update_wavelength, idx), names='value')

    @property
    def widget_container(self):
        return self._widget_container

    def on_change(self, handler):
        self.on_change_handler = handler

    def on_add_wavelength(self, handler):
        self.on_add_wavelength_handler = handler

    def on_remove_wavelength(self, handler):
        self.on_remove_wavelength_handler = handler


class SpectralBandsControlPanel():
    def __init__(self, *, spectral_bands: List[Tuple[float, float]]=[(3.0, 5.0)], Nmax=10, lambda_min=0.2, lambda_max=30):
        self.spectral_bands = spectral_bands
        self.Nmax = Nmax
        self.lambda_min = lambda_min
        self.lambda_max = lambda_max

        self._widget_container = widgets.VBox([])
        self.on_change_handler = type(None)
        self.on_add_spectral_band_handler = type(None)
        self.on_remove_spectral_band_handler = type(None)

        self.update_widgets()

    def add_spectral_band(self, spectral_bands):
        self.spectral_bands.append(spectral_bands)
        self.update_widgets()
        self.on_add_spectral_band_handler()

    def remove_spectral_band(self, idx):
        self.spectral_bands.pop(idx)
        self.update_widgets()
        self.on_remove_spectral_band_handler()

    def update_spectral_band(self, idx, change):
        self.spectral_bands[idx] = change.new
        self.on_change_handler()
        print(self.spectral_bands)

    def add_slider(self, ni):
        button = widgets.Button(description='Add Spectral Band', button_style='success', disabled=(ni>=self.Nmax))
        button.on_click(lambda button: self.add_spectral_band((3.0, 5.0)))
        return button

    def remove_slider(self, idx, ni):
        button = widgets.Button(description='', icon='trash', button_style='danger', disabled=(idx==0 and ni==1))
        button.on_click(lambda button: self.remove_spectral_band(idx))
        return button

    def update_widgets(self):
        sliders = [
            widgets.HBox([
                widgets.FloatRangeSlider(
                    description=f'$\Lambda_{{{idx+1}}}$ (µm)',
                    value=xx,
                    min=self.lambda_min,
                    max=self.lambda_max,
                    step=0.1,
                    readout=True,
                    style = {'description_width': 'initial'},
                ),
                self.remove_slider(idx, len(self.spectral_bands)),
            ])
            for (idx, xx) in enumerate(self.spectral_bands)
        ]
        self._widget_container.children = sliders + [self.add_slider(len(self.spectral_bands))]

        for (idx, slider) in enumerate(sliders):
            slider.children[0].observe(functools.partial(self.update_spectral_band, idx), names='value')

    @property
    def widget_container(self):
        return self._widget_container

    def on_change(self, handler):
        self.on_change_handler = handler

    def on_add_spectral_band(self, handler):
        self.on_add_spectral_band_handler = handler

    def on_remove_spectral_band(self, handler):
        self.on_remove_spectral_band_handler = handler
