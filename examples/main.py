# -*- coding: utf-8 -*-
import sys,os
sys.path.append('./../pycmg/')
from generate_mesostructure import Mesostructure
from configuration import Configuration
from visualization import export_data, visualize_sections
import numpy as np

output_name = 'ab2_new_2'

vf_max_assembly_input = np.loadtxt(f'{output_name}_input_generated_vf_max.csv')

my_configuration = Configuration(vf_max_assembly=vf_max_assembly_input, average_shape=[1, 0.75, 0.75])
my_configuration.load_inclusions(conf_csv=f'{output_name}_input_generated.csv')
my_mesostructure = Mesostructure(mesostructure_size=[20, 20, 20], resolution=[0.1, 0.1, 0.1])
my_mesostructure.add_configuration(my_configuration)
my_virtual_mesostructure = my_mesostructure.assemble_sra()
np.save(f'{output_name}_mesostructure.npy', my_virtual_mesostructure)    # .npy extension is added if not given
visualize_sections(my_virtual_mesostructure, 3)
export_data(my_virtual_mesostructure, 'vtk', f'{output_name}_mesostructure.vti')
