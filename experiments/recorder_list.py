import json
import copy
import pdb
import numpy as np
import pickle


def listify_mat(matrix):
    matrix = np.array(matrix).astype(str)
    if len(matrix.shape) > 1:
        matrix_list = []
        for row in matrix:
            try:
                matrix_list.append(list(row))
            except:
                pdb.set_trace()
        return matrix_list
    else:

        return list(matrix)


class Recorder():
    def __init__(self):
        self._traj, self._cur_traj = [], []
        return

    def pack_traj(self):
        self._traj.append(copy.deepcopy(self._cur_traj))
        self._cur_traj = []

        return

    def add(self, o, a, r, d):
        o = [listify_mat(obs) for obs in o]
        a = [listify_mat(act) for act in a]
        self._cur_traj.append((o, a, listify_mat(r), d))
        return

    def export_pickle(self, filename='traj'):
        if filename == '':
            raise ValueError('incorrect file name')
        traj = []
        for t in self._traj:
            # obs = np.array([tt[0] for tt in t]).astype(np.float32)
            # act = np.array([tt[1] for tt in t]).astype(np.float32)
            obs = ([tt[0] for tt in t])
            act = ([tt[1] for tt in t])
            rwd = np.array([tt[2] for tt in t]).astype(np.float32)
            done = np.array([tt[3] for tt in t])

            # pdb.set_trace()
            traj.append({
                'observations': obs[:-1],
                'next_observations': obs[1:],
                'actions': act[:-1],
                'rewards': rwd[:-1],
                'terminals': done[:-1]
            })
        with open('{}.pkl'.format(filename), 'wb') as outfile:
            pickle.dump(traj, outfile)
        return

    def export(self, filename='traj'):
        if filename == '':
            raise ValueError('incorrect file name')
        traj = {'traj': []}
        for t in self._traj:
            traj['traj'].append(t)
        # json.dumps(traj, sort_keys=True, indent=4)

        pdb.set_trace()

        with open('{}.json'.format(filename), 'w') as outfile:
            json.dump(traj, outfile)
        return