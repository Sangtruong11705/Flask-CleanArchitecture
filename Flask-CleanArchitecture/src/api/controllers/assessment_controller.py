from flask import Blueprint, request, jsonify

bp = Blueprint('assessment', __name__, url_prefix='/assessments')

@bp.route('/submit', methods=['POST'])
def submit_assessment():
    try:
        data = request.get_json()
        # Tính tổng điểm từ mảng câu trả lời [0, 6, 3...]
        answers = data.get('answers', [])
        total_score = sum(answers)

        # Logic đánh giá rủi ro
        if total_score <= 3:
            risk_level = "Nguy cơ Thấp"
            recommendation = "Bạn đang kiểm soát tốt. Hãy duy trì lối sống lành mạnh."
            action_type = "info"
        elif total_score <= 26:
            risk_level = "Nguy cơ Trung bình"
            recommendation = "Cảnh báo: Có dấu hiệu lạm dụng. Nên tham gia khóa học kỹ năng."
            action_type = "warning"
        else:
            risk_level = "Nguy cơ Cao"
            recommendation = "Báo động: Mức độ nghiêm trọng. Cần gặp chuyên gia ngay."
            action_type = "danger"

        return jsonify({
            "score": total_score,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "action_type": action_type
        }), 200
        
    except Exception as e:
        print(f"Lỗi: {e}")
        return jsonify({'error': 'Lỗi xử lý'}), 500