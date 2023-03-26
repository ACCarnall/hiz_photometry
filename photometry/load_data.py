import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bagpipes as pipes

from astropy.table import Table


def load_data(ID):

    #cat = Table.read("JWST_N45_phot_updated_ZP.fits").to_pandas()
    cat = pd.read_csv("CEERS_Full.phot", delim_whitespace=True)

    cat.index = cat["ID"].astype(str).values#.astype(int).

    flux_cols = ["F606W_flux",
                 "F814W_flux",
                 "F105W_flux",
                 "F125W_flux",
                 "F140W_flux",
                 "F160W_flux",
                 "F115W_flux",
                 "F150W_flux",
                 "F200W_flux",
                 "F277W_flux",
                 "F356W_flux",
                 "F410M_flux",
                 "F444W_flux"]

    err_cols = ["F606W_flux_error",
                "F814W_flux_error",
                "F105W_flux_error",
                "F125W_flux_error",
                "F140W_flux_error",
                "F160W_flux_error",
                "F115W_flux_error",
                "F150W_flux_error",
                "F200W_flux_error",
                "F277W_flux_error",
                "F356W_flux_error",
                "F410M_flux_error",
                "F444W_flux_error"]

    photometry = np.c_[cat.loc[str(ID), flux_cols],
                       cat.loc[str(ID), err_cols]]

    photometry *= 10**-3

    # Limit SNR to 20 sigma in each band
    for i in range(len(photometry)):
        if np.abs(photometry[i, 0]/photometry[i, 1]) > 20.:
            photometry[i, 1] = np.abs(photometry[i, 0]/20.)

    # blow up the errors associated with any N/A points in the photometry
    for i in range(len(photometry)):
        if (photometry[i, 1] <= 0) or np.isnan(photometry[i, 1]):
            photometry[i, 0] = 0.
            photometry[i, 1] = 9.9*10**99.

    return photometry.astype("float")
