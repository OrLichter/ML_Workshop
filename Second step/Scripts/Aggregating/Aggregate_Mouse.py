import pandas as pd
import glob
import os

# SET UP
MOUSE_DATA = pd.read_excel('aMet.xlsx')
OUTPUT_FOLDER = 'Second step/image clusters/minmax scaler/Mouse Aggregation'
DATA_FOLDER = 'Second step/image clusters/minmax scaler'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


def aggregate_up(aggregate_column: str, pathces_df: pd.DataFrame, mouse_data: pd.DataFrame = MOUSE_DATA) -> pd.DataFrame:
    columns2keep = list(pathces_df.columns)
    columns2keep.append(aggregate_column)
    columns2keep.remove('Image')
    columns2keep.remove('Unnamed: 0')
    print(columns2keep)
    joint_df = pd.merge(pathces_df, mouse_data, left_on='Image', right_on='Scan ')[columns2keep]

    return joint_df.groupby(aggregate_column).agg(lambda x:x.value_counts().index[0])


def main():
    for file in glob.glob(f'{DATA_FOLDER}/*.csv'):
        patches = pd.read_csv(file)
        file_name = file.split('/')[-1]
        print(file_name)
        aggregate_up('Mouse #', patches).to_csv(f'{OUTPUT_FOLDER}/{file_name}')


main()