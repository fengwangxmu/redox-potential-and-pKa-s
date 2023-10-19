#!/usr/bin/env python3
import os
import ase
from ase.io import read, write
import numpy as np
import random as r

def xyz_to_npy(xyz, output_dir, idx=0, atoms_kind=0):
    if os.path.exists(output_dir):
        ats = read(xyz, '0')
        print(len(ats.get_chemical_symbols()))
        print('Files already exist!')
        return 
    else:    
        os.makedirs(output_dir)
        ats = read(xyz, ':')
        energies = np.array([at.get_potential_energy() for at in ats])
        forces = np.array([np.ravel(at.get_forces()) for at in ats])
        coords = np.array([np.ravel(at.get_positions()) for at in ats])
        numbers = [at.get_array('numbers') for at in ats]
        boxes = [at.get_cell().reshape(9) for at in ats]
        if atoms_kind == 0:
            symbol_set = set(ats[0].get_chemical_symbols())
        else:
            symbol_set = atoms_kind
        sym_dict = dict(zip(symbol_set, range(len(symbol_set))))
        type_raw = [str(sym_dict[specie]) for specie in ats[0].get_chemical_symbols()]
        idx = str(len([l for l in os.listdir(output_dir) if 'set'in l])).zfill(3)  
        os.makedirs(output_dir+'/set.'+idx)
        np.save(output_dir+'/set.'+idx+'/energy.npy', energies)
        np.save(output_dir+'/set.'+idx+'/force.npy', forces)
        np.save(output_dir+'/set.'+idx+'/coord.npy', coords)
        np.save(output_dir+'/set.'+idx+'/box.npy', boxes)
        with open(output_dir+'/type.raw', 'w') as f:
            f.write(' '.join(type_raw))
        print(len(ats))
        return 0
"""
cell = [14.217, 14.217, 14.217]
atoms = read("pos.xyz", "::1")
forces = read("frc.xyz", "::1")

for idx, atom in enumerate(atoms):
    atom.set_cell(cell)
    atom.set_pbc((True, True, True))
    atom.set_positions(atom.get_positions(wrap=True))
    atom.info['E'] = atom.info['E']*27.2114
    atom.set_array('force', forces[idx].get_positions() * 27.2114/0.52918)

write("2.xyz", atoms)
"""

import glob
concs = glob.glob("./*xyz")
concs.sort()

print(concs)
atoms_kind = [ 'O', 'H', 'C', "Na"]

for idx, conc in enumerate(concs):
    xyz_to_npy(xyz=conc, output_dir='system-0%02d'%(idx), atoms_kind=atoms_kind)
   

