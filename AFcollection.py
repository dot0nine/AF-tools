
import os,re
import pandas as pd
from datafiles_opener import *
import numpy as np

class AF_Collection(object):
    def __init__(self):
        self._dir = os.getcwd()
        self.models = {}

    def set_dir(self, _dir):
        self._dir = _dir

    def get_data(self):
        return self.models

    def get_stat_par(self, x):
        return [np.average(x), np.std(x), np.var(x), np.median(x)]

    def import_af_run(self, _dir):
        self.set_dir(_dir)
        f_extension = ".json"
        # _encoding = 'ansi'
        # delimeters = ''

        subdirs = [x[0] for x in os.walk(self._dir)][1:]  #  exclude the root folder
        for sd in subdirs:
            print(sd)
        for sd in subdirs:
            model = sd.split('\\')[-1][:-7]
            print('Model\t', model)
            self.models[model] = {'pLDDT': [], 'pAE': [], 'rank': [], 'model_num': [], 'ylim_pLDDT': [0, 100], 'ylim_pAE': [0,30]}  # to get rid of .result ending

            json_files = open_files(full_path=sd, _filter='*' + f_extension)
            for f in json_files:
                if re.match(model + '_unrelaxed_rank_\d+_model_\d+_scores', f):
                    # print('File', f)

                    pLDDT, pAE = self.scores(f'{sd}\\{f}')
                    # print()
                    rank_n, model_n = self.extract_rank_model_n(f, model)
                    # print('Pars\t', (pLDDT, pAE, rank_n, model_n))
                    for k, v in zip(('pLDDT', 'pAE', 'rank', 'model_num'), (pLDDT, pAE, rank_n, model_n)):
                        self.models[model][k].append(v)

                # print(self.models.keys())
            self.models[model]['pLDDT_av'] = np.mean(self.models[model]['pLDDT'])
            self.models[model]['pLDDT_best'] = max(self.models[model]['pLDDT'])
            self.models[model]['pAE_av'] = np.mean(self.models[model]['pAE'])
            self.models[model]['pAE_best'] = min(self.models[model]['pAE'])

    # def output_analysis(self, model):
    #     data = self.get_data()[model]
    #     pars = ['pLDDT', 'pAE']
    #     par_dict = {}
    #     for p, yl in zip(pars, [(0, 100), (0, 30)]):
    #         par_dict[p] = {'dataset': data[p], 'ylim': yl, f'{p}_best': data[ f'{p}_best']}
    #         self.models[model] {'dataset': data[p], 'ylim': yl, f'{p}_best': data[ f'{p}_best']}
    #         for k, v in  zip(['av', 'std', 'var', 'med'], self.get_stat_par(data[p])):
    #             par_dict[p][k] = v
    #
    #     for k, v in zip(('ylim_pLDDT', 'ylim_pAE','av', 'std', 'var', 'med'), ()):


        # return par_dict




    def extract_rank_model_n(self, s, model):
        pattern = re.compile(model + '_unrelaxed_rank_(?P<rank_n>.*?)_model_(?P<model_n>.*?)_scores', re.VERBOSE)
        match = pattern.match(s)
        if match:
            rank_n = int(match.group("rank_n"))
            model_n = int(match.group("model_n"))
            return (rank_n, model_n)

        # return (name, n1, n2)

    # def set_scores(self, model, scores):
    #     self.models[model]['pLDDT'] = scores[0]
    #     self.models[model]['pAE'] = scores[1]

    # def pLDDT_score(self, file):
    #     dataframe = pd.read_json(file)
    #     pLDDT = dataframe.iloc[-60:, 2]
    #     return pLDDT

    def scores(self, file):
        # file = f'{model}_unrelaxed_rank_{model_num}.json'
        dataframe = pd.read_json(file)
        pLDDT = np.mean(dataframe.iloc[:,2])
        pAE = dataframe.iloc[:,1]
        pae_av_re = []
        for k in range(0, len(pAE)):
            pae_av_re.append(np.mean(pAE.iloc[k]))
        pAE = np.mean(pae_av_re)
        return (pLDDT, pAE)



