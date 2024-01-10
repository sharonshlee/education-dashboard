"""
ResourcesManagement class
Managing ResourcesManagement' CRUD operations
"""
from typing import List

from sqlalchemy import or_

from .data_manager_interface import DataManagerInterface
from backend.db.models import ResourceManagement


class ResourcesManagement:
    """
    ResourcesManagement class
    Implementing ResourcesManagement' CRUD operations
    """

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager


    @staticmethod
    def __resource_management_to_dict(resource_management) -> dict:
        """
        Convert db object to dict format
        """

        return {"resource_id": resource_management.resource_id,
                "resource_name": resource_management.resource_name,
                "allocated_teachers": resource_management.allocated_teachers,
                "utilization_rate": resource_management.utilization_rate
                }


    def get_all_resources_management(self) -> List[dict] | None:
        """
        Return a list of all resources management
        :return:
            A list of dictionaries representing resources management |
            None or []
        """
        resources_management_query = self._data_manager.get_all_data()
        if resources_management_query is None:
            return None

        resources_management = []
        for resource_management in resources_management_query:
            resources_management.append(self.__resource_management_to_dict(resource_management))
        
        return resources_management


    def search_resources(self, search_term):
        """
        Return a list filtered resources given search term
        :param 
            search_term: str
        :return:
            filtered resources (dict) |
            None or []
        """
        query = ResourceManagement.query

        if search_term:
            queries = []

            if search_term.isdigit():
                search_term = int(search_term)
                queries.append(ResourceManagement.resource_id == search_term)
                queries.append(ResourceManagement.utilization_rate == search_term)
            else:
                queries.append(ResourceManagement.resource_name.ilike(f'%{search_term}%'))

            query = query.filter(or_(*queries))

        resources = query.all()
        
        if resources is None:
            return None
        
        filtered_resources = []
        for resource in resources:
            filtered_resources.append(self.__resource_management_to_dict(resource))
            
        return filtered_resources
