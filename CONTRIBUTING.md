## Contributing

To start developing notebooks for the Photonics Project, first clone the repository,
  and install the required dependencies (ideally, in a virtual environment):

```shell
git clone git@github.com:photonics-project/notebooks
cd notebooks
pip install -r requirements/dev-requirements.txt
pip-sync requirements/*.txt
```

While the purpose of this project is to develop Jupyter notebooks for optoelectronic device engineering,
  actual `*.ipynb` notebook files are conspicuously absent and explicitly ignored.
Because version controlling notebooks can be quite difficult, with notebooks being just a serialized JSON object
  (containing metadata, rich text, and possibly binary blobs),
  we have opted to instead write the notebooks as plain Python scripts and convert to notebooks on-the-fly.
Additionally, the notebooks are meant to be run using [`voila`][voila],
  to provide the look and feel more close to that of an application.
The `blackbody.py` file is a good example of how this is done, with cells denoted by `# %%`.
The conversion is done with [`jupytext`][jupytext] and more information on this approach can be found there.
Development can be streamlined by automatically converting the script on changes, and then refreshing the browser.

```shell
jupytext --to notebook blackbody.py
watchmedo shell-command --patterns="blackbody.py" --command="jupytext --to notebook blackbody.py"
voila blackbody.ipynb
```

A `Makefile` has been provided to assist with development.
It is possible to start a development server with `make start-dev`,
  which will automatically keep the notebooks in sync.
All that is needed is to refresh the browser.
The development server can be stopped with `make stop-dev`.
Try `make help` for a list of all the options.


### Widget Library

To assist with creating new Photonics Project notebooks,
  we have been developing, and will continue to maintain, a library of composite widgets (see [here](controls.py)).
Please check out the following notebooks for a demonstration:

| Notebook | Link |
|:--|:--|
| `controls-gallery` | [![Binder](https://mybinder.org/badge_logo.svg)][controls-gallery] |

[controls-gallery]: https://mybinder.org/v2/gh/photonics-project/notebooks/main?urlpath=voila%2Frender%2Fbuild%2Fcontrols-gallery.ipynb


[voila]: https://github.com/voila-dashboards/voila
[jupytext]: https://github.com/mwouts/jupytext
