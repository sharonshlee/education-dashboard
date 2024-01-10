"""
Data models for entities:
TeacherActivity
StudentProgress
ResourceManagement
CoachDetails
CoachTeacherInteractions
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY

db = SQLAlchemy()

class TeacherActivity(db.Model):
    """
    TeacherActivity Class
    """
    __tablename__ = 'teacher_activities'

    teacher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    last_active = db.Column(db.Date)
    activity_score = db.Column(db.Integer)
    student_interaction_rating = db.Column(db.Numeric)
    subjects_taught = db.Column(ARRAY(db.String))

    coach_teachers = db.relationship('CoachTeacherInteractions', back_populates='teacher_activity', cascade='all, delete-orphan')



class StudentProgress(db.Model):
    """
    StudentProgress Class
    """
    __tablename__ = 'student_progress'

    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String)
    average_score_improvement = db.Column(db.Integer)
    homework_completion_rate = db.Column(db.Integer)
    attendance_rate = db.Column(db.Integer)


class ResourceManagement(db.Model):
    """
    ResourceManagement Class
    """
    __tablename__ = 'resource_management'

    resource_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_name = db.Column(db.String)
    allocated_teachers = db.Column(ARRAY(db.Integer))
    utilization_rate = db.Column(db.Integer)
    

class CoachDetails(db.Model):
    """
    CoachDetails Class
    """
    __tablename__ = 'coach_details'

    coach_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    specialization = db.Column(db.String)
    years_of_experience = db.Column(db.Integer)
    coach_teachers = db.relationship('CoachTeacherInteractions', back_populates='coach_detail', cascade='all, delete-orphan')
    


class CoachTeacherInteractions(db.Model):
    """
    CoachTeacherInteractions Class
    """
    __tablename__ = 'coach_teacher_interactions'

    coach_teacher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach_details.coach_id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher_activities.teacher_id'), nullable=False)
    last_meeting_date = db.Column(db.Date)
    meeting_notes = db.Column(db.String)

    coach_detail = db.relationship('CoachDetails', back_populates='coach_teachers')
    teacher_activity = db.relationship('TeacherActivity', back_populates='coach_teachers')
