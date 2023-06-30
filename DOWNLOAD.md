Dataset **FloodNet (Track 1)** can be downloaded in Supervisely format:

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/k/f/16/Xta6nyvvxvq7X3ZAfZrkaLwTlu6x5j4POkxruv16POvl3UhNutIgX6jw2c5ZahSbbjCCOJgxALCvMz3itxsSR4WeGHGHkS9mU0VKTNWl6VylhNLW8C7pV5Uep81b.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='FloodNet (Track 1)', dst_path='~/dtools/datasets/FloodNet (Track 1).tar')
```
The data in original format can be 🔗[downloaded here](https://drive.google.com/drive/folders/1sZZMJkbqJNbHgebKvHzcXYZHJd6ss4tH)