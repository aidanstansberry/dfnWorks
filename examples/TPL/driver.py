#"""
#   :synopsis: Driver run file for TPL example
#   :version: 2.0
#   :maintainer: Jeffrey Hyman
#.. moduleauthor:: Jeffrey Hyman <jhyman@lanl.gov>
#"""

from pydfnworks import *
import os

jobname = os.getcwd() + "/output"
dfnFlow_file = os.getcwd() + '/dfn_explicit.in'
dfnTrans_file = os.getcwd() + '/PTDFN_control.dat'

DFN = DFNWORKS(jobname,
               dfnFlow_file=dfnFlow_file,
               dfnTrans_file=dfnTrans_file,
               ncpu=8)

DFN.params['domainSize']['value'] = [15, 15, 15]
DFN.params['h']['value'] = 0.1
DFN.params['domainSizeIncrease']['value'] = [.5,.5,.5]
DFN.params['keepOnlyLargestCluster']['value'] = True
DFN.params['ignoreBoundaryFaces']['value'] = False
DFN.params['boundaryFaces']['value'] = [1,1,0,0,0,0]

DFN.add_fracture_family(shape="ell",
                        distribution="tpl",
                        kappa=10.0,
                        aspect=2,
                        beta_distribution=1,
                        beta=45.0,
                        theta=0.0,
                        phi=0.0,
                        alpha=1.8,
                        min_radius=1.0,
                        max_radius=5.0,
                        p32=0.5, 
                        hy_variable = 'transmissivity',
                        hy_function = 'log-normal',
                        hy_params = {"mu":1e-13, "sigma":1.2})

DFN.add_fracture_family(shape="ell",
                        distribution="tpl",
                        kappa=10.0,
                        aspect=2,
                        beta_distribution=1,
                        beta=0.0,
                        theta=90.0,
                        phi=45.0,
                        alpha=1.8,
                        min_radius=1.0,
                        max_radius=5.0,
                        p32=0.5,
                        hy_variable = 'transmissivity',
                        hy_function = 'log-normal',
                        hy_params = {"mu":1e-13, "sigma":1.2})

DFN.print_family_information(1)

DFN.make_working_directory(delete=True)

DFN.check_input()

for key in DFN.params.keys():
    print(key, DFN.params[key]['value'])

# define_paths()
DFN.create_network()
# DFN.output_report()
DFN.mesh_network(coarse_factor=10)

DFN.dfn_flow()
DFN.dfn_trans()