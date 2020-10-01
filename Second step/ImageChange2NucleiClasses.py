from PIL import Image, ImageDraw
import pandas as pd
from typing import Union, Optional
from GoogleDriveClass import GoogleClient
import os
from tqdm import tqdm

COLOR_DICT = {
    0: (0, 191, 255),
    1: (255, 235, 153),
    2: (255, 26, 26),
    3: (77, 184, 255),
    4: (191, 128, 64),
    5: (204, 204, 255),
    6: (204, 163, 0),
    7: (20, 31, 31),
    8: (153, 153, 153),
    9: (255, 204, 255),
}


def draw_circle(x: float, y: float, radius: int, color: int,  draw_object: ImageDraw.Draw) -> None:
    """

    Args:
        x: x coordinate of center
        y: y coordinate of center
        color: a number from 1 to 10 to represent the color of the circle.
        radius: the radius

    Returns:

    """
    draw_object.ellipse((x - radius, y - radius, x + radius, y + radius), fill=COLOR_DICT[color])

def get_concat_h(im1: Image, im2: Image) -> Image:
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def nuclei_by_group(image_path: str, csv_path: str, k: int, circle_radius: int=4,
                       output_path: Optional[str]=None, show: bool=True):
    original_image = Image.open(image_path)
    changed_image = Image.open(image_path)
    df = pd.read_csv(csv_path)
    draw = ImageDraw.Draw(changed_image)

    for index, row in df.iterrows():
        draw_circle(row['Centroid X px'], row['Centroid Y px'], circle_radius, row[f'K={k}'], draw)
    concatenated_image = get_concat_h(original_image, changed_image)
    if show:
        concatenated_image.show()
    if output_path:
        concatenated_image.save(output_path)
        print("Saved output_path")


def download_and_color_whole_slide(slide_name: str, k: int,output_folder: Optional[str]=None,
                                   images_folder: str='Normalized Images', data_folder: str='Kmean Mini Batch (Standard Scaler)'):
    """

    Args:
        slide_name: The name of the slide i.e MB16CC002
        k: the number of clusters
        output_folder: The folder to output all the files to. If left empty prints all results
        images_folder: The images folder in Google Drive
        data_folder: The data folder in Google Drive

    Returns:

    """
    def file_id_by_name(cluster_data_list: list, file_name: str):
        """
        searches cluster_data_list for a file that starts with file_name.

        Args:
            cluster_data_list: a list of file dictionaries in the format {'id':XXXX, 'name':XXXX}
            file_name: the name of the file

        Returns:
            the file's id from cluster data_list
        """
        for file_dict in cluster_data_list:
            if file_name in file_dict.get('name'):
                return file_dict.get('id')
        return None

    client = GoogleClient()
    slides = client.get_all_files(folder_name=images_folder, substring=slide_name)
    kmeans_data = client.get_all_files(folder_name=data_folder, substring=slide_name)
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for file_dict in tqdm(slides):
        slide_file_id, file_name = file_dict.values()
        data_file_id = file_id_by_name(kmeans_data, file_name[:-4])
        try:
            slide = client.download_file(slide_file_id)
            data = client.download_file(data_file_id)
            if output_folder:
                output_path = output_folder + '/' + file_name
                nuclei_by_group(slide, data, 4, output_path=output_path, show=False)
            else:
                nuclei_by_group(slide, data, 4)
            slide.close()
            data.close()
        except Exception:
            print(f"Could not find either data or slide for {file_name}")


download_and_color_whole_slide('MB16CC009', 4, output_folder='Outputs')