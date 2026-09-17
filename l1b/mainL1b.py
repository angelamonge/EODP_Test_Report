
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\\Users\\jesus\\Desktop\\MISE\\5 SEMICUATRIMESTRE\\Earth Observation Data Processing\\EODC_Code_2\\auxiliary'
indir = r"C:\\Users\\jesus\\Desktop\\MISE\\5 SEMICUATRIMESTRE\\Earth Observation Data Processing\\EODP_TER_2021-20260917T101917Z-1-001\\EODP_TER_2021\\EODP-TS-L1B\\input"
outdir = r"C:\\Users\\jesus\\Desktop\\MISE\\5 SEMICUATRIMESTRE\\Earth Observation Data Processing\\EODP_TER_2021-20260917T101917Z-1-001\\EODP_TER_2021\\EODP-TS-L1B\\output_test"

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
