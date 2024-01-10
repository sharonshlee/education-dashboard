"""
CoachesTeachersInteractions class
Managing CoachesTeachersInteractions' CRUD operations
"""
from datetime import datetime
from typing import List

from sqlalchemy import or_

from .data_manager_interface import DataManagerInterface
from backend.db.models import CoachTeacherInteractions, CoachDetails, TeacherActivity


class CoachesTeachersInteractions:
    """
    CoachesTeachersInteractions class
    Implementing CoachesTeachersInteractions' CRUD operations
    """

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager


    @staticmethod
    def __coach_teacher_to_dict(coach_teacher) -> dict:
        """
        Convert from db object to dict format
        """
        raw_date = coach_teacher.last_meeting_date
        last_meeting_date = raw_date.strftime('%Y-%m-%d')

        return {"coach_teacher_id": coach_teacher.coach_teacher_id,
                "coach_id": coach_teacher.coach_id,
                "teacher_id": coach_teacher.teacher_id,
                "last_meeting_date": last_meeting_date,
                "meeting_notes": coach_teacher.meeting_notes,
                "coach_name": coach_teacher.coach_detail.name,
                "teacher_name": coach_teacher.teacher_activity.name
                }


    def get_all_coaches_teachers_interactions(self) -> List[dict] | None:
        """
        Return a list of all coaches teachers interactions
        :return:
            A list of dictionaries representing coaches teachers interactions |
            None or []
        """
        coaches_teachers_query = self._data_manager.get_all_data()
        if coaches_teachers_query is None:
            return None

        coaches_teachers = []
        for coach_teacher in coaches_teachers_query:
            coaches_teachers.append(self.__coach_teacher_to_dict(coach_teacher))

        return coaches_teachers


    def search_coaches_teachers(self, search_term: str, meeting_from: str, meeting_to:str) -> List[dict] | None:
        """
        Return a list filtered coaches teachers interactions given search term and last meeting dates
        :param 
            search_term: str
            meeting_from: str 
            meeting_to: str
        :return:
            filtered coaches teachers interactions (dict) |
            None or []
        """
        query = CoachTeacherInteractions.query

        if search_term:
            query = query.join(CoachDetails) \
                         .join(TeacherActivity) \
                         .filter(or_(CoachTeacherInteractions.meeting_notes.ilike((f'%{search_term}%')),
                                     CoachDetails.name.ilike((f'%{search_term}%')), 
                                     TeacherActivity.name.ilike((f'%{search_term}%'))
                                    ))

        if meeting_from:
            start_datetime = datetime.strptime(meeting_from, '%Y-%m-%d')
            query = query.filter(CoachTeacherInteractions.last_meeting_date >= start_datetime)

        if meeting_to:
            end_datetime = datetime.strptime(meeting_to, '%Y-%m-%d')
            query = query.filter(CoachTeacherInteractions.last_meeting_date <= end_datetime)

        coaches_teachers = query.all()
        
        if coaches_teachers is None:
            return None
        
        filtered_coaches_teachers = []
        for coach_teacher in coaches_teachers:
            filtered_coaches_teachers.append(self.__coach_teacher_to_dict(coach_teacher))

        return filtered_coaches_teachers
