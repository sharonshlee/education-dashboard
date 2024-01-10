"""
StudentsProgress class
Managing StudentProgress' CRUD operations
"""
from typing import List

from sqlalchemy import or_

from .data_manager_interface import DataManagerInterface
from backend.db.models import StudentProgress


class StudentsProgress:
    """
    StudentsProgress class
    Implementing StudentProgress' CRUD operations
    """

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager


    @staticmethod
    def __student_progress_to_dict(student_progress) -> dict:
        """
        Convert db object to dict format
        """

        return {"class_id": student_progress.class_id,
                "subject": student_progress.subject,
                "average_score_improvement": student_progress.average_score_improvement,
                "homework_completion_rate": student_progress.homework_completion_rate,
                "attendance_rate": student_progress.attendance_rate
                }


    def get_all_students_progress(self) -> List[dict] | None:
        """
        Return a list of all students progress
        :return:
            A list of dictionaries representing students progress |
            None or []
        """
        students_progress_query = self._data_manager.get_all_data()
        if students_progress_query is None:
            return None

        students_progress = []
        for student_progress in students_progress_query:
            students_progress.append(self.__student_progress_to_dict(student_progress))

        return students_progress
    
    
    def search_students_progress(self, search_term: str) -> dict | None:
        """
        Return a list filtered students progress given search term
        :param 
            search_term: str
        :return:
            filtered students progress (dict) |
            None or []
        """
        query = StudentProgress.query

        if search_term:
            queries = []

            if search_term.isdigit():
                search_term = int(search_term)
                queries.append(StudentProgress.class_id == search_term)
                queries.append(StudentProgress.average_score_improvement == search_term)
                queries.append(StudentProgress.homework_completion_rate == search_term)
                queries.append(StudentProgress.attendance_rate == search_term)
            else:
                queries.append(StudentProgress.subject.ilike(f'%{search_term}%'))

            query = query.filter(or_(*queries))

        students = query.all()
        
        if students is None:
            return None
        
        filtered_students = []
        for student in students:
            filtered_students.append(self.__student_progress_to_dict(student))

        return filtered_students
