import sys

import jinja2
import matplotlib.pyplot as plt
import numpy as np


TAPE5_TEMPLATE = jinja2.Environment().from_string(r'''
{{'%5d'|format(MODEL)}}    1    0    0{{'%40s'|format(' '*40)}}    0
{{'%5d'|format(IHAZE)}}    0    0
{{'%10.3f'|format(H1)}}{{'%20s'|format(' '*20)}}{{'%10.3f'|format(RANGE)}}
   400.000 50000.000{{'%10.3f'|format(DV)}}
{{'%5d'|format(IRPT)}}
'''.strip())


models = np.array([1, 2, 3, 4, 5, 6])
ranges = np.array([0.5, 1, 2, 5, 10, 20, 50])
haze_types = np.array([0, 1, 2, 5])

parameters = np.array(np.meshgrid(models, ranges, haze_types, indexing='ij')).reshape((3, -1)).T

H1 = 0.0
DV = 5

assert ((50000-400) % DV) == 0

Npts = (50000-400)//DV + 1

xnu = np.linspace(400, 50000, Npts)


def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'prepare-TAPE5':
        prepare_TAPE5()

    if len(sys.argv) == 2 and sys.argv[1] == 'process-TAPE7':
        process_TAPE7()

    if len(sys.argv) == 2 and sys.argv[1] == 'plot':
        plot()


def prepare_TAPE5():
    with open('TAPE5', 'w') as f:
        for (idx, (MODEL, RANGE, IHAZE)) in enumerate(parameters):
            IRPT = 0 if idx == len(parameters)-1 else 1
            print(
                TAPE5_TEMPLATE.render(
                    MODEL=MODEL,
                    IHAZE=IHAZE,
                    H1=H1,
                    RANGE=RANGE,
                    DV=DV,
                    IRPT=IRPT,
                ),
                file=f
            )


def process_TAPE7():
    xlambda = 1e4/xnu
    Tcoeff = np.zeros((len(parameters), Npts))

    with open('TAPE7', 'r') as f:
        for idx in range(len(parameters)):
            Tcoeff[idx] = np.loadtxt(f, skiprows=11, max_rows=Npts, usecols=(1,))
            f.read(8)

    # for idx in range(len(data)):
    #     print(np.interp(1000, xnu, data[idx]))

    np.savez('lowtran7.npz', xlambda=xlambda, Tcoeff=Tcoeff)


def plot():
    data = np.load('lowtran7.npz')

    xlambda = data['xlambda']
    Tcoeff = data['Tcoeff']

    idx = np.ravel_multi_index((4, 1), (len(models), len(ranges)))

    (fig, ax) = plt.subplots(constrained_layout=True)

    ax.plot(xlambda, Tcoeff[idx])

    ax.set_xlabel('Wavelength (µm)')
    ax.set_ylabel('Transmission')

    ax.set_xlim([30, 5])
    ax.set_ylim([0, 1])

    fig.savefig('transmission.png')


main()
