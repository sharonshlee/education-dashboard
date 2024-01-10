"""
DataManagerInterface:
Data management for db sources.
"""
from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """
    An Interface Class that reading file,
    parsing the data into Python
    data structures (lists and dictionaries),
    and providing methods to
    manipulate the data
    """

    @abstractmethod
    def get_all_data(self):
        """
        Return all the data from db
        :return:
            Query object representing all the data
        """

