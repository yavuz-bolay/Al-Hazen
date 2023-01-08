import os
from shutil import copy

import pandas


class Classificator:
    thresh_dir = "/thresh_resized/"
    gray_dir = "/gray_resized/"
    original_dir = "/resized/"

    def __init__(self, file_no, stat_dir, ds_dir, cls_stat_dir, detect_val=0.85):
        self.file_no = file_no
        if ds_dir.startswith("./"):
            self.ds_dir = os.getcwd() + ds_dir[1:]
        else:
            self.ds_dir = ds_dir
        buf = ""
        for _dir in self.ds_dir.split("/")[1:]:
            buf += "/" + _dir
            try:
                os.mkdir(buf)
            except FileExistsError:
                continue
        if cls_stat_dir.startswith("./"):
            self.cls_stat_dir = os.getcwd() + cls_stat_dir[1:]
        else:
            self.cls_stat_dir = cls_stat_dir
        buf = ""
        for _dir in self.cls_stat_dir.split("/")[1:]:
            buf += "/" + _dir
            try:
                os.mkdir(buf)
            except FileExistsError:
                continue
        self.detect_val = detect_val
        self.thresh = pandas.read_csv(
            f"{stat_dir}{self.thresh_dir}{self.file_no}.csv",
            index_col=0
        ).drop(0, axis=0)
        self.original = pandas.read_csv(
            f"{stat_dir}{self.original_dir}{self.file_no}.csv",
            index_col=0
        ).drop(0, axis=0)
        self.gray = pandas.read_csv(
            f"{stat_dir}{self.gray_dir}{self.file_no}.csv",
            index_col=0
        ).drop(0, axis=0)
        self.__max = self.thresh["mean"].max()
        self.__mean = int(self.thresh["mean"].mean())
        self.optic_detector = int(
            (
                    (
                            self.__max - self.__mean
                    ) * self.detect_val
            ) + self.__mean
        )
        self.area_detector = int(
            self.__mean -
            (
                    self.__mean *
                    (1 - self.detect_val)
             )
        )

    def create_mask(self):
        masks = {
            "optic_disk":
                (self.thresh["mean"] <= self.__max)
                & (self.thresh["mean"] >= self.optic_detector),
            "optic_area":
                (self.thresh["mean"] < self.optic_detector)
                & (self.thresh["mean"] > self.area_detector),
            "other":
                (self.thresh["mean"] <= self.area_detector)
        }
        return masks

    def classificate(self, dataframe):
        masks = self.create_mask()
        classes = {}
        for _dir, mask in masks.items():
            classes[_dir] = dataframe[mask]
        return classes

    def run(self, gray=True, c_ful=True):
        print("START CLASSIFYING FOR :", self.file_no)
        print("^"*150)
        if gray:
            gray_dict = self.__run(self.gray, "gray")
            self.save_statistics("gray", gray_dict)
        if c_ful:
            original_dict = self.__run(self.original, "original")
            self.save_statistics("original", original_dict)
        return True

    def __run(self, dataframe, save_dir):
        data_cls = self.classificate(dataframe)
        data_dict = {}
        for _dir, files in data_cls.items():
            data = []
            new_path = self.ds_dir + "/" + save_dir \
                       + "/" + _dir \
                       + "/" + str(self.file_no) \
                       + "/"
            buf_dir = ""
            for dir_ in new_path.split("/")[1:-1]:
                buf_dir += "/" + dir_
                try:
                    os.mkdir(buf_dir)
                except FileExistsError:
                    pass
            for file in files.values:
                new_file = f"{file[0].split('/')[-1]}"
                file_path = new_path + new_file
                print(f"saved : <{new_file}> in | {new_path}")
                copy(file[0], file_path)
                data.append([file_path, file[1], file[2]])
            data = pandas.DataFrame(data, columns=["file_path", "mean", "median"])
            data_dict[_dir] = data
        return data_dict

    def save_statistics(self, type_, datadict):
        file_path = self.cls_stat_dir + f"/{self.file_no}/" + "{}"
        for name, data in datadict.items():
            path = file_path.format(type_)
            buf_dir = ""
            for _dir in path.split("/")[1:]:
                buf_dir += f"/{_dir}"
                try:
                    os.mkdir(buf_dir)
                except FileExistsError:
                    pass
            data.to_csv(path + f"/{name}.csv")
            print(f"saved <{name}.csv> in | {path}")
            print(data)
            print("/"*150)






class ClassificatorList:

    def __init__(self, stat_dir, od_dir, ds_dir, cls_stat_dir, detect_val):
        # int(i.strip(".jpg")) for i in os.listdir(od_dir)
        self.file_numbers = [91, 92, 93, 94, 95, 96, 97, 98, 99]
        self.stat_dir = stat_dir
        self.ds_dir = ds_dir
        self.detect_val = detect_val
        self.index = 0
        self.cls_stat_dir = cls_stat_dir

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.file_numbers):
            classificator = Classificator(
                self.file_numbers[self.index],
                self.stat_dir, self.ds_dir,
                self.cls_stat_dir, self.detect_val
            )
            self.index += 1
            return classificator
        else:
            raise StopIteration

def main():
    classificator = Classificator(1, "./dataset/statistics", "./dataset", "./classification_statistics", detect_val=0.9)
    print("area detector: ", classificator.area_detector)
    print("optic disk detector: ", classificator.optic_detector)
    classificator.run()
    print(classificator.cls_stat_dir)


if __name__ == '__main__':
    main()
