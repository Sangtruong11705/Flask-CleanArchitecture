from flask import Flask, jsonify
from api.swagger import spec
# Thay đổi 1: Import hàm đăng ký route từ file routes.py
from api.routes import register_routes 
from api.middleware import middleware
from api.responses import success_response
from infrastructure.databases import init_db
from config import Config
from flasgger import Swagger
from config import SwaggerConfig
from flask_swagger_ui import get_swaggerui_blueprint

def create_app():
    app = Flask(__name__)
    Swagger(app)
    
    # Thay đổi 2: Sử dụng register_routes thay vì app.register_blueprint(todo_bp)
    register_routes(app)

     # Thêm Swagger UI blueprint
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Todo API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    try:
        init_db(app)
    except Exception as e:
        print(f"Error initializing database: {e}")

    # Register middleware
    middleware(app)

    # Register routes for APISpec (Swagger custom generation)
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            # Thay đổi 3: Thêm 'survey.' vào danh sách để hiện lên Swagger
            if rule.endpoint.startswith(('todo.', 'course.', 'user.', 'survey.')):
                view_func = app.view_functions[rule.endpoint]
                print(f"Adding path: {rule.rule} -> {view_func}")
                try:
                    spec.path(view=view_func)
                except Exception as e:
                    print(f"Skipping swagger for {rule.endpoint}: {e}")

    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())

    return app

# Run the application
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9999, debug=True)