
# LEVEL-1B MODULE

import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

while current_dir in sys.path:
    sys.path.remove(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset

try:
    from l1b.src.initL1b import initL1b
    from common.io.writeToa import writeToa, readToa
    from common.src.auxFunc import getIndexBand
    from common.io.readFactor import readFactor, EQ_MULT, EQ_ADD, NC_EXT
except (ModuleNotFoundError, ImportError):
    from initL1b import initL1b
    from common.io.writeToa import writeToa, readToa
    from common.src.auxFunc import getIndexBand
    from common.io.readFactor import readFactor, EQ_MULT, EQ_ADD, NC_EXT

class l1b(initL1b):

    def __init__(self, auxdir, indir, outdir):
        super().__init__(auxdir, indir, outdir)

    def processModule(self):

        self.logger.info("Start of the L1B Processing Module")

        for band in self.globalConfig.bands:

            self.logger.info("Start of BAND " + band)

            # Read TOA - output of the ISM in Digital Numbers
            # -------------------------------------------------------------------------------
            toa = readToa(self.indir, self.globalConfig.ism_toa + band + '.nc')

            # Equalization (radiometric correction)
            # -------------------------------------------------------------------------------
            if self.l1bConfig.do_equalization:
                self.logger.info("EODP-ALG-L1B-1010: Radiometric Correction (equalization)")

                # Read the multiplicative and additive factors from auxiliary/equalization/
                eq_mult = readFactor(os.path.join(self.auxdir,self.l1bConfig.eq_mult+band+NC_EXT),EQ_MULT)
                eq_add = readFactor(os.path.join(self.auxdir,self.l1bConfig.eq_add+band+NC_EXT),EQ_ADD)

                # Do the equalization and save to file
                toa = self.equalization(toa, eq_add, eq_mult)
                writeToa(self.outdir, self.globalConfig.l1b_toa_eq + band, toa)

            # Restitution (absolute radiometric gain)
            # -------------------------------------------------------------------------------
            self.logger.info("EODP-ALG-L1B-1020: Absolute radiometric gain application (restoration)")
            toa = self.restoration(toa, self.l1bConfig.gain[getIndexBand(band)])

            # Write output TOA
            # -------------------------------------------------------------------------------
            writeToa(self.outdir, self.globalConfig.l1b_toa + band, toa)
            self.plotL1bToa(toa, self.outdir, band)

            self.logger.info("End of BAND " + band)

        self.logger.info("End of the L1B Module!")


    def equalization(self, toa, eq_add, eq_mult):
        """
        Equlization. Apply an offset and a gain.
        :param toa: TOA in DN
        :param eq_add: Offset in DN
        :param eq_mult: Gain factor, adimensional
        :return: TOA in DN, equalized
        """

        toa = (toa-eq_add)/eq_mult

        return toa

    def restoration(self,toa,gain):
        """
        Absolute Radiometric Gain - restore back to radiances
        :param toa: TOA in DN
        :param gain: gain in [rad/DN]
        :return: TOA in radiances [mW/sr/m2]
        """

        toa = toa*gain
        self.logger.debug('Sanity check. TOA in radiances after gain application ' + str(toa[1,-1]) + ' [mW/m2/sr]')

        return toa

    def plotL1bToa(self, toa_l1b, outputdir, band):

        toa_profile = toa_l1b[0, :] if len(toa_l1b.shape) > 1 else toa_l1b

        plt.figure(figsize=(20, 10))

        plt.plot(toa_profile, color='red', linewidth=2, label='TOA L1B')

        plt.title(f'Equalization and restoration for {band}', fontsize=20)

        plt.xlabel('ACT pixel [-]', fontsize=16)
        plt.ylabel('TOA [mW/m2/sr]', fontsize=16)

        plt.grid(True)

        plt.legend(loc='upper right', fontsize=12)

        output_file = os.path.join(outputdir, f'l1b_toa_{band}.png')
        plt.savefig(output_file, bbox_inches='tight')

        plt.close()

        self.logger.debug(f'Plot saved at: {output_file}')

        a=1 # dummy

