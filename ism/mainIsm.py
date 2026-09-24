# MAIN FUNCTION TO CALL THE ISM MODULE

from ism.src.ism import ism

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r"C:\Users\jesus\Desktop\MISE\5SEMICUATRIMESTRE\EODP\EODC_Code_2\auxiliary"
indir = r"C:\Users\jesus\Desktop\MISE\5SEMICUATRIMESTRE\EODP\EODP_TER_2021-20260917T101917Z-1-001\EODP_TER_2021\EODP-TS-ISM\input\gradient_alt100_act150" # small scene
outdir = r"C:\Users\jesus\Desktop\MISE\5SEMICUATRIMESTRE\EODP\EODP_TER_2021-20260917T101917Z-1-001\EODP_TER_2021\EODP-TS-ISM\output"

# Initialise the ISM
myIsm = ism(auxdir, indir, outdir)
myIsm.processModule()