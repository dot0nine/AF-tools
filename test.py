import AFcollection
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import itertools
import pandas as pd
scapCC4 = AFcollection.AF_Collection()

scapCC4.import_af_run(r'C:\Users\lj21342\OneDrive - University of Bristol\Documents\01-Science\Computational\scapCC4\AF2\apCC4_x4 vs SC\\')
data_dict = scapCC4.get_data()
proteins = pd.DataFrame.from_dict(data_dict, orient='index')
# data_dict = {}
# for model in proteins:
#     data_dict[model] = scapCC4.output_analysis(model)
# data = pd.DataFrame.from_dict(data_dict)
print(proteins.columns)
fig1, axs = plt.subplots(1, 2)  # pLDDT and pAE
# sns.set_theme(style="ticks", palette="pastel")
axs = np.array(axs)  # https://www.pythonfixing.com/2021/10/fixed-python-subplot-used-to-show-one.html
fig1.suptitle('AF2 output', fontsize=16)
pars = ['pLDDT', 'pAE']
# par_dict = {}
# for p in pars:
#     par_dict = {'dataset':[], 'ylim':[], 'av': 0, 'std': 0, 'var': 0, 'med': 0}

# out_str = 'Protein\tpLDDT_av\tpLDDT_best\tpAE_av\tpAE_best\n'

for par, ax, yl in zip(pars, axs.flat, ((0, 100), (0, 30))):  # plot only the parameters from the list specified above
    ax.set_title(par, fontsize=14)
    # out_str += par + '\n'
    palette = itertools.cycle(sns.color_palette("Set2"))
    # for model in proteins:
    # data = scapCC4.output_analysis(model)
    #     ax.scatter()

    # print([scapCC4.output_analysis(model)[par]['dataset'] for model in proteins])
    # sns.boxplot(x=proteins.keys(), y=[scapCC4.output_analysis(model)[par]['dataset'] for model in proteins])
    # for x, y in zip(proteins.keys(), [scapCC4.output_analysis(model)[par]['dataset'] for model in proteins]):
    #     sns.barplot(x=x, y=y)
    # print(len(proteins['pLDDT_av']))
    # print(proteins.iloc[0])
    # print(proteins.iloc[0])
    # print(proteins['pLDDT_av'])
    # print(proteins[f'{par}'].index)
    # print(proteins[f'{par}'].values)

    sns.boxplot(proteins[f'{par}'], ax=ax)
    # print(proteins[par])
    # print(proteins['Protein'])
    #
    # sns.boxplot(y=par, x='Protein', data=proteins, ax=ax)

    # print(data_dict.keys())
    # print([data_dict[model][f'{par}'] for model in data_dict.keys()])
    # for model in data_dict.keys():
    #     sns.boxplot(x=data_dict.keys(), y=data_dict[model][f'{par}'], ax=ax)


    # sns.boxplot(x=proteins.iloc[0], y=proteins['pLDDT_av']) #, data=proteins)
    #ax.set_xtick(rotation=45)

        # for p in pars:
        # # pLDDT, pLDDT_av, pLDDT_best, pAE, pAE_av, pAE_best = [x for x in proteins[model].values()]
        # for k,v in zip([pLDDT, pLDDT_av, pLDDT_best, pAE, pAE_av, pAE_best])proteins[model].items():
        #     data = samples[s].get_surfaces()[par]['dataset']
        #     pLDDT_av, pLDDT_best, pAE_av, pAE_best = samples[s].get_stat_par(data)
        #     color = next(palette)
        #     out_str += f'{s}\t{pLDDT_av:.1f}\t{pLDDT_best:.1f}\t{pAE_av:.2f}\t{pAE_best:.2f}\n'
        #     label = f'{s}'
        #     sns.histplot(ax=ax, data=data, bins=101, binrange=samples[s].get_surfaces()[par]['xlim'], kde=True,
        #                  alpha=0.7, color=color, common_norm=False, line_kws={"lw": 3}, label=label, stat=stat)
        # out_str += '\n'
        # ax.set_xlim(samples[s].get_surfaces()[par]['xlim'])

    ax.set_ylim(yl)


plt.show()

