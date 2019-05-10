from pathlib import Path

DIR_DATA_ROOT = Path('data')

DIR_MAGNITUDE_MODELS = DIR_DATA_ROOT / 'models'
DIR_W2V_MODELS = DIR_DATA_ROOT / 'w2v'

FILEPATH_PATH_CONFIG = Path('config.json')
FILEPATH_DATA_PICKLED = DIR_DATA_ROOT / 'data'
FILEPATH_W2V_MODEL = lambda epochs, size: DIR_W2V_MODELS / f'w2v_e{epochs}_s{size}.model'
FILEPATH_CORPUS = DIR_DATA_ROOT / 'corpus.txt'
FILEPATH_RAW_DATASET = DIR_DATA_ROOT / 'spotify_dataset.csv'
FILEPATH_DATASET = DIR_DATA_ROOT / 'dataset.csv'
