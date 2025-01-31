Dataset **FloodNet 2021: Track 1** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzEyMzhfRmxvb2ROZXQgMjAyMTogVHJhY2sgMS9mbG9vZG5ldC0yMDIxOi10cmFjay0xLURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogInoxeFRSYmlGZ3Z4UjRkNlhVZlNUMy90U1hZbWNacG5scmNBc0JybnJNdVk9In0=)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='FloodNet 2021: Track 1', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://drive.google.com/drive/folders/1sZZMJkbqJNbHgebKvHzcXYZHJd6ss4tH).