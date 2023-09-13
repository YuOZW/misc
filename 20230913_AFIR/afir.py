# based on geomeTRIC v1.0.1
# install geomeTRIC from pip
# pip install geomeTRIC

import os
import sys
import shutil
import traceback
from copy import deepcopy
import numpy as np
from scipy.spatial import distance

from geometric.nifty import kj2au, ang2bohr
eps = 1.0061 * kj2au
R0 = 3.8164 * ang2bohr
accum_max_force = 500.0   # in kJ / mol
path_step_size = 0.1       # in Angstrom

from mendeleev.fetch import fetch_table
df_element = fetch_table('elements')
df_covalent = df_element[['covalent_radius_pyykko']] / 100 * ang2bohr
df_covalent.index = df_element['symbol']
df_covalent = df_covalent.to_dict()['covalent_radius_pyykko']

from pysisyphus.trj import get_geoms, dump_geoms, standardize_geoms

def calc_omega(elem1, elem2, r_12):
    R1 = df_covalent[elem1]
    R2 = df_covalent[elem2]
    _omega = (R1 + R2) / r_12
    return _omega ** 6

class artificial_force:
    def __init__(self):
        self.atom1 = 0
        self.atom2 = 0
        self.rho = 1      # 1 (add) or -1 (break)
        self.gamma = 0.0  # in hartree
        self.alpha = 0.0  # in hartree / bohr
        self.method = 'AFIR'
    def calc_alpha(self):
        self.alpha = self.gamma / (2 ** (-1/6) - (1 + np.sqrt(1 + self.gamma / eps)) ** (-1/6)) / R0
    def _debug_print(self):
        print('atom1', self.atom1)
        print('atom2', self.atom2)
        print('rho', self.rho)
        print('alpha', self.alpha)
        print('gamma', self.gamma)
        print('method', self.method)
        print()

class checkpoint:
    def __init__(self):
        self.label = []
        self.geom = []
        self.af_list  = []
        self.pre_opt  = False
        self.path_opt = False
        self.ts_opt   = False

