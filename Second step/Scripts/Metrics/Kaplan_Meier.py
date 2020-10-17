from lifelines import KaplanMeierFitter
import pandas as pd
from matplotlib import pyplot as plt
import glob
from lifelines.statistics import multivariate_logrank_test
from pylab import text
import warnings
warnings.filterwarnings("ignore")

SACRIFICE_TIME_FILE_PATH = '../../Mice Sacrafice Time.xlsx'
SACRIFICE_DF = pd.read_excel(SACRIFICE_TIME_FILE_PATH)
SACRIFICE_DF.head()

files = glob.glob('../../image clusters/standard scaler/Mouse Aggregation/*.csv')
files.extend(glob.glob('../../image clusters/minmax scaler/Mouse Aggregation/*.csv'))


def kaplan_meier_calc(file_path: str) -> None:
    print(file_path)
    mouse_cluster_df = pd.read_csv(file_path)
    df = pd.merge(mouse_cluster_df, SACRIFICE_DF,on='Mouse #')

    file_name = file_path.split('/')[-1].split('.')[0]
    scaling_type = file_path.split('/')[-3]
    save_name = f'{scaling_type}: {file_name}'

    fig, axs = plt.subplots(3, 3, figsize=(15, 15))

    kmf = KaplanMeierFitter()

    fig.suptitle(save_name, fontsize=20)
    for k in range(2,11):
        ax = axs[int((k-2)/3), (k-2) % 3]
        ax.set_title(f'K={k}')
        for name, grouped_df in df.groupby(f'K={k}'):
            kmf.fit(grouped_df["Month"], grouped_df["Event"], label=name)
            kmf.plot(ax=ax)
        results = multivariate_logrank_test(df.Month, df[f'K={k}'], df.Event, weightings='wilcoxon')
        text(0.2, 0.5, f'P-Value: {round(results.p_value,3)}', ha='center', va='center', transform=ax.transAxes)
    plt.savefig(f'{save_name}.png')


for file in files:
    kaplan_meier_calc(file)