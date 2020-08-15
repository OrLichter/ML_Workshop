#!/usr/bin/env python
# coding: utf-8

# In[58]:


import glob
import pandas as pd
import os


def calculate_and_save(file_list, output, calc_type='mean', verbose=True, save=False):
    dataframes = []
    for file in file_list:
        if verbose:
            print(f"Loading {file}")
        df = pd.read_csv(file, sep="\t")
        dataframes.append(df)
    if verbose:
        print("Concatenating")
    concatenated_df = pd.concat(dataframes, axis=0)
    if verbose:
        print(f"Calculating mean for {concatenated_df.shape[0]} rows")
    if calc_type == 'mean':
        calculated_vec = concatenated_df.mean(axis=0)
    if calc_type == 'sum':
        calculated_vec = concatenated_df.sum(axis=0)
    try:
        calculated_vec = pd.concat([concatenated_df.iloc[1,:5], calculated_vec])
        if save:
            calculated_vec.to_csv(output)
            print(f'Saved {output}')
            return
        else:
            print(f"Returning {output}")
            return calculated_vec.to_frame().T
    except:
        # This happens if no cells were extracted i.e. text file is almost empty
        return None


def create_mean_data_per_series(base_dir='ROI features', output_dir='Averaged Features'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for slide in glob.glob(f"{base_dir}/*"):
        for series in glob.glob(f"{slide}/*"):
            slide_name = slide.rsplit('/', 1)[-1]
            series_name = series.rsplit('/', 1)[-1]
            output = f'{output_dir}/{slide_name}_{series_name}.csv'
            calculate_and_save(glob.glob(f"{series}/*.txt"), output, verbose=True)

            
def create_mean_data_per_slide(base_dir='ROI features', output_dir='Averaged Features'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for slide in glob.glob(f"{base_dir}/*"):
        file_list = []
        for series in glob.glob(f"{slide}/*"):
            file_list.append(glob.glob(f"{series}/*.txt"))
        slide_name = slide.rsplit('/', 1)[-1]
        output = f'{output_dir}/{slide_name}.csv'
        calculate_and_save(file_list, output)
        
    

def create_mean_data_per_image(base_dir='ROI features', output_dir='Averaged Features',save=True):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    final_df = None
    for slide in glob.glob(f"{base_dir}/*"):
        dataframes = []
        for series in glob.glob(f"{slide}/*"):
            for image in glob.glob(f"{series}/*.txt"):
                slide_name = slide.rsplit('/', 1)[-1]
                series_name = series.rsplit('/', 1)[-1]
                image_name = image.rsplit('/', 1)[-1].rsplit('_',1)[-1].rsplit('.',1)[0]
                output = f'{output_dir}/{slide_name}_{series_name}_{image_name}.csv'
                mean_vec = calculate_and_save([image], output,save=save)
                if not save:
                    if final_df is None:
                        final_df = mean_vec
                    elif mean_vec is not None and mean_vec.shape == (1,1483):                        
                        final_df = pd.concat([final_df, mean_vec])
                    else:
                        print(f"Ignored {output} due to some error")
    return final_df


def create_mean_data_per_image_one_dir(base_dir='ROI features', output_dir='Averaged Features', save=True, calc_type='mean'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    final_df = None
    counter = 0
    for image in glob.glob(f"{base_dir}/*.txt"):
        counter +=1
        print(counter)
        output = f"{output_dir}/{image.split('/')[-1]}_{calc_type}.csv"
        mean_vec = calculate_and_save([image], output, save=save, calc_type=calc_type, verbose=False)
        if not save:
            if final_df is None:
                final_df = mean_vec
            elif mean_vec is not None:
                final_df = pd.concat([final_df, mean_vec])
            else:
                print(f"Ignored {output} due to some error")
    return final_df

calc_type = 'sum'
final_df = create_mean_data_per_image_one_dir("../../Ayman's Data", output_dir="Ayman's Data Output", calc_type=calc_type, save=False)
final_df.to_csv(f"Ayman's Data Output/all_{calc_type}.csv")