def main():

    cp = checkpoint()

    ### -----------------------------------------------------------------------------------------------------------
    ### STEP 1: read input file
    ### -----------------------------------------------------------------------------------------------------------

    def read_input():

        if len(sys.argv) < 2:
            raise RuntimeError("Input file is not specified")

        _fname = sys.argv[1]

        if not os.path.isfile(_fname):
            raise RuntimeError("Input file does not exist")

        with open(_fname, 'r') as _fin:
            _lines = _fin.readlines()

        _method = 'RADIAL'
        with open('_psi4.inp', 'w') as _fout:
            _read_geom = False
            _read_afir = False
            for _line in _lines:
                if 'molecule' in _line.lower() and '{' in _line:
                    _fout.write(f'{_line}')
                    _read_geom = True
                elif '}' in _line and _read_geom == True:
                    _fout.write(f'{_line}')
                    _read_geom = False
                elif _read_geom == True:
                    _items = _line.strip().split()
                    if len(_items) == 4:
                        _fout.write('%geometry\n')
                        cp.label.append(_items[0])
                        cp.geom.append([_items[1], _items[2], _items[3]])
                    else:
                        _fout.write(f'{_line}')
                elif 'afir' in _line.lower() and '{' in _line:
                    _fout.write(f'# {_line}')
                    _read_afir = True
                elif '}' in _line and _read_afir == True:
                    _fout.write(f'# {_line}')
                    _read_afir = False
                elif _read_afir == True:
                    _fout.write(f'# {_line}')
                    _items = _line.upper().strip().split()
                    if _items[0] == 'METHOD':
                        _method = _items[1]
                    elif _items[0] == 'ADD':
                        _af = artificial_force()
                        _af.atom1 = int(_items[1]) - 1
                        _af.atom2 = int(_items[2]) - 1
                        _af.rho = 1
                        _af.gamma = float(_items[3]) * kj2au # convert kJ/mol to hartree
                        _af.calc_alpha()
                        _af.method = _method
                        cp.af_list.append(_af)
                    elif _items[0] == 'BREAK':
                        _af = artificial_force()
                        _af.atom1 = int(_items[1]) - 1
                        _af.atom2 = int(_items[2]) - 1
                        _af.rho = -1
                        _af.gamma = float(_items[3]) * kj2au # convert kJ/mol to hartree
                        _af.calc_alpha()
                        _af.method = _method
                        cp.af_list.append(_af)
                    elif _items[0] == 'PRE_OPT':
                        if _items[1] == 'ON' or _items[1] == 'YES':
                            cp.pre_opt = True
                    elif _items[0] == 'PATH_OPT':
                        if _items[1] == 'ON' or _items[1] == 'YES':
                            cp.path_opt = True
                    elif _items[0] == 'TS_OPT':
                        if _items[1] == 'ON' or _items[1] == 'YES':
                            cp.ts_opt = True
                    else:
                        pass
                else:
                    _fout.write(f'{_line}')

            cp.geom = np.array(cp.geom, dtype=float) * ang2bohr

        ### end of the function ------------------------------------------------------------ ###

    read_input()

    ### -----------------------------------------------------------------------------------------------------------
    ### STEP 2: pre-optimization
    ### -----------------------------------------------------------------------------------------------------------

    def prepare_input(foutname):
        with open('_psi4.inp', 'r') as _fin:
            _lines = _fin.readlines()

        with open(foutname, 'w') as _fout:
            _read_geom = False
            for _line in _lines:
                if '%geometry' in _line:
                    _read_geom = True
                    continue
                if _read_geom == True:
                    for i, xyz in enumerate(cp.geom):
                        xyz = xyz / ang2bohr
                        _fout.write(f'{cp.label[i]} {xyz[0]} {xyz[1]} {xyz[2]}\n')
                    _read_geom = False
                else:
                    _fout.write(f'{_line}')

    def preopt():

        import geometric

        ### prepare input file ------------------------------------------------------------- ###

        prepare_input('_pre_opt.inp')

        ### prepare input arguments -------------------------------------------------------- ###

        _args = {}
        _args['input'] = '_pre_opt.inp'
        _args['engine'] = 'psi4'
        _args['coordsys'] = 'dlc'
        _args['trust'] = 1.0e-1
        _args['tmax'] =  3.0e-1
        _args['tmin'] =  1.0e-3
        _args['converge'] = [
            'energy', 1.0e-5,
            'grms',   1.7e-3,
            'gmax',   2.5e-3,
            'drms',   6.7e-3,
            'dmax',   1.0e-2,
            ]
        _args['maxiter'] = 100

        ### modified functions ------------------------------------------------------------- ###

        def calc_modified(self, coords, dirname, read_data=False, copydir=None):
            coord_hash = hash(coords.tobytes())
            if coord_hash in self.stored_calcs:
                result = self.stored_calcs[coord_hash]['result']
            else:
                read_success = False
                if read_data and os.path.exists(dirname) and hasattr(self, 'read_result'):
                    try:
                        result = self.read_result(dirname, check_coord=coords)
                        read_success = True
                        geometric.nifty.logger.info("Successfully read existing single-point result from %s\n" % dirname)
                    except (geometric.errors.EngineError, geometric.errors.CheckCoordError): pass
                if not read_success:
                    if copydir:
                        self.copy_scratch(copydir, dirname)
                    elif not os.path.exists(dirname): os.makedirs(dirname)
                    result = self.calc_new(coords, dirname)

                    ## Save structure ------------------------------------------------------- ##

                    _coords = coords.reshape(-1, 3)
                    cp.geom = deepcopy(_coords)
                    _E = result['energy']
                    with open('_pre_opt_final.xyz', 'w') as fout:
                        fout.write(f'{len(_coords)}\n')
                        fout.write(f'E = {_E}\n')
                        for j, xyz in enumerate(_coords):
                            fout.write(f'{self.M.elem[j]} {xyz[0] / ang2bohr} {xyz[1] / ang2bohr} {xyz[2] / ang2bohr}\n')

                self.stored_calcs[coord_hash] = {'coords':coords, 'result':result}

            return result

        ### modify functions --------------------------------------------------------------- ###

        geometric.engine.Engine.calc = calc_modified

        ### run optimization --------------------------------------------------------------- ###

        geometric.optimize.run_optimizer(**_args)

        ### end of the function ------------------------------------------------------------ ###

    if cp.pre_opt == True:
        preopt()


    ### -----------------------------------------------------------------------------------------------------------
    ### STEP 3: optimization with artificial force
    ### -----------------------------------------------------------------------------------------------------------

    def afir():

        import geometric

        ### prepare input file ------------------------------------------------------------- ###

        prepare_input('_afir.inp')

        ### prepare input arguments -------------------------------------------------------- ###

        _args = {}
        _args['input'] = '_afir.inp'
        _args['engine'] = 'psi4'
        _args['coordsys'] = 'cart'
        _args['trust'] = 2.0e-2
        _args['tmax'] =  6.0e-2
        _args['tmin'] =  1.0e-4
        _args['converge'] = [
            'energy', 1.0e-3,
            'grms',   1.0e-1,
            'gmax',   1.0e-1,
            'drms',   1.0e-2,
            'dmax',   1.0e-2,
            ]
        _args['maxiter'] = 100

        ### prepare output file ------------------------------------------------------------ ###

        with open('_afir_path.xyz', 'w') as _fout:
            pass

        ### modified functions ------------------------------------------------------------- ###

        def calc_modified(self, coords, dirname, read_data=False, copydir=None):
            coord_hash = hash(coords.tobytes())
            if coord_hash in self.stored_calcs:
                result = self.stored_calcs[coord_hash]['result']
            else:
                read_success = False
                if read_data and os.path.exists(dirname) and hasattr(self, 'read_result'):
                    try:
                        result = self.read_result(dirname, check_coord=coords)
                        read_success = True
                        geometric.nifty.logger.info("Successfully read existing single-point result from %s\n" % dirname)
                    except (geometric.errors.EngineError, geometric.errors.CheckCoordError): pass
                if not read_success:
                    if copydir:
                        self.copy_scratch(copydir, dirname)
                    elif not os.path.exists(dirname): os.makedirs(dirname)
                    result = self.calc_new(coords, dirname)

                    ## Add artifitial force ------------------------------------------------- ##

                    _coords = coords.reshape(-1, 3)
                    _gradient = result['gradient'].reshape(-1, 3)
                    _energy = 0.0
                    _force = np.zeros_like(_gradient)

                    _E = result['energy']
                    with open('_afir_path.xyz', 'a') as fout:
                        fout.write(f'{len(_coords)}\n')
                        fout.write(f'E = {_E}\n')
                        for j, xyz in enumerate(_coords):
                            xyz = xyz / ang2bohr
                            fout.write(f'{self.M.elem[j]} {xyz[0]} {xyz[1]} {xyz[2]}\n')

                    for _af in cp.af_list:

                        # method == 'AFIR' --------------------------------------------------- #

                        if _af.method == 'AFIR':
                            _vec_12 = _coords[_af.atom2] - _coords[_af.atom1]
                            _r_12 = np.linalg.norm(_vec_12)
                            _force[_af.atom1] = _force[_af.atom1]  + _af.rho * _af.alpha * _vec_12 / _r_12
                            _force[_af.atom2] = _force[_af.atom2]  - _af.rho * _af.alpha * _vec_12 / _r_12
                            _energy += _af.rho * _af.alpha * _r_12 * 2

                        # method == 'RADIAL' ------------------------------------------------- #
                    
                        elif _af.method == 'RADIAL':
                            _p = 2.0
                            _vec_12 = _coords[_af.atom2] - _coords[_af.atom1]
                            _r_12 = np.linalg.norm(_vec_12)
                            _R_1 = df_covalent[self.M.elem[_af.atom1]]
                            _R_2 = df_covalent[self.M.elem[_af.atom2]]
                            print(_coords[_af.atom1], _coords[_af.atom2], _gradient[_af.atom1], _gradient[_af.atom2]) # debug
                            for i in range(len(_coords)):
                                _R_i = df_covalent[self.M.elem[i]]

                                _r_1i = np.linalg.norm(_coords[i] - _coords[_af.atom1])
                                _omega_1i = ((_R_1 + _R_i) / (_r_1i + _R_1 + _R_i)) ** _p
                                _force[i] = _force[i]  + _af.rho * _af.alpha * _vec_12 / _r_12 * _omega_1i
                                _energy += _af.rho * _af.alpha * _r_12 * _omega_1i

                                _r_2i = np.linalg.norm(_coords[i] - _coords[_af.atom2])
                                _omega_2i = ((_R_2 + _R_i) / (_r_2i + _R_2 + _R_i)) ** _p
                                _force[i] = _force[i]  - _af.rho * _af.alpha * _vec_12 / _r_12 * _omega_2i
                                _energy += _af.rho * _af.alpha * _r_12 * _omega_2i

                        # -------------------------------------------------------------------- #

                    _gradient = _gradient - _force
                    result['energy'] = result['energy'] + _energy
                    result['gradient'] = _gradient.flatten()

                self.stored_calcs[coord_hash] = {'coords':coords, 'result':result}

            return result

        def optimizeGeometry_modified(self):
            """
            High-level optimization loop.
            This allows calcEnergyForce() to be separated from the rest of the codes
            """
            self.calcEnergyForce()
            self.prepareFirstStep()
            while self.state not in [geometric.optimize.OPT_STATE.CONVERGED, geometric.optimize.OPT_STATE.FAILED]:
                self.step()
                if self.state == geometric.optimize.OPT_STATE.NEEDS_EVALUATION:
                    self.calcEnergyForce()
                    self.evaluateStep()
                if self.recalcHess:
                    # If a Hessian recalculation is needed at this point, we need to
                    # call calcEnergyForce() which will compute the cartesian Hessian,
                    # convert it to IC, and then store it.
                    self.calcEnergyForce()

                ## Magnify force ------------------------------------------------------------ ##

                if self.state == geometric.optimize.OPT_STATE.CONVERGED:
                    reach_max_force = False
                    for i, _af in enumerate(cp.af_list):
                        cp.af_list[i].gamma = cp.af_list[i].gamma * 1.25
                        cp.af_list[i].calc_alpha()
                        cp.af_list[i]._debug_print()
                        if cp.af_list[i].gamma > accum_max_force:
                            reach_max_force = True
                    if reach_max_force == False:
                        self.state = geometric.optimize.OPT_STATE.NEEDS_EVALUATION

                ## -------------------------------------------------------------------------- ##

            if self.state == geometric.optimize.OPT_STATE.FAILED:
                raise geometric.errors.GeomOptNotConvergedError("Optimizer.optimizeGeometry() failed to converge.")
            # If we want to save the Hessian used by the optimizer (in Cartesian coordinates)
            if self.params.write_cart_hess:
                # One last Hessian update before writing it out
                self.UpdateHessian()
                geometric.nifty.logger.info("Saving current approximate Hessian (Cartesian coordinates) to %s" % self.params.write_cart_hess)
                Hx = self.IC.calcHessCart(self.X, self.G, self.H)
                np.savetxt(self.params.write_cart_hess, Hx, fmt='% 14.10f')
            if self.params.hessian in ['last', 'first+last', 'each']:
                Hx = geometric.normal_modes.calc_cartesian_hessian(self.X, self.molecule, self.engine, self.dirname, read_data=False, verbose=self.params.verbose)
                if self.params.frequency:
                    self.frequency_analysis(Hx, 'last', True)
            return self.progress

        ### modify functions --------------------------------------------------------------- ###

        geometric.engine.Engine.calc = calc_modified
        geometric.optimize.Optimizer.optimizeGeometry = optimizeGeometry_modified

        ### run optimization --------------------------------------------------------------- ###

        geometric.optimize.run_optimizer(**_args)

        ### end of the function ------------------------------------------------------------ ###

    #afir()


    ### -----------------------------------------------------------------------------------------------------------
    ### STEP 4: path optimization
    ### -----------------------------------------------------------------------------------------------------------

    def pathopt():

        import geometric

        ### prepare input file ------------------------------------------------------------- ###

        prepare_input('_path_opt.inp')


        with open('_afir_path.xyz', 'r') as _fin:
            _lines = _fin.readlines()

        with open('_path_init.trj', 'w') as _fout:
            pass

        _geom = []
        _distmat = None
        i = 0
        while True:
            if i >= len(_lines): break
            _line = _lines[i]
            i += 1
            if _line.strip().isnumeric() == False: break
            _natom = int(_line.strip())
            _line = _lines[i]
            i += 1
            _title = _line.strip()
            _label = []
            __geom = []
            for j in range(_natom):
                _line = _lines[i]
                i += 1
                _items = _line.strip().split()
                _label.append(_items[0])
                __geom.append([_items[1], _items[2], _items[3]])
            __geom = np.array(__geom, dtype=float) * ang2bohr
            __distmat = distance.cdist(__geom, __geom, metric='euclidean')
            if len(_geom) == 0:
                _geom.append(__geom)
                _distmat = deepcopy(__distmat)
            else:
                _diff = _distmat - __distmat
                _diff = _diff * _diff
                _rmse = np.sqrt(_diff.mean())
                if _rmse > 0.1:
                    _geom.append(__geom)
                    _distmat = deepcopy(__distmat)
                    with open('_path_init.trj', 'a') as _fout:
                        _fout.write(f'{_natom}\n')
                        _fout.write(f'{_title}\n')
                        for j in range(_natom):
                            _fout.write(f'{_label[j]} ')
                            _fout.write(f'{__geom[j][0] / ang2bohr} ')
                            _fout.write(f'{__geom[j][1] / ang2bohr} ')
                            _fout.write(f'{__geom[j][2] / ang2bohr}\n')

        ### prepare input file ------------------------------------------------------------- ###

        # 作成中

        _geom_kwargs = {}
        _geoms = get_geoms('_path_init.trj', coord_type='cart')
        _geoms = standardize_geoms(_geoms, 'cart', _geom_kwargs)

        _cos_kwargs = {}
        print(_geoms)


        ### prepare input arguments -------------------------------------------------------- ###

        _args = {}
        _args['input'] = '_path_opt.inp'
        _args['chain_coords'] = '_path_init.xyz'
        _args['engine'] = 'psi4'

    if cp.path_opt == True:
        pathopt()

    ### -----------------------------------------------------------------------------------------------------------
    ### STEP 5: TS optimization
    ### -----------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
