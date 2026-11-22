import torch
from torch import nn, optim
from torch.utils.data import Dataset
from pathlib import Path
from torchvision.transforms import v2 as transforms
import numpy as np
from typing import Dict, Callable
from os import getenv
from datetime import datetime


"""
Сlass for training neural networks.
"""
class TransactionsData(Dataset):
    __paths: list[str] = []
    __valid_data: Dict[str, list[list[str]]] = {}
    __mapping: Dict[str, Callable[[],None]] = {}
    __unique_ids: set[int] = {}
    __chunk_datetime: int = 0
    __indices: Dict[str, list[list[str]]] = {}
    __mode: str = ""

    def __load_paths(self) -> None: ...
    def __parse_data(self, path_data: str) -> Dict[str, Callable[[],None]]: ...
    def __init_test_data(self) -> None: ...
    def __init_train_data(self) -> None: ...
    def __init__valid_data(self) -> None: ...
    def __load_settings(self) -> None: ...
    def __load_chunk_datetime_month(self) -> None: ...


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
        self.__mode = mode
        self.__load_settings()
        self.__mapping["train"] = self.__init_train_data
        self.__mapping["test"] = self.__init_test_data

        self.__mapping[mode]()
        if valid:
            self.__init__valid_data()        
        
    def __load_settings(self) -> None:
        """Method for getting settings from env file"""
        self.__load_paths()
        self.__load_chunk_datetime_month()

    def __load_chunk_datetime_month(self) -> None:
        """Method for load chunk datetime for separation dataset"""
        self.__chunk_datetime = int(getenv("CHUNK_DATETIME_MONTH", 2))


    def __load_paths(self) -> None:
        """
        Method for getting paths

        Method initing paths array, where:
        [0] - train identity datasset
        [1] - train transaction dataset
        [2] - test identity dataset
        [3] - test transaction dataset
        """
        train_tr = getenv("FULL_PATH_UPDATED_TRAIN_DATA_TRAN")
        test_tr = getenv("FULL_PATH_UPDATED_TEST_DATA_TRAN")
        train_id = getenv("FULL_PATH_SOURCE_TRAIN_DATA_ID")
        test_id = getenv("FULL_PATH_SOURCE_TEST_DATA_ID")

        self.__paths = [train_id, train_tr, test_id, test_tr]

    def __len__(self):
        return len(self.__indices)

    def __parse_data(self, path_data: str) -> Dict[str, Callable[[],None]]:
        """Method for parsing data into torch dataset"""
        with open(path_data, "r", encoding="utf-8") as file:
            is_header: bool = True
            index_datetime: int = 0
            months_chunck: set[int] = {}
            for line in enumerate(file):
                if is_header:
                    is_header = False
                    name_header_datetime = getenv("HEADER_DATETIME")
                    index_datetime = line.split(",").index(name_header_datetime)
                    continue
                line: str = line.strip()
                parts: list[str] = line.split(",")
                key_id: int = int(parts[0])

                month: int = datetime(parts[index_datetime]).month
                self.__unique_ids.add(key_id)
                months_chunck.add(month)
                if len(months_chunck) <= self.__chunk_datetime:
                    ...

    def __init_test_data(self) -> None:
        """Method for initing test data for dataset"""
        self.__parse_data(self.__paths[2])
        self.__parse_data(self.__paths[3])

    def __init_train_data(self) -> None:
        """Method for initing train data for dataset"""
        self.__parse_data(self.__paths[0])
        self.__parse_data(self.__paths[1])

    def __init__valid_data(self) -> None:
        """Method for initing valid data for dataset"""
        ...