from flask import Flask
from .config import Config
from .api.middleware import setup_middleware
from .api.routes import register_routes
from .infrastructure.databases import init_db
from .app_logging import setup_logging
# 1. Import module CORS để xử lý lỗi kết nối Frontend
from .cors import init_cors 
# 2. Import Controller đánh giá (Assessment) mới tạo
from .api.controllers.assessment_controller import bp as assessment_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Thiết lập Logging
    setup_logging(app)
    
    # Khởi tạo Database
    init_db(app)
    
    # Kích hoạt CORS (Quan trọng để test với Frontend React)
    init_cors(app)
    
    # Thiết lập Middleware
    setup_middleware(app)
    
    # Đăng ký các routes cũ (như Todo, Course...)
    register_routes(app)

    # Đăng ký Blueprint cho tính năng Đánh giá (Assessment)
    app.register_blueprint(assessment_bp)

    return app