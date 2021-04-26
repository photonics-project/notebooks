# %% [markdown]
# #Controls
# Below is a gallery of control panels to assist with notebook development for the Photonics Project.


# %% [markdown]
# ## Wavelengths Control Panel
# Here is a control panel for selecting the values for a number of wavelengths.
# %%
from controls import WavelengthsControlPanel


control_panel = WavelengthsControlPanel()
control_panel.widget_container


# %% [markdown]
# ## Spectral Bands Control Panel
# Here is a control panel for defining a number of spectral bands.
# %%
from controls import SpectralBandsControlPanel


control_panel = SpectralBandsControlPanel()
control_panel.widget_container
