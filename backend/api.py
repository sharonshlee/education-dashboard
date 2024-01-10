"""
Educational Dashboard App as a web service.
"""
from collections import Counter

from flask import Blueprint, jsonify, render_template, request

from backend.db.models import (
    TeacherActivity, StudentProgress, ResourceManagement,
    CoachDetails, CoachTeacherInteractions, db
)
from backend.data_managers.teachers_activities import TeachersActivities
from backend.data_managers.students_progress import StudentsProgress
from backend.data_managers.resources_management import ResourcesManagement
from backend.data_managers.coaches_details import CoachesDetails
from backend.data_managers.coaches_teachers_interactions import CoachesTeachersInteractions

from backend.data_managers.data_manager import DataManager

teachers_activities_data_manager = TeachersActivities(DataManager('teacher_id', TeacherActivity, db))
students_progress_data_manager = StudentsProgress(DataManager('class_id', StudentProgress, db))
resources_data_manager = ResourcesManagement(DataManager('resource_id', ResourceManagement, db))
coaches_data_manager = CoachesDetails(DataManager('coach_id', CoachDetails, db))
coaches_teachers_data_manager = CoachesTeachersInteractions(DataManager('coach_teacher_id', CoachTeacherInteractions, db))


api = Blueprint('api', __name__)


def jsonify_error_message(message, code: int):
    """
    Return jsonify error message
    and error code
    :param code: int
    :param message: str | list
    :return: error message (json), code (int)
    """
    return jsonify({"error_message": message}), code


# GET data APIs
@api.route('/teacher-activities', methods=['GET'])
def get_teacher_activities():
    """
    Return all the teacher activities
    :returns
        List of teacher activities dictionary |
        Error Message
    """
    teachers_activities = teachers_activities_data_manager.get_all_teachers_activities()
    if teachers_activities is None:
        return jsonify_error_message("Teacher activities not found.", 404)

    return jsonify(teachers_activities), 200  # ok


@api.route('/student-progress', methods=['GET'])
def get_students_progress():
    """
    Return all the students progress
    :returns
        List of students progress dictionary |
        Error Message
    """
    students_progress = students_progress_data_manager.get_all_students_progress()

    if students_progress is None:
        return jsonify_error_message("Students progress not found.", 404)

    return jsonify(students_progress), 200  # ok


def get_resource_teacher_name(resources):
    """
    Return the corresponding names of the teachers for the teacher ids in resource."
    """
    teacher_activities = teachers_activities_data_manager.get_all_teachers_activities()

    result = {}
    for teacher in teacher_activities:
        result[teacher['teacher_id']] = teacher['name']

    for resource in resources:
        allocated_teachers_ids = resource['allocated_teachers']
        allocated_teachers_names = [result[id] for id in allocated_teachers_ids]
        resource['allocated_teachers'] = allocated_teachers_names

    return resources


@api.route('/resource-management', methods=['GET'])
def get_resource_management():
    """
    Return all the resources management
    :returns
        List of resources management dictionay |
        Error Message
    """
    raw_resources = resources_data_manager.get_all_resources_management()

    resources = get_resource_teacher_name(raw_resources)

    return jsonify(resources), 200 # ok


@api.route('/coach', methods=['GET'])
def get_coach_details():
    """
    Return all the coaches details
    :returns
        List of coaches details dictionay |
        Error Message
    """
    coaches = coaches_data_manager.get_all_coaches_details()
    
    if coaches is None:
        return jsonify_error_message("Coach not found.", 404)
    
    return jsonify(coaches), 200 # ok


@api.route('/coach-teacher', methods=['GET'])
def get_coach_teacher_interactions():
    """
    Return all the coaches teachers interactions
    :returns
        List of coaches teachers interactions dictionay |
        Error Message
    """
    coaches_teachers = coaches_teachers_data_manager.get_all_coaches_teachers_interactions()

    if coaches_teachers is None:
        return jsonify_error_message("Coach not found.", 404)
    
    return jsonify(coaches_teachers), 200 # ok


# Summary APIs
@api.route('/summary', methods=["GET"])
def get_summary():
    """
    Return total numbers of teachers, classes, resources, and coaches 
    and averages for teacher activities and student progress.
    """
    teachers_activities = teachers_activities_data_manager.get_all_teachers_activities()
    students_progress = students_progress_data_manager.get_all_students_progress()
    resources_management = resources_data_manager.get_all_resources_management()
    coaches = coaches_data_manager.get_all_coaches_details()

    if teachers_activities is None or \
        students_progress is None or \
        resources_management is None or \
        coaches is None:
        return jsonify_error_message("Data not found.", 404)
    
    total_teachers = len(teachers_activities)
    total_classes =len(Counter([c['class_id'] for c in students_progress]))
    total_resources =len(resources_management)
    total_student_progress = len(students_progress)
    total_coaches = len(coaches)

    average_teacher_activity_scores =  0 if total_teachers == 0 else round(sum([teacher['activity_score'] 
                                            for teacher in teachers_activities]) / total_teachers)
    average_student_interation_ratings = 0 if total_teachers == 0 else round(sum([teacher['student_interaction_rating'] 
                                              for teacher in teachers_activities]) / total_teachers, 1)

    average_student_avg_scores_improvement = 0 if total_student_progress == 0 else round(sum([student['average_score_improvement'] 
                                                    for student in students_progress]) / total_student_progress)
    average_homework_comletion_rates = 0 if total_student_progress == 0 else round(sum([student['homework_completion_rate'] 
                                            for student in students_progress]) / total_student_progress)
    average_attendace_rates = 0 if total_student_progress == 0 else round(sum([student['attendance_rate'] 
                                    for student in students_progress]) / total_student_progress)
    
    
    result =    {"teachers":{"total_teachers": total_teachers,
                             "average_teacher_activity_scores": average_teacher_activity_scores,
                             "average_student_interation_ratings": float(average_student_interation_ratings)
                            },
                "students": {"total_classes": total_classes,
                             "average_student_avg_scores_improvement": average_student_avg_scores_improvement,
                             "average_homework_comletion_rates": average_homework_comletion_rates,
                             "average_attendace_rates": average_attendace_rates
                            },
                "resources":{"total_resources": total_resources},
                "coaches":{"total_coaches": total_coaches}
                }
    
    
    return jsonify(result), 200 # ok



# Search
@api.route('/search-teachers', methods=['POST'])
def search_teachers_activities():
    """
    Return the filtered teachers based on user input search term or last active dates
    :returns
         render teachers_results.html page
    """
    search_term = request.json.get('search_term_teacher', '')
    active_date_from = request.json.get('active_date_from', '')
    active_date_to = request.json.get('active_date_to', '')

    if search_term or active_date_from or active_date_to:
        filtered_teachers = teachers_activities_data_manager \
                            .search_teachers_activities(search_term, 
                                                        active_date_from, 
                                                        active_date_to)

        if filtered_teachers is None:
            return render_template('teachers_results.html', teachers=[]) 
        
        return render_template('teachers_results.html', teachers=filtered_teachers) 
    
    all_teachers = teachers_activities_data_manager.get_all_teachers_activities()
    if all_teachers is None:
        return render_template('teachers_results.html', teachers=[]) 

    return render_template('teachers_results.html', teachers=all_teachers) 
        

@api.route('/search-students-progress', methods=['POST'])
def search_students_progress():
    """
    Return the filtered students progress based on user input search term
    :returns
        render students_results.html page
    """
    search_term = request.json.get('search_term_student', '')

    if search_term:
        filtered_students = students_progress_data_manager.search_students_progress(search_term)

        if filtered_students is None:
            return render_template('students_results.html', students=[]) 
        
        return render_template('students_results.html', students=filtered_students) 
    
    all_students = students_progress_data_manager.get_all_students_progress()
    if all_students is None:
        return render_template('students_results.html', students=[]) 

    return render_template('students_results.html', students=all_students) 


@api.route('/search-resources', methods=['POST'])
def search_resources():
    """
    Return the filtered resources based on user input search term
    :returns
        render resources_results.html page
    """
    search_term = request.json.get('search_term_resource')

    if search_term:
        raw_filtered_resources = resources_data_manager.search_resources(search_term)
        
        filtered_resources = get_resource_teacher_name(raw_filtered_resources)


        return render_template('resources_results.html', resources=filtered_resources)
    
    raw_resources = resources_data_manager.get_all_resources_management()
    
    if raw_resources is None:
        return render_template('resources_results.html', resources=[]) 
    
    all_resources = get_resource_teacher_name(raw_resources)
    
    return render_template('resources_results.html', resources=all_resources) 


@api.route('/search-coaches', methods=['POST'])
def search_coaches():
    """
    Return the filtered coaches based on user input search term
    :returns
        render coaches_results.html page
    """
    search_term = request.json.get('search_term_coach', '')

    if search_term:
        filtered_coaches = coaches_data_manager.search_coaches(search_term)

        if filtered_coaches is None:
            return render_template('coaches_results.html', coaches=[]) 
        
        return render_template('coaches_results.html', coaches=filtered_coaches) 
 
    all_coaches = coaches_data_manager.get_all_coaches_details()
    if all_coaches is None:
            return render_template('coaches_results.html', coaches=[]) 

    return render_template('coaches_results.html', coaches=all_coaches) 


@api.route('/search-coaches-teachers', methods=['POST'])
def search_coaches_teachers():
    """
    Return the filtered coaches teachers interactions based on 
    user input search term or last meeting dates
    :returns
        render coaches_teachers_results.html page
    """
    search_term = request.json.get('search_term_coach_teacher', '')
    dateFrom = request.json.get('meeting_date_from', '')
    dateTo = request.json.get('meeting_date_to', '')

    if search_term or dateFrom or dateTo:
        filtered_coaches_teachers = coaches_teachers_data_manager \
                                        .search_coaches_teachers(search_term, 
                                                                dateFrom, 
                                                                dateTo)
        
        if filtered_coaches_teachers is None:
            return render_template('coaches_teachers_results.html', coaches_teachers=[])
        
        return render_template('coaches_teachers_results.html', coaches_teachers=filtered_coaches_teachers) 

    all_coaches_teachers = coaches_teachers_data_manager.get_all_coaches_teachers_interactions()
    if all_coaches_teachers is None:
        return render_template('coaches_teachers_results.html', coaches_teachers=[])

    return render_template('coaches_teachers_results.html', coaches_teachers=all_coaches_teachers) 
