import os

import cv2
import numpy
import pandas


class PreProcessor:
    def __dir__(self):
        if "parse" in self.ds_dir:
            dir_list = []
        else:
            dir_list = ["resized", "gray_resized", "thresh_resized"]
        return dir_list

    def __init__(self, file_name: str, ds_dir: str, od_dir: str, thresh_val, thresh_ratio, image=None):
        self.file_name = file_name
        self.thresh_ratio = thresh_ratio
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
        if od_dir.startswith("./"):
            self.od_dir = os.getcwd() + od_dir[1:]
        else:
            self.od_dir = od_dir
        if image is not None:
            self.image = image
        else:
            self.image = cv2.imread(f"{self.od_dir}/{self.file_name}")
        if thresh_val == "auto":
            self.thresh_val = int((int(numpy.max(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)))
                                   - int(numpy.mean(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)))) * thresh_ratio) \
                              + int(numpy.mean(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)))
            print(self.thresh_val)
        else:
            self.thresh_val = thresh_val

    def _constructor(self, image, ds_dir):
        return PreProcessor(
            self.file_name, ds_dir, self.od_dir,
            self.thresh_val, self.thresh_ratio,
            image
        )

    @property
    def resized(self):
        ds_dir = f"{self.ds_dir}/resized/original"
        image = cv2.resize(self.image, (1000, 1000))
        return self._constructor(image, ds_dir)

    @property
    def gray(self):
        ds_dir = f"{self.ds_dir}/gray"
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return self._constructor(image, ds_dir)

    @property
    def gray_resized(self):
        ds_dir = f"{self.ds_dir}/resized/gray"
        image = cv2.cvtColor(self.resized.image, cv2.COLOR_BGRA2GRAY)
        return self._constructor(image, ds_dir)

    @property
    def thresh(self):
        ds_dir = f"{self.ds_dir}/thresh"
        _, thresh = cv2.threshold(
            self.gray.image, self.thresh_val,
            255, cv2.THRESH_BINARY
        )
        return self._constructor(thresh, ds_dir)

    @property
    def thresh_resized(self):
        ds_dir = f"{self.ds_dir}/resized/thresh"
        _, thresh = cv2.threshold(
            self.gray_resized.image, self.thresh_val,
            255, cv2.THRESH_BINARY
        )
        return self._constructor(thresh, ds_dir)

    @property
    def mean(self):
        if len(self.image.shape) == 3:
            return numpy.mean(self.gray.image)
        else:
            return numpy.mean(self.image)

    @property
    def median(self):
        if len(self.image.shape) == 3:
            return numpy.median(self.gray.image)
        else:
            return numpy.median(self.image)

    @property
    def stat(self):
        stat = [self.file_name, self.mean, self.median]
        return stat

    def parse(self, size=(230, 230), step=10):
        w, h = size
        h_count = 0
        index = 0
        while h_count + h <= self.image.shape[0]:
            w_count = 0
            while w_count + w <= self.image.shape[1]:
                image = self.image[h_count: h_count + h, w_count: w_count + w]
                ds_dir = f"{self.ds_dir}/parse/{self.file_name.strip('.jpg')}"
                filename = f"{index}.jpg"
                yield PreProcessor(
                    file_name=filename, ds_dir=ds_dir, od_dir=self.od_dir,
                    thresh_val=self.thresh_val, thresh_ratio=self.thresh_ratio,
                    image=image
                )
                w_count += step
                index += 1
            h_count += step

    def statistic(self):
        return [f"{self.ds_dir}/{self.file_name}", int(self.mean), int(self.median)]

    def save(self):
        print(f"saved: <{self.file_name}> in {self.ds_dir}")
        buf = "/"
        for _dir in self.ds_dir.split("/")[1:]:
            buf = buf + _dir + "/"
            try:
                os.mkdir(buf)
            except FileExistsError:
                continue
        path = f"{self.ds_dir}/{self.file_name}"
        cv2.imwrite(path, self.image)

    def run(self, size=(230, 230), step=10):
        print("START PREPROCESS: ", self.file_name)
        print("#" * 150)
        for proc in dir(self):
            stat_dir = proc
            proc = self.__getattribute__(proc)
            stats = [proc.statistic()]
            stats.extend(proc.run_parser())
            proc.save()
            self.write_statistics(stats, stat_dir, self.file_name.strip(".jpg"))

    def run_parser(self, size=(230, 230), step=10):
        print("RUN PARSE: ", self.ds_dir + self.file_name)
        print("#" * 150)
        stats = []
        parser = enumerate(self.parse(size, step))
        for index, parsed in parser:
            parsed.save()
            stats.append(parsed.statistic())
        return stats

    def write_statistics(self, statistic: list[str, int, int], stat_dir: str, file: str):
        df = pandas.DataFrame(statistic, columns=["file_path", "mean", "median"])
        stat_dir = self.ds_dir + "/statistics/" + stat_dir
        buf = ""
        for _dir in stat_dir.split("/")[1:]:
            try:
                buf += "/" + _dir
                os.mkdir(buf)
            except FileExistsError:
                continue
        df.to_csv(stat_dir + f"/{file}.csv")
        print(df)


class PreProcessorList:

    def __init__(self, ds_dir, od_dir, thresh, thresh_ratio):
        self.filenames = os.listdir(od_dir)
        self.ds_dir = ds_dir
        self.od_dir = od_dir
        self.index = 0
        self.thresh = thresh
        self.thresh_ratio = thresh_ratio

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.filenames):
            image = PreProcessor(
                file_name=self.filenames[self.index],
                ds_dir=self.ds_dir,
                od_dir=self.od_dir,
                thresh_val=self.thresh,
                thresh_ratio=self.thresh_ratio
            )
            self.index += 1
            return image
        else:
            raise StopIteration

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, item):
        if item < len(self.filenames):
            image = PreProcessor(
                file_name=self.filenames[self.index],
                ds_dir=self.ds_dir,
                od_dir=self.od_dir,
                thresh_val=self.thresh,
                thresh_ratio=self.thresh_ratio
            )
            return image
        else:
            raise IndexError


def main():
    image_list = PreProcessorList(
        ds_dir="./dataset",
        od_dir="./original",
        thresh="auto"
    )
    for image in image_list:
        image.run()
    """image_list = PreProcessorList(
        ds_dir="/media/freven/BOLAY/AlHazen/dataset/patient",
        od_dir="/media/freven/BOLAY/AlHazen/original/patient",
        thresh="auto"
    )
    for image in image_list:
        image.run()"""


if __name__ == '__main__':
    main()
