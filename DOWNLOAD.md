Dataset **FloodNet 2021: Track 1** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMTIzOF9GbG9vZE5ldCAyMDIxOiBUcmFjayAxL2Zsb29kbmV0LTIwMjE6LXRyYWNrLTEtRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiZ2FxZkorQ3dIU0R0U0srWFZwZGtjVWR5dHJGRVY5THgyUDVLVDV1RVdPdz0ifQ==?response-content-disposition=attachment%3B%20filename%3D%22floodnet-2021%3A-track-1-DatasetNinja.tar%22)

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