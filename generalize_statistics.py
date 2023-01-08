import os

import pandas


class Generalizer:

    def __init__(self, stat_dir, general_dir):
        self.file_list = os.listdir(stat_dir)
        self.stat_dir = stat_dir
        if general_dir.startswith("./"):
            self.general_dir = os.getcwd() + general_dir[1:]
        else:
            self.general_dir = general_dir
        buf = ""
        for _dir in self.general_dir.split("/")[1:]:
            buf += "/" + _dir
            try:
                os.mkdir(buf)
            except FileExistsError:
                continue

    def generalize(self, type_, class_):
        buffer = []
        for file in self.file_list:
            data = pandas.read_csv(
                f"{self.stat_dir}/{file}/{type_}/{class_}.csv",
                index_col=0
            )
            for value in data.values:
                buffer.append(list(value))
        return buffer

    def save(self, data, type_, class_):
        path = f"{self.general_dir}/{type_}"
        buf_dir = ""
        for dir_ in path.split("/")[1:]:
            buf_dir += "/" + dir_
            try:
                os.mkdir(buf_dir)
            except FileExistsError:
                pass
        print(data)
        print(f"saved <{class_}.csv> in | {path}")
        data.to_csv(f"{path}/{class_}.csv")

    def run(self):
        types = ["gray", "original"]
        classes = ["optic_area", "optic_disk", "other"]
        for type_ in types:
            for class_ in classes:
                data = pandas.DataFrame(
                    self.generalize(type_, class_),
                    columns=["file_path", "mean", "median"]
                )
                self.save(data, type_, class_)


def main():
    generalizer = Generalizer("./classification_statistics", "./general_statistics")
    generalizer.run()


if __name__ == '__main__':
    main()
