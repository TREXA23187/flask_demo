import pandas
import os
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def read_dataset(target):
    dataset = pandas.read_csv(os.path.join(os.path.dirname(__file__), "..", "data/data.csv"))

    y = dataset[target]
    x = dataset.drop(target, axis=1)

    return x, y


def split_dataset(x, y):
    return train_test_split(x, y, test_size=0.3, random_state=0)


def train_dataset(x_train, y_train):
    clf = KNeighborsClassifier()
    clf.fit(x_train, y_train)

    return clf


def evaluate_classifier_model(classifier, x_test, y_test):
    y_pred = classifier.predict(x_test)
    y_score = classifier.predict_proba(x_test)

    # ------------ 1. Accuracy ------------ #
    accuracy = sklearn.metrics.accuracy_score(y_test, y_pred)
    recall = sklearn.metrics.recall_score(y_test, y_pred, average="micro")
    f1_score = sklearn.metrics.f1_score(y_test, y_pred, average="micro")
    confusion_matrix = sklearn.metrics.confusion_matrix(y_test, y_pred)

    return {
        "accuracy": accuracy,
        "recall": recall,
        "f1_score": f1_score,
        "confusion_matrix": confusion_matrix.tolist()
    }


def run():
    x, y = read_dataset("Species")
    x_train, x_test, y_train, y_test = split_dataset(x, y)
    model = train_dataset(x_train, y_train)
    evaluation = evaluate_classifier_model(model, x_test, y_test)

    return evaluation


if __name__ == '__main__':
    res = run()
    print(res)
