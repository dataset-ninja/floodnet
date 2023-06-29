import os
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_name, get_file_name_with_ext
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)
        api.file.download(team_id, teamfiles_path, local_path)

        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                sly.logger.info(f"Downloading '{file_name_with_ext}'...")
                if not os.path.exists(local_path):
                    api.file.download(team_id, teamfiles_path, local_path)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
                sly.logger.info(f"Archive '{file_name_with_ext}' was unpacked successfully")
                sly.fs.silent_remove(local_path)

            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    objclasses = [
        sly.ObjClass("Background", sly.Bitmap),
        sly.ObjClass("Building-flooded", sly.Bitmap),
        sly.ObjClass("Building-non-flooded", sly.Bitmap),
        sly.ObjClass("Road-flooded", sly.Bitmap),
        sly.ObjClass("Road-non-flooded", sly.Bitmap),
        sly.ObjClass("Water", sly.Bitmap),
        sly.ObjClass("Tree", sly.Bitmap),
        sly.ObjClass("Vehicle", sly.Bitmap),
        sly.ObjClass("Pool", sly.Bitmap),
        sly.ObjClass("Grass", sly.Bitmap),
    ]
    idx_to_objclasses = {idx: cls for idx, cls in zip(range(10), objclasses)}

    tag_meta_ptg1 = sly.TagMeta("flooded", sly.TagValueType.NONE)
    tag_meta_ptg2 = sly.TagMeta("non-flooded", sly.TagValueType.NONE)

    folder_to_tag_meta = {
        "Labeled/Flooded": tag_meta_ptg1,
        "Labeled/Non-Flooded": tag_meta_ptg2,
    }

    # teamfiles_dir = "/4import/LoveDA/"

    labeled_dirname = "Labeled"
    unlabeled_dirname = "Unlabeled"
    flooded_dirname = "Flooded"
    nonflooded_dirname = "Non-Flooded"
    images_dirname = "image"
    masks_dirname = "mask"
    # dataset_path = download_dataset(teamfiles_dir)
    dataset_path = "./APP_DATA/FloodNet"
    mask_ext = "_lab.png"

    def _create_ann(image_path, ds_path, dirname):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        masks_dir = os.path.join(ds_path, dirname, masks_dirname)
        mask_path = os.path.join(masks_dir, get_file_name(image_path) + mask_ext)

        if not os.path.exists(mask_path):
            return sly.Annotation(img_size=(img_height, img_wight))
        ann_np = sly.imaging.image.read(mask_path)[:, :, 2]

        for i in np.unique(ann_np):
            if i == 0:
                continue
            obj_mask = ann_np == i
            curr_bitmap = sly.Bitmap(obj_mask)
            curr_obj_class = idx_to_objclasses[i]
            if curr_bitmap.area > 100:
                curr_label = sly.Label(curr_bitmap, curr_obj_class)
                labels.append(curr_label)

        tag = sly.Tag(meta=folder_to_tag_meta[dirname])
        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=[tag])

    def _process_images_and_annotations(ds, batch, ds_path, dirname, progress_cb):
        images_names = [os.path.basename(image_path) for image_path in batch]
        img_infos = api.image.upload_paths(ds.id, images_names, batch)

        anns_batch = [_create_ann(image_path, ds_path, dirname) for image_path in batch]
        img_ids = [im_info.id for im_info in img_infos]
        api.annotation.upload_anns(img_ids, anns_batch)

        progress_cb(len(batch))

    meta = sly.ProjectMeta(
        obj_classes=objclasses,
        tag_metas=list(folder_to_tag_meta.values()),
    )

    project = api.project.create(workspace_id, project_name)
    api.project.update_meta(project.id, meta.to_json())

    ds_names = os.listdir(dataset_path)
    for ds_name in ds_names:
        ds_path = os.path.join(dataset_path, ds_name)
        if os.path.isdir(ds_path):
            dataset = api.dataset.create(project.id, ds_name)
            if ds_name != "Train":
                img_dirpath = os.path.join(ds_path, images_dirname)
                all_images_path = [
                    os.path.join(img_dirpath, img_name) for img_name in os.listdir(img_dirpath)
                ]
                pbar = tqdm(desc=f"Processing '{ds_name}' dataset", total=len(all_images_path))
                for batch in sly.batched(all_images_path, batch_size=10):
                    images_names = [os.path.basename(image_path) for image_path in batch]
                    img_infos = api.image.upload_paths(dataset.id, images_names, batch)

                    pbar.update(len(batch))
            else:
                labeled_flooded_img_dir = os.path.join(
                    ds_path, labeled_dirname, flooded_dirname, images_dirname
                )
                labeled_nonflooded_img_dir = os.path.join(
                    ds_path, labeled_dirname, nonflooded_dirname, images_dirname
                )
                unlabeled_img_dir = os.path.join(ds_path, unlabeled_dirname, images_dirname)

                labeled_flooded_img_names = os.listdir(labeled_flooded_img_dir)
                labeled_nonflooded_img_names = os.listdir(labeled_nonflooded_img_dir)
                unlabeled_img_names = os.listdir(unlabeled_img_dir)

                labeled_flooded_images = [
                    os.path.join(labeled_flooded_img_dir, img_name)
                    for img_name in labeled_flooded_img_names
                ]
                labeled_nonflooded_images = [
                    os.path.join(labeled_nonflooded_img_dir, img_name)
                    for img_name in labeled_nonflooded_img_names
                ]
                unlabeled_images = [
                    os.path.join(unlabeled_img_dir, img_name) for img_name in unlabeled_img_names
                ]
                all_images_path = (
                    labeled_flooded_images + labeled_nonflooded_images + unlabeled_images
                )

                pbar = tqdm(desc=f"Processing '{ds_name}' dataset", total=len(all_images_path))
                for batch in sly.batched(labeled_flooded_images, batch_size=10):
                    _process_images_and_annotations(
                        dataset, batch, ds_path, f"{labeled_dirname}/{flooded_dirname}", pbar.update
                    )
                for batch in sly.batched(labeled_nonflooded_images, batch_size=10):
                    _process_images_and_annotations(
                        dataset,
                        batch,
                        ds_path,
                        f"{labeled_dirname}/{nonflooded_dirname}",
                        pbar.update,
                    )

                for batch in sly.batched(unlabeled_images, batch_size=10):
                    images_names = [os.path.basename(image_path) for image_path in batch]
                    img_infos = api.image.upload_paths(dataset.id, images_names, batch)

                    pbar.update(len(batch))

    return project
