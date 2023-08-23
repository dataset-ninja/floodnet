Dataset **FloodNet 2021 (Track 1)** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/D/F/sk/ng8BPmL4pAijbd4bBGU0lHD2QJtGPebGy8TpD1ej0BqTNIU3qGUFZ9tqrT6gpgHsPv0VIONthE6GwlnCLnBxGTRIgxd9QjVozJq3ICmAz5FpPSXC6SR8VXx5UNTj.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='FloodNet 2021 (Track 1)', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://drive.google.com/drive/folders/1sZZMJkbqJNbHgebKvHzcXYZHJd6ss4tH).