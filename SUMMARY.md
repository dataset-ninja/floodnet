**FloodNet: A High Resolution Aerial Imagery Dataset for Post Flood Scene Understanding** is a dataset for semantic segmentation tasks. It is used in the Search and Rescue (SAR) and environmental industries.

The dataset consists of 2343 images with 1488 labeled objects belonging to 10 different classes including *Grass*, *Tree*, *Road-non-flooded*, and other: *Water*, *Building-non-flooded*, *Vehicle*, *Pool*, *Road-flooded*, *Building-flooded*, and *Background*.

Images in the FloodNet (Track 1) dataset have pixel-level semantic segmentation annotations. Due to the nature of the semantic segmentation task, it can be automatically transformed into an object detection (bounding boxes for every object) task. There are 1945 (83% of the total) unlabeled images (i.e. without annotations). There are 3 splits in the dataset: *Test* (448 images), *Train* (1445 images), and *Validation* (450 images). The dataset was released in 2020 by the [UMBC, USA](https://umbc.edu/), [Texas A&M University](https://www.tamu.edu/), and [Dewberry, USA](https://www.dewberry.com/).

Here are the visualized examples for each of the 10 classes:

[Dataset classes](https://github.com/dataset-ninja/floodnet/raw/main/visualizations/classes_preview.webm)
