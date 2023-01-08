import os

import pandas
from matplotlib import pyplot

class Plot:

    def __init__(self, stat_dir):
        self.stat_dir = stat_dir
        classes = [i.strip(".csv") for i in os.listdir(stat_dir)]
        print(classes)
        self.data_dict = {}
        for class_ in classes:
            mean = [list(i) for i in pandas.read_csv(
                f"{self.stat_dir}/{class_}.csv",
                index_col=0
            )[["mean", "median"]].values]
            print(mean)
            self.data_dict[class_] = mean

    def visualize(self):
        for key, data in self.data_dict.items():
            pyplot.scatter(data[0], data[1], label=key, marker="o")
        pyplot.axis([0,256,0,256])
        pyplot.ylabel("medyan")
        pyplot.xlabel("ortalama")
        pyplot.title("Dağılım")
        pyplot.show()


def main():
    vis = Plot("./general_statistics/gray")
    vis.visualize()


if __name__ == '__main__':
    main()

