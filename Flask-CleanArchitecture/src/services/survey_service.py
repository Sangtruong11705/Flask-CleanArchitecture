from datetime import datetime
from domain.factories.assessment_factory import AssessmentFactory
from domain.models.survey_result import SurveyResult
from infrastructure.repositories.survey_repository import SurveyRepository

class SurveyService:
    def __init__(self, repository: SurveyRepository):
        self.repository = repository

    def submit_survey(self, user_id: int, survey_type: str, answers: dict) -> SurveyResult:
        # 1. SỬ DỤNG FACTORY METHOD: Lấy đúng bộ đánh giá
        evaluator = AssessmentFactory.get_evaluator(survey_type)
        
        # 2. Thực hiện đánh giá logic
        result_data = evaluator.evaluate(answers)
        
        # 3. Tạo Domain Model kết quả
        survey_result = SurveyResult(
            id=None,
            user_id=user_id,
            survey_type=survey_type,
            score=result_data['score'],
            risk_level=result_data['risk_level'],
            recommendation=result_data['recommendation'],
            created_at=datetime.utcnow()
        )
        
        # 4. Lưu xuống DB thông qua Repository
        return self.repository.save(survey_result)