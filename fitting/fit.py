import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bagpipes as pipes

from astropy.table import Table

from load_data import load_data


def get_fit_instructions():
    """ Set up the desired fit_instructions dictionary. """

    dust = {}
    dust["type"] = "Salim"
    dust["eta"] = (1., 3.)
    dust["Av"] = (0., 8.)
    dust["delta"] = (-0.3, 0.3)
    dust["delta_prior"] = "Gaussian"
    dust["delta_prior_mu"] = 0.
    dust["delta_prior_sigma"] = 0.1
    dust["B"] = (0., 5.)

    zmet_factor = (0.02/0.014)

    nebular = {}
    nebular["logU"] = (-4., -2.)

    constant = {}
    constant["massformed"] = (0., 13.)
    constant["metallicity"] = (0.01/zmet_factor, 3.5/zmet_factor)
    constant["metallicity_prior"] = "log_10"
    constant["age_min"] = 0.
    constant["age_max"] = (0.001, 14.)
    constant["age_max_prior"] = "log_10"
    """
    dblplaw = {}
    dblplaw["massformed"] = (0., 13.)
    dblplaw["metallicity"] = (0.01/zmet_factor, 3.5/zmet_factor)
    dblplaw["metallicity_prior"] = "log_10"
    dblplaw["alpha"] = (0.1, 1000.)
    dblplaw["alpha_prior"] = "log_10"
    dblplaw["beta"] = (0.1, 1000.)
    dblplaw["beta_prior"] = "log_10"
    dblplaw["tau"] = (0.1, 15.)
    """
    fit_instructions = {}
    fit_instructions["dust"] = dust
    fit_instructions["constant"] = constant
    #fit_instructions["dblplaw"] = dblplaw
    fit_instructions["nebular"] = nebular
    fit_instructions["t_bc"] = 0.01
    fit_instructions["redshift"] = (0., 20.)

    return fit_instructions


filt_list = np.loadtxt("../filters/filt_list_combined.txt", dtype="str")

IDs = ["CEERS1_13256", "CEERS1_16943", "CEERS1_19996"]
redshifts = [4.9, 11.45, 4.9]
"""
for i in range(3):
    galaxy = pipes.galaxy(IDs[i], load_data, filt_list=filt_list, spectrum_exists=False)
    galaxy.plot()
input()
"""
fit_instructions = get_fit_instructions()

fit_cat = pipes.fit_catalogue(IDs, fit_instructions, load_data, run="donnan23_model",
                              cat_filt_list=filt_list, vary_filt_list=False,
                              make_plots=True, time_calls=False, redshifts=redshifts,
                              spectrum_exists=False, full_catalogue=True, redshift_sigma=0.15)

fit_cat.fit(n_live=500, verbose=True, mpi_serial=False)
