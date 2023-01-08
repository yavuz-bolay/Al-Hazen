from .preprocess import PreProcessorList
from .classification import ClassificatorList
from .generalize_statistics import Generalizer
from .data_visualization import Plot


class Run:

    def __init__(self, od_dir, ds_dir, thresh, thresh_ratio, detect_val=0.85):
        self.ds_dir = ds_dir
        self.od_dir = od_dir
        self.detect_val = detect_val
        self.preprocessor = PreProcessorList(ds_dir, od_dir, thresh, thresh_ratio)

    def run(self):
        print("RUN PREPROCESSOR")
        print("."*200)
        """for image in self.preprocessor:
            image.run()"""

        print("RUN CLASSIFICATOR")
        print("." * 200)
        classificator_list = ClassificatorList(
            self.ds_dir + "/statistics", self.od_dir,
            self.ds_dir + "/classificate",
            self.ds_dir + "/classificate/statistics", self.detect_val
        )

        for classificator in classificator_list:
            classificator.run()

        """print("RUN GENERALIZER")
        print("." * 200)
        generalizer = Generalizer(
            self.ds_dir + "/classificate/statistics",
            self.ds_dir + "/classificate/statistics/general"
        )
        generalizer.run()

        print("RUN VISUALIZER")
        print("." * 200)
        visualizer = Plot(self.ds_dir + "/classificate/statistics/general")
        sure = input("PROCESS FINISHED, DO YOU WANT TO SEE DATA VISULAIZE? (y/n)")
        if sure in "yY":
            visualizer.visualize()
        return visualizer"""

