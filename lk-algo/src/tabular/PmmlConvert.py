from sklearn2pmml import PMMLPipeline, sklearn2pmml


class AlgoConverter:
    def __init__(self) -> None:
        self.pipeline = []

    def add_element(self, pipeline) -> None:
        self.pipeline = pipeline

    def export(self, path: str) -> None:
        pip = PMMLPipeline(self.pipeline)
        sklearn2pmml(pip, path + ".pmml", with_repr=True)
