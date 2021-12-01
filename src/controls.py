import functools
from typing import List, Tuple

import ipyvuetify as v
import ipywidgets as widgets
import traitlets


class MyFloatSlider(v.VuetifyTemplate):
    label = traitlets.Unicode().tag(sync=True)
    value = traitlets.Float(default_value=0).tag(sync=True)
    min = traitlets.Float(default_value=0).tag(sync=True)
    max = traitlets.Float(default_value=1).tag(sync=True)
    step = traitlets.Float(default_value=0.1).tag(sync=True)

    @traitlets.default('template')
    def _template(self):
        return '''
          <v-slider
            v-model="value"
            :label="label"
            :min="min" :max="max" :step="step"
            hide-details
            style="width: 400px"
            class="align-center"
          >
            <template v-slot:append>
              <v-text-field
                v-model="value"
                type="number"
                :min="min" :step="step"
                dense hide-details outlined single-line
                class="mt-0 pt-0"
                style="width: 5em"
                @change="$set(value, $event)"
              ></v-text-field>
            </template>
          </v-slider>
        '''


class MyFloatRangeSlider(v.VuetifyTemplate):
    label = traitlets.Unicode().tag(sync=True)
    value = traitlets.List(traitlets.Float(), default_value=[0, 1]).tag(sync=True)
    min = traitlets.Float(default_value=0).tag(sync=True)
    max = traitlets.Float(default_value=1).tag(sync=True)
    step = traitlets.Float(default_value=0.1).tag(sync=True)

    @traitlets.default('template')
    def _template(self):
        return '''
          <v-range-slider
            v-model="value"
            :label="label"
            :min="min" :max="max" :step="step"
            hide-details
            style="width: 400px"
            class="align-center"
          >
            <template v-slot:append>
              <v-text-field
                type="number"
                :value="value[0]"
                :min="min" :step="step"
                dense hide-details outlined single-line
                class="mt-0 pt-0"
                style="width: 5em"
                @change="$set(value, 0, $event)"
              ></v-text-field>
              <v-text-field
                type="number"
                :value="value[1]"
                :max="max" :step="step"
                dense hide-details outlined single-line
                class="mt-0 pt-0"
                style="width: 5em"
                @change="$set(value, 1, $event)"
              ></v-text-field>
            </template>
          </v-range-slider>
        '''


class WavelengthsControlPanel():
    def __init__(self, *, xlambda: List[float]=[3.0, 5.0], lambda_min=0.2, lambda_max=30):
        self.xlambda = xlambda
        self.lambda_min = lambda_min
        self.lambda_max = lambda_max
        self._active_wavelengths = [0]

        self.on_change_handler = type(None)

    def toggle_wavelength(self, widget, event, data):
        self._active_wavelengths = data
        self.on_change_handler()

    def update_wavelength(self, idx, change):
        self.xlambda[idx] = change.new
        self.on_change_handler()

    @property
    def active_wavelengths(self):
        return sorted(self._active_wavelengths)

    @property
    def widget(self):
        sliders = [
            MyFloatSlider(
                label=f'Wavelength #{idx+1} (µm)',
                value=xx,
                min=self.lambda_min,
                max=self.lambda_max,
                step=0.1,
            )
            for (idx, xx) in enumerate(self.xlambda)
        ]
        for (idx, slider) in enumerate(sliders):
            slider.observe(functools.partial(self.update_wavelength, idx), names='value')

        toggle = v.BtnToggle(
            v_model=self._active_wavelengths,
            mandatory=True,
            multiple=True,
            children=[
                v.Btn(x_small=True, active=True, children=[f'{idx+1}']) for (idx, xx) in enumerate(self.xlambda)
            ]
        )

        toggle.on_event('change', self.toggle_wavelength)

        return v.Html(
            tag='div', class_='d-flex flex-column',
            children=[
                # toggle,
                # v.Html(tag='br'),
                *sliders
            ]
        )

    def on_change(self, handler):
        self.on_change_handler = handler

    def __str__(self):
        return str({
            # 'active_wavelengths': self.active_wavelengths,
            'xlambda': self.xlambda,
        })


class SpectralBandsControlPanel():
    def __init__(self, *, spectral_bands: List[Tuple[float, float]]=[(3.0, 5.0)], lambda_min=0.2, lambda_max=30):
        self.spectral_bands = spectral_bands
        self.lambda_min = lambda_min
        self.lambda_max = lambda_max
        self._active_spectral_bands = [0]

        self.on_change_handler = type(None)

    def toggle_spectral_band(self, widget, event, data):
        self._active_spectral_bands = data
        self.on_change_handler()

    def update_spectral_band(self, idx, change):
        self.spectral_bands[idx] = change.new
        self.on_change_handler()

    @property
    def active_spectral_bands(self):
        return sorted(self._active_spectral_bands)

    @property
    def widget(self):
        sliders = [
            MyFloatRangeSlider(
                label=f'Band #{idx+1} (µm)',
                value=xx,
                min=self.lambda_min,
                max=self.lambda_max,
                step=0.1,
            )
            for (idx, xx) in enumerate(self.spectral_bands)
        ]
        for (idx, slider) in enumerate(sliders):
            slider.observe(functools.partial(self.update_spectral_band, idx), names='value')

        toggle = v.BtnToggle(
            v_model=self._active_spectral_bands,
            mandatory=True,
            multiple=True,
            children=[
                v.Btn(x_small=True, active=True, children=[f'{idx+1}']) for (idx, xx) in enumerate(self.spectral_bands)
            ]
        )

        toggle.on_event('change', self.toggle_spectral_band)

        return v.Html(
            tag='div', class_='d-flex flex-column',
            children=[
                # toggle,
                # v.Html(tag='br'),
                *sliders
            ]
        )

    def on_change(self, handler):
        self.on_change_handler = handler

    def __str__(self):
        return str({
            # 'active_spectral_bands': self.active_spectral_bands,
            'spectral_bands': self.spectral_bands,
        })


class OpticsControlPanel():
    def __init__(self, *, diameter: float=1.0, focal_length: float=2.0):
        self.diameter = diameter
        self.focal_length = focal_length

        self.on_change_handler = type(None)

    @property
    def fnumber(self):
        return self.focal_length/self.diameter

    def update_parameters(self, parameter, change):
        setattr(self, parameter, change.new)
        self.on_change_handler()

    @property
    def widget(self):
        diameter = MyFloatSlider(
            label='Diameter (cm)',
            value=self.diameter,
            min=0.1,
            max=10,
            step=0.1,
        )
        focal_length = MyFloatSlider(
            label='Focal Length (cm)',
            value=self.focal_length,
            min=0.1,
            max=10,
            step=0.1,
        )

        diameter.observe(functools.partial(self.update_parameters, 'diameter'), names='value')
        focal_length.observe(functools.partial(self.update_parameters, 'focal_length'), names='value')

        return v.Html(
            tag='div', class_='d-flex flex-column',
            children=[
                diameter,
                focal_length,
            ]
        )

    def on_change(self, handler):
        self.on_change_handler = handler

    def __str__(self):
        return str({
            'diameter': self.diameter,
            'focal_length': self.focal_length,
            'fnumber': self.fnumber,
        })


class DetectorFormatControlPanel():
    def __init__(self, *, Hdim: int=1280, Vdim: int=720, pitch: float=20.0):
        self.Hdim = Hdim
        self.Vdim = Vdim
        self.pitch = pitch

        self.on_change_handler = type(None)

    def update_parameters(self, parameter, widget, event, data):
        setattr(self, parameter, data)
        self.on_change_handler()

    @property
    def widget(self):
        Hdim = v.TextField(
            label='Horizontal Dimension (pixels)',
            type='number',
            value=self.Hdim,
            attributes={
                'min': 1,
                'max': 12288,
            }
        )
        Vdim = v.TextField(
            label='Vertical Dimension (pixels)',
            type='number',
            value=self.Vdim,
            attributes={
                'min': 1,
                'max': 12288,
            }
        )
        pitch = v.TextField(
            label='Pixel Pitch (µm)',
            type='number',
            value=self.pitch,
            attributes={
                'min': 2,
                'max': 120,
            }
        )

        Hdim.on_event('input', functools.partial(self.update_parameters, 'Hdim'))
        Vdim.on_event('input', functools.partial(self.update_parameters, 'Vdim'))
        pitch.on_event('input', functools.partial(self.update_parameters, 'pitch'))

        return v.Html(
            tag='div', class_='d-flex flex-column',
            children=[Hdim, Vdim, pitch]
        )

    def on_change(self, handler):
        self.on_change_handler = handler

    def __str__(self):
        return str({
            'Hdim': self.Hdim,
            'Vdim': self.Vdim,
            'pitch': self.pitch,
        })
