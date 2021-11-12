# %% [markdown]
# #Controls
# Below is a gallery of control panels to assist with notebook development for the Photonics Project.


# %%
import ipyvuetify as v

from controls import MyFloatSlider
from controls import MyFloatRangeSlider
from controls import WavelengthsControlPanel
from controls import SpectralBandsControlPanel


wavelengths_control_panel = WavelengthsControlPanel(xlambda=[4, 10])
spectral_bands_control_panel = SpectralBandsControlPanel(spectral_bands=[(3, 5), (8, 12)], lambda_max=25)


output = {
    'wavelengths_control_panel': v.Html(tag='span', children=[str(wavelengths_control_panel)]),
    'spectral_bands_control_panel': v.Html(tag='span', children=[str(spectral_bands_control_panel)]),
}


def update():
    output['wavelengths_control_panel'].children = str(wavelengths_control_panel),
    output['spectral_bands_control_panel'].children = str(spectral_bands_control_panel),


wavelengths_control_panel.on_change(update)
spectral_bands_control_panel.on_change(update)


v.Html(
    tag='div',
    class_='d-flex flex-row',
    children=[
        v.Card(
            outlined=True,
            children=[
                v.CardTitle(children=['Float Slider']),
                v.CardText(children=[
                    MyFloatSlider(
                        label='Wavelength #1',
                        min=0, max=25,
                        value=3
                    ),
                ]),
            ]
        ),
        v.Card(
            outlined=True,
            children=[
                v.CardTitle(children=['Float Range Slider']),
                v.CardText(children=[
                    MyFloatRangeSlider(
                        label='Band #1',
                        min=0, max=25,
                        value=[3, 5]
                    ),
                ]),
            ]
        ),
        v.Card(
            outlined=True,
            children=[
                v.CardTitle(children=['Wavelengths Control Panel']),
                v.CardText(children=[
                    wavelengths_control_panel.widget,
                    output['wavelengths_control_panel'],
                ]),
            ]
        ),
        v.Card(
            outlined=True,
            children=[
                v.CardTitle(children=['Spectral Bands Control Panel']),
                v.CardText(children=[
                    spectral_bands_control_panel.widget,
                    output['spectral_bands_control_panel'],
                ]),
            ]
        ),
    ]
)
