import functools
from typing import List

import ipywidgets as widgets


class WavelengthsControlPanel():
    def __init__(self, *, xlambda: List[float]=[3.0, 5.0]):
        self.xlambda = xlambda

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
        button = widgets.Button(description='Add Wavelength', button_style='success', disabled=(ni>=10))
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
                    description=f'$\lambda_{idx}$ (µm)',
                    value=xx,
                    min=0.1,
                    max=30,
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
