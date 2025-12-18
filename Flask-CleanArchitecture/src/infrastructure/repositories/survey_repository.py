from infrastructure.models.survey_result_model import SurveyResultModel
from domain.models.survey_result import SurveyResult
from infrastructure.databases.mssql import session
from datetime import datetime

class SurveyRepository:
    def __init__(self):
        self.session = session

    def save(self, survey_result: SurveyResult) -> SurveyResult:
        try:
            model = SurveyResultModel(
                user_id=survey_result.user_id,
                survey_type=survey_result.survey_type,
                score=survey_result.score,
                risk_level=survey_result.risk_level,
                recommendation=survey_result.recommendation,
                created_at=survey_result.created_at
            )
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            
            # Cập nhật ID lại cho domain model
            survey_result.id = model.id
            return survey_result
        except Exception as e:
            self.session.rollback()
            raise e