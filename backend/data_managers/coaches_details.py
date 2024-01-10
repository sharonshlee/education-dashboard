"""
CoachesDetails class
Managing CoachesDetails' CRUD operations
"""
from typing import List

from sqlalchemy import or_

from .data_manager_interface import DataManagerInterface
from backend.db.models import CoachDetails


class CoachesDetails:
    """
    CoachesDetails class
    Implementing CoachesDetails' CRUD operations
    """

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager


    @staticmethod
    def __coach_details_to_dict(coach) -> dict:
        """
        Convert db object to dict format
        """

        return {"coach_id": coach.coach_id,
                "name": coach.name,
                "specialization": coach.specialization,
                "years_of_experience": coach.years_of_experience
                }


    def get_all_coaches_details(self) -> List[dict] | None:
        """
        Return a list of all coaches details
        :return:
            A list of dictionaries representing coaches details |
            None or []
        """
        coaches_query = self._data_manager.get_all_data()
        if coaches_query is None:
            return None

        coaches_details = []
        for coach in coaches_query:
            coaches_details.append(self.__coach_details_to_dict(coach))

        return coaches_details


    def search_coaches(self, search_term):
        """
        Return a list filtered coaches given search term
        :param 
            search_term: str
        :return:
            filtered coaches (dict) |
            None or []
        """
        query = CoachDetails.query

        if search_term:
            queries = []

            if search_term.isdigit():
                search_term = int(search_term)
                queries.append(CoachDetails.coach_id == search_term)
                queries.append(CoachDetails.years_of_experience == search_term)
            else:
                queries.append(CoachDetails.name.ilike(f'%{search_term}%'))
                queries.append(CoachDetails.specialization.ilike(f'%{search_term}%'))

            query = query.filter(or_(*queries))

        coaches = query.all()
        
        if coaches is None:
            return None
        
        filtered_coaches = []
        for coach in coaches:
            filtered_coaches.append(self.__coach_details_to_dict(coach))
            
        return filtered_coaches
