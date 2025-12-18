from infrastructure.databases.mssql import init_mssql, Base

# Import trực tiếp từ file (module) thay vì import qua package
# Điều này giúp tránh lỗi "cannot import name" khi file __init__.py ở models bị rỗng
import infrastructure.models.course_register_model
import infrastructure.models.todo_model
import infrastructure.models.user_model
import infrastructure.models.course_model
import infrastructure.models.consultant_model
import infrastructure.models.appointment_model
import infrastructure.models.program_model
import infrastructure.models.feedback_model
import infrastructure.models.survey_model

# Import file quan trọng nhất mà bạn đang bị lỗi
import infrastructure.models.survey_result_model 

def init_db(app):
    init_mssql(app)