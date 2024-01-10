"""
TeachersActivities class
Managing TeachersActivities' CRUD operations
"""
from datetime import datetime
from typing import List
from sqlalchemy import or_


from .data_manager_interface import DataManagerInterface
from backend.db.models import TeacherActivity


class TeachersActivities:
    """
    TeachersActivities class
    Implementing TeachersActivities' CRUD operations
    """

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager


    @staticmethod
    def __teacher_activity_to_dict(teacher_activity) -> dict:
        """
        Convert db object to dict format
        """
        raw_date = teacher_activity.last_active
        last_active_date = raw_date.strftime('%Y-%m-%d')

        return {"teacher_id": teacher_activity.teacher_id,
                "name": teacher_activity.name,
                "last_active": last_active_date,
                "activity_score": teacher_activity.activity_score,
                "student_interaction_rating": teacher_activity.student_interaction_rating,
                "subjects_taught": teacher_activity.subjects_taught
                }


    def get_all_teachers_activities(self) -> List[dict] | None:
        """
        Return a list of all teachers activities
        :return:
            A list of dictionaries representing teachers activities
        """
        teachers_activities_query = self._data_manager.get_all_data()
        if teachers_activities_query is None:
            return None

        teachers_activities = []
        for teacher_activity in teachers_activities_query:
            teachers_activities.append(self.__teacher_activity_to_dict(teacher_activity))

        return teachers_activities
    

    @staticmethod
    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False


    def search_teachers_activities(self, search_term: str, active_from: str, active_to: str) -> dict | None:
        """
        Return a list filtered teachers activities given search term or last active dates
        :params
            search_term: str
            active_from: str
            active_to: str
        :return:
            filtered teacher activities (dict) |
            None or []
        """
        query = TeacherActivity.query
        
        if search_term:
            queries = []

            if search_term.isdigit():
                search_term = int(search_term)
                queries.append(TeacherActivity.teacher_id == search_term)
                queries.append(TeacherActivity.activity_score == search_term)
            elif self.is_float(search_term):
                search_term = float(search_term)
                queries.append(TeacherActivity.student_interaction_rating == search_term)
            else:
                queries.append(TeacherActivity.name.ilike(f'%{search_term}%'))

            query = query.filter(or_(*queries))

        if active_from:
            start_datetime = datetime.strptime(active_from, '%Y-%m-%d')
            query = query.filter(TeacherActivity.last_active >= start_datetime)

        if active_to:
            end_datetime = datetime.strptime(active_to, '%Y-%m-%d')
            query = query.filter(TeacherActivity.last_active <= end_datetime)


        teachers = query.all()
        if teachers is None:
            return None
        
        filtered_teachers = []
        for teacher in teachers:
            filtered_teachers.append(self.__teacher_activity_to_dict(teacher))

        return filtered_teachers

