from abc import ABC, abstractmethod

# --- 1. Abstract Product (Giao diện chung) ---
class AssessmentEvaluator(ABC):
    @abstractmethod
    def evaluate(self, answers: dict) -> dict:
        """
        Input: Danh sách câu trả lời
        Output: { 'score': int, 'risk_level': str, 'recommendation': str }
        """
        pass

# --- 2. Concrete Products (Các bộ đánh giá cụ thể) ---

class AssistEvaluator(AssessmentEvaluator):
    """Bộ đánh giá cho người lớn (ASSIST)"""
    def evaluate(self, answers: dict) -> dict:
        # Giả lập logic tính điểm ASSIST
        score = sum(answers.values()) 
        if score > 27:
            return {"score": score, "risk_level": "Cao", "recommendation": "Cần can thiệp chuyên sâu"}
        elif score > 4:
            return {"score": score, "risk_level": "Trung bình", "recommendation": "Tư vấn ngắn hạn"}
        return {"score": score, "risk_level": "Thấp", "recommendation": "Không cần can thiệp"}

class CrafftEvaluator(AssessmentEvaluator):
    """Bộ đánh giá cho vị thành niên (CRAFFT)"""
    def evaluate(self, answers: dict) -> dict:
        # CRAFFT thường tính điểm Yes/No (Yes=1, No=0)
        score = sum(answers.values())
        if score >= 2:
            return {"score": score, "risk_level": "Cao", "recommendation": "Cần đánh giá kỹ hơn và tư vấn"}
        return {"score": score, "risk_level": "Thấp", "recommendation": "Giáo dục phòng ngừa"}

# --- 3. Creator (Factory Class) ---
class AssessmentFactory:
    @staticmethod
    def get_evaluator(survey_type: str) -> AssessmentEvaluator:
        if survey_type.upper() == "ASSIST":
            return AssistEvaluator()
        elif survey_type.upper() == "CRAFFT":
            return CrafftEvaluator()
        else:
            raise ValueError(f"Loại khảo sát '{survey_type}' không được hỗ trợ.")