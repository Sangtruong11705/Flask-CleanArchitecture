class SurveyResult:
    def __init__(self, id, user_id, survey_type, score, risk_level, recommendation, created_at):
        self.id = id
        self.user_id = user_id
        self.survey_type = survey_type
        self.score = score
        self.risk_level = risk_level
        self.recommendation = recommendation
        self.created_at = created_at