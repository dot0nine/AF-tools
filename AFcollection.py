
import os,re
import pandas as pd
from datafiles_opener import *
import numpy as np

class AF_Collection(object):
    def __init__(self):
        self._dir = os.getcwd()
        self.proteins = {}

    def set_dir(self, _dir):
        self._dir = _dir

    def get_data(self):
        return self.proteins

    def get_stat_par(self, x):
        return {'av': np.average(x), 'std': np.std(x), 'var': np.var(x), 'med': np.median(x), 'max': np.maximum(x)}

    def import_af_run(self, _dir):
        self.set_dir(_dir)
        f_extension = ".json"
        # _encoding = 'ansi'
        # delimeters = ''

        subdirs = [x[0] for x in os.walk(self._dir)][1:]  #  exclude the root folder
        for count, sd in enumerate(subdirs):
            # print(sd)
            self.proteins[count] = {'Protein': '', 'pLDDT': [], 'pAE': [], 'rank': [], 'model_num': [], 'ylim_pLDDT': [0, 100], 'ylim_pAE': [0,30]}  # to get rid of .result ending

            json_files = open_files(full_path=sd, _filter='*' + f_extension)
            for f in json_files:
#                if re.match('\w+_unrelaxed_rank_\d+_model_\d+_scores', f):
                if re.search('scores_rank_\d+_alphafold2_\w+_model_\d+', f):
                    run = re.split('scores_rank_\d+_alphafold2_\w+_model_\d+', f)[0][:-1]
                    prot  = []
                    # print(run)
                    for i in run.split('_'):
                        # print(i)
                        prot.append(i)
                        if re.match('(\w+)?x\d+', i):
                            # print('yo')
                            # print(int(i.split('x')[-1]))
                            self.proteins[count]['Oligo state'] = int(i.split('x')[-1])
                            break

                    prot = '_'.join(prot)

                    for k, v in self.get_data().items():
                        if 'Oligo state' not in v:
                            v['Oligo state'] = 1


                    # print('prot\t', prot)
                    # print('File', f)
                    self.proteins[count]['Protein'] = prot
                    pLDDT, pAE = self.scores(f'{sd}\\{f}')

                    rank_n, model_n = self.extract_rank_model_n(f, run)
                    # print('Pars\t', (pLDDT, pAE, rank_n, model_n))
                    for k, v in zip(('pLDDT', 'pAE', 'rank', 'model_num'), (pLDDT, pAE, rank_n, model_n)):
                        self.proteins[count][k].append(v)

                # print(self.proteins.keys())
            self.proteins[count]['pLDDT_av'] = np.mean(self.proteins[count]['pLDDT'])
            self.proteins[count]['pLDDT_best'] = max(self.proteins[count]['pLDDT'])
            self.proteins[count]['pAE_av'] = np.mean(self.proteins[count]['pAE'])
            self.proteins[count]['pAE_best'] = min(self.proteins[count]['pAE'])

    # def output_analysis(self, prot):
    #     data = self.get_data()[prot]
    #     pars = ['pLDDT', 'pAE']
    #     par_dict = {}
    #     for p, yl in zip(pars, [(0, 100), (0, 30)]):
    #         par_dict[p] = {'dataset': data[p], 'ylim': yl, f'{p}_best': data[ f'{p}_best']}
    #         self.proteins[prot] {'dataset': data[p], 'ylim': yl, f'{p}_best': data[ f'{p}_best']}
    #         for k, v in  zip(['av', 'std', 'var', 'med'], self.get_stat_par(data[p])):
    #             par_dict[p][k] = v
    #
    #     for k, v in zip(('ylim_pLDDT', 'ylim_pAE','av', 'std', 'var', 'med'), ()):


        # return par_dict




    def extract_rank_model_n(self, s, prot):
        # pattern = re.compile(prot + '_unrelaxed_rank_(?P<rank_n>.*?)_model_(?P<model_n>.*?)_scores', re.VERBOSE)
        pattern = re.compile(prot + '_scores_rank_(?P<rank_n>.*?)_alphafold2_\w+_model_(?P<model_n>.*?)_seed_\d+', re.VERBOSE)
        match = pattern.match(s)
        if match:
            rank_n = int(match.group("rank_n"))
            model_n = int(match.group("model_n"))
            return (rank_n, model_n)

        # return (name, n1, n2)

    # def set_scores(self, prot, scores):
    #     self.proteins[prot]['pLDDT'] = scores[0]
    #     self.proteins[prot]['pAE'] = scores[1]

    # def pLDDT_score(self, file):
    #     dataframe = pd.read_json(file)
    #     pLDDT = dataframe.iloc[-60:, 2]
    #     return pLDDT

    def scores(self, file):
        # file = f'{prot}_unrelaxed_rank_{model_num}.json'
        dataframe = pd.read_json(file)
        pLDDT = np.mean(dataframe['plddt']) #.iloc[:,2])
        pAE = dataframe['pae']  # .iloc[:,1]
        pae_av_re = []
        for k in range(0, len(pAE)):
            pae_av_re.append(np.mean(pAE.iloc[k]))
        pAE = np.mean(pae_av_re)
        return (pLDDT, pAE)



