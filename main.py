import pickle
from pathlib import Path

import numpy as np
from sklearn.neural_network import MLPClassifier
from tqdm import tqdm

ABROCKYOU_TXT = "abrockyou.txt"
ABROCKYOU_MD5 = "abrockyou.md5"

MLP_MODEL_PATH = "mlp.pkl"

MEAN = 0xf / 2.
STD = (((0xf + 1) ** 2 - 1) / 12) ** 0.5


def read_hashes(file_path):
    hashes = []
    with open(file_path) as f:
        for line in tqdm(f, desc="Reading MD5 hashes from {}".format(file_path)):
            line = line.rstrip('\n')
            line_ints = [int(char_hex, base=16) for char_hex in line]
            hashes.append(line_ints)
    hashes = np.vstack(hashes)
    hashes = (hashes - MEAN) / STD
    return hashes


def split_train_test(train_rate=0.6):
    print("Splitting train / test ...")
    with open(ABROCKYOU_MD5) as f:
        hashes = f.readlines()
    with open(ABROCKYOU_TXT) as f:
        wordlist = f.readlines()
    assert len(wordlist) == len(hashes)
    indices = np.random.permutation(len(hashes))
    hashes = np.take(hashes, indices)
    wordlist = np.take(wordlist, indices)
    n_train = int(train_rate * len(wordlist))
    train_dir = Path("train")
    test_dir = Path("test")
    for fold_dir in (train_dir, test_dir):
        fold_dir.mkdir(exist_ok=True)
    for suffix, data in (('md5', hashes), ('txt', wordlist)):
        data_train, data_test = data[:n_train], data[n_train:]
        file_name = "abrockyou.{}".format(suffix)
        with open(train_dir / file_name, 'w') as f:
            f.writelines(data_train)
        with open(test_dir / file_name, 'w') as f:
            f.writelines(data_test)
    print("Split is completed.")


def read_xy(fold_name="train", n_take=float('inf')):
    fold_name = Path(fold_name)
    if not fold_name.exists():
        split_train_test()
    hashes = read_hashes(fold_name / ABROCKYOU_MD5)
    with open(fold_name / ABROCKYOU_TXT) as f:
        y = [line.startswith('a') for line in f]
    n_take = min(len(hashes), n_take)
    hashes = hashes[:n_take]
    y = y[:n_take]
    return hashes, y


def train():
    hashes, y = read_xy(fold_name="train")
    print("Training ...")
    mlp = MLPClassifier(hidden_layer_sizes=(100, 20), max_iter=200)
    mlp.fit(hashes, y)
    with open(MLP_MODEL_PATH, 'wb') as f:
        pickle.dump(mlp, f)


def test(test_fold="test"):
    with open(MLP_MODEL_PATH, 'rb') as f:
        mlp = pickle.load(f)
    hashes, y = read_xy(fold_name=test_fold)
    print("Testing ...")
    y_predicted = mlp.predict(hashes)
    accuracy = (y == y_predicted).mean()
    print("{fold_name} accuracy: {accur}".format(fold_name=test_fold, accur=accuracy))


if __name__ == '__main__':
    train()
    test(test_fold="train")
    test(test_fold="test")
