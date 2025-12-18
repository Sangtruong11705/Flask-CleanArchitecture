from flask import Blueprint, request, jsonify
from services.survey_service import SurveyService
from infrastructure.repositories.survey_repository import SurveyRepository

bp = Blueprint('survey', __name__, url_prefix='/surveys')

# Khởi tạo service (Dependency Injection thủ công đơn giản)
survey_repo = SurveyRepository()
survey_service = SurveyService(survey_repo)

@bp.route('/submit', methods=['POST'])
def submit_survey():
    """
    Submit a survey assessment
    ---
    post:
      summary: Nộp bài khảo sát (ASSIST, CRAFFT...)
      tags:
        - Surveys
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                survey_type:
                  type: string
                  example: "ASSIST"
                answers:
                  type: object
                  description: "Key-value pair of question ID and score/answer"
                  example: {"q1": 4, "q2": 3, "q3": 0}
      responses:
        201:
          description: Survey submitted successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  risk_level:
                    type: string
                  recommendation:
                    type: string
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        survey_type = data.get('survey_type')
        answers = data.get('answers')

        if not all([user_id, survey_type, answers]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Gọi Service xử lý
        result = survey_service.submit_survey(user_id, survey_type, answers)

        return jsonify({
            'message': 'Đánh giá hoàn tất',
            'data': {
                'score': result.score,
                'risk_level': result.risk_level,
                'recommendation': result.recommendation
            }
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500