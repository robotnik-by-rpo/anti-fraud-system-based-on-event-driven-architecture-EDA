import torch
from torch import nn, optim
from torch.utils.data import Dataset
from pathlib import Path
from torchvision.transforms import v2 as transforms
import numpy as np
from typing import Dict, Callable
from os import getenv


"""
Сlass for training neural networks.
"""
class TransactionsData(Dataset):
    __paths: list[str] = []
    __train_data: Dict[str, list[list[str]]] = {}
    __test_data: Dict[str, list[list[str]]] = {}
    __valid_data: Dict[str, list[list[str]]] = {}
    __mapping: Dict[str, Callable[[],None]] = {}

    def __load_paths(self) -> None: ...
    def __parse_data(self, path_data: str) -> None: ...
    def __init_test_data(self) -> None: ...
    def __init_train_data(self) -> None: ...
    def __init__valid_data(self) -> None: ...

    def __init__(self, mode: str, valid: bool) -> None:
        """
        Arg:
            mode: choose data for creating 
            valid: flag for creating validation dataset

        Returns:
            None

        Example:
            >>> TransactionsData("train", True)
        """
        self.__load_paths()
        self.__mapping["train"] = self.__init_train_data
        self.__mapping["test"] = self.__init_test_data

        self.__mapping[mode]()
        if valid:
            self.__init__valid_data()        
        

    def __load_paths(self) -> None:
        """Method for getting paths"""
        train_tr = getenv("FULL_PATH_UPDATED_TRAIN_DATA_TRAN")
        test_tr = getenv("FULL_PATH_UPDATED_TEST_DATA_TRAN")
        train_id = getenv("FULL_PATH_SOURCE_TRAIN_DATA_ID")
        test_id = getenv("FULL_PATH_SOURCE_TEST_DATA_ID")

        self.__paths = [train_id, train_tr, test_id, test_tr]

    def __parse_data(self, path_data: str) -> None:
        """Method for parsing data into torch dataset"""
        ...

    def __init_test_data(self) -> None:
        """Method for initing test data for dataset"""
        ...

    def __init_train_data(self) -> None:
        """Method for initing train data for dataset"""
        ...

    def __init__valid_data(self) -> None:
        """Method for initing valid data for dataset"""
        ...