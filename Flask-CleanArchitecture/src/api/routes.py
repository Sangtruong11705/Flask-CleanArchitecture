# File: src/api/routes.py

# Xóa "src." ở đầu dòng, chỉ giữ lại từ "api..."
from api.controllers.todo_controller import bp as todo_bp
from api.controllers.survey_controller import bp as survey_bp

def register_routes(app):
    app.register_blueprint(todo_bp)
    app.register_blueprint(survey_bp)