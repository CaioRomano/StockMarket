from App.libs.libs import ABC, abstractmethod


class ModelSkeleton(ABC):
    """
    Classe Abstrata responsável por criar um modelo para outras classes
    """

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def create_model(self):
        pass

    @abstractmethod
    def run_model(self):
        pass

    @abstractmethod
    def get_stats_model(self):
        pass
