from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from infrastructure.databases.base import Base

class SurveyResultModel(Base):
    __tablename__ = 'survey_results_v2'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)    
    survey_type = Column(String(50), nullable=False) 
    score = Column(Float, nullable=False)
    risk_level = Column(String(50))
    recommendation = Column(String(255))
    created_at = Column(DateTime)   