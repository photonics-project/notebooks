# ---
# jupyter:
#   kernelspec:
#     name: python3
#     display_name: Python 3
#     language: python
# ---


# %% [markdown]
# #Controls
# Below is a gallery of control panels to assist with notebook development for the Photonics Project.


# %%
import ipyvuetify as v

from controls import (
    DetectorFormatControlPanel,
    MyFloatRangeSlider,
    MyFloatSlider,
    OpticsControlPanel,
    SpectralBandsControlPanel,
    WavelengthsControlPanel,
)


my_float_slider = MyFloatSlider(label='Wavelength #1', min=0, max=25, value=3)
my_float_range_slider = MyFloatRangeSlider(label='Band #1', min=0, max=25, value=[3, 5], resettable=True)
optics_control_panel = OpticsControlPanel(diameter=1.0, focal_length=2.0)
detector_format_control_panel = DetectorFormatControlPanel(Hdim=1280, Vdim=720, pitch=12)
wavelengths_control_panel = WavelengthsControlPanel(xlambda=[4, 10])
spectral_bands_control_panel = SpectralBandsControlPanel(spectral_bands=[(3, 5), (8, 12)], lambda_max=25)


output = {
    'my_float_slider': v.Html(tag='span', children=[str(my_float_slider)]),
    'my_float_range_slider': v.Html(tag='span', children=[str(my_float_range_slider)]),
    'optics_control_panel': v.Html(tag='span', children=[str(optics_control_panel)]),
    'detector_format_control_panel': v.Html(tag='span', children=[str(detector_format_control_panel)]),
    'wavelengths_control_panel': v.Html(tag='span', children=[str(wavelengths_control_panel)]),
    'spectral_bands_control_panel': v.Html(tag='span', children=[str(spectral_bands_control_panel)]),
}


def update(*args, **kwargs):
    output['my_float_slider'].children = str(my_float_slider),
    output['my_float_range_slider'].children = str(my_float_range_slider),
    output['optics_control_panel'].children = str(optics_control_panel),
    output['detector_format_control_panel'].children = str(detector_format_control_panel),
    output['wavelengths_control_panel'].children = str(wavelengths_control_panel),
    output['spectral_bands_control_panel'].children = str(spectral_bands_control_panel),


my_float_slider.observe(update, names='value')
my_float_range_slider.observe(update, names='value')
optics_control_panel.on_change(update)
detector_format_control_panel.on_change(update)
wavelengths_control_panel.on_change(update)
spectral_bands_control_panel.on_change(update)


def cardify(title, widgets):
    return (
        v.Card(
            outlined=True,
            children=[
                v.CardTitle(children=[title]),
                v.CardText(children=widgets)
            ]
        )
    )


v.Container(fluid=True, children=[
    v.Row(children=[
        v.Col(cols=12, md=6, children=[
            cardify('Float Slider', [
                my_float_slider,
                output['my_float_slider'],
            ])
        ]),
        v.Col(cols=12, md=6, children=[
            cardify('Float Range Slider', [
                my_float_range_slider,
                output['my_float_range_slider'],
            ])
        ]),
        v.Col(cols=12, md=6, children=[
            cardify('Wavelengths Control Panel', [
                wavelengths_control_panel.widget,
                output['wavelengths_control_panel'],
            ])
        ]),
        v.Col(cols=12, md=6, children=[
            cardify('Spectral Bands Control Panel', [
                spectral_bands_control_panel.widget,
                output['spectral_bands_control_panel'],
            ])
        ]),
        v.Col(cols=12, md=6, children=[
            cardify('Optics Control Panel', [
                optics_control_panel.widget,
                output['optics_control_panel'],
            ])
        ]),
        v.Col(cols=12, md=6, children=[
            cardify('Detector Format Control Panel', [
                detector_format_control_panel.widget,
                output['detector_format_control_panel'],
            ])
        ]),
    ])
])
