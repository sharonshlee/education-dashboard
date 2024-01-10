"""
DataManager class implemented DataManagerInterface
for managing data from database
"""
from abc import ABC

from sqlalchemy.exc import SQLAlchemyError

from .data_manager_interface import DataManagerInterface


class DataManager(DataManagerInterface, ABC):
    """
    A class for managing data
    from database
    """

    def __init__(self, id_key, entity, db):
        self.db = db
        self._id_key = id_key
        self._entity = entity


    def get_all_data(self):
        """
        Return all data from DB
        :return:
            A query object representing all the data
            None
        """
        try:
            return self._entity.query.all()
        
        except SQLAlchemyError as err:
            print(err)
            self.db.session.rollback()
            return None
        
        """
        Delete an item based on item_id
        :param item_id: int
        :return:
            True for success delete item (bool) |
            None
        """

        try:
            item = self._entity.query.get(item_id)
            self.db.session.delete(item)
            self.db.session.commit()
            return True
        except SQLAlchemyError:
            self.db.session.rollback()
            return None
