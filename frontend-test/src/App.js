import React, { useState } from 'react';

// Bộ câu hỏi giả lập (Mô phỏng WHO ASSIST)
const QUESTIONS = [
  {
    id: 1,
    text: "Trong cuộc đời bạn, bạn đã bao giờ sử dụng chất kích thích (thuốc lá, rượu, ma túy...) chưa?",
    options: [
      { label: "Chưa bao giờ", score: 0 },
      { label: "Đã từng, nhưng đã bỏ", score: 3 },
      { label: "Đang sử dụng", score: 6 }
    ]
  },
  {
    id: 2,
    text: "Trong 3 tháng qua, tần suất bạn sử dụng là bao nhiêu?",
    options: [
      { label: "Không bao giờ", score: 0 },
      { label: "1-2 lần/tháng", score: 4 },
      { label: "Hàng tuần", score: 6 },
      { label: "Hàng ngày", score: 8 }
    ]
  },
  {
    id: 3,
    text: "Bạn có bao giờ cảm thấy rất thèm muốn hoặc bị thôi thúc phải sử dụng không?",
    options: [
      { label: "Không bao giờ", score: 0 },
      { label: "Thỉnh thoảng", score: 3 },
      { label: "Thường xuyên", score: 6 }
    ]
  },
  {
    id: 4,
    text: "Việc sử dụng chất kích thích có gây ra vấn đề về sức khỏe, xã hội, pháp lý hay tài chính không?",
    options: [
      { label: "Không", score: 0 },
      { label: "Có, 1-2 lần", score: 5 },
      { label: "Có, thường xuyên", score: 7 }
    ]
  }
];

function App() {
  const [answers, setAnswers] = useState({}); // Lưu điểm số của từng câu: {1: 0, 2: 6...}
  const [result, setResult] = useState(null); // Lưu kết quả từ server trả về
  const [loading, setLoading] = useState(false);

  // Xử lý khi chọn đáp án
  const handleSelect = (questionId, score) => {
    setAnswers({ ...answers, [questionId]: score });
  };

  // Gửi dữ liệu lên Backend
  const handleSubmit = async () => {
    // Validate xem đã chọn hết câu hỏi chưa
    if (Object.keys(answers).length < QUESTIONS.length) {
      alert("Vui lòng trả lời hết các câu hỏi!");
      return;
    }

    setLoading(true);
    try {
      // Chuyển object answers thành mảng điểm số để gửi đi: [0, 6, 3, 5]
      const scoresArray = Object.values(answers);
      
      const response = await fetch('http://localhost:9999/assessments/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: scoresArray }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Lỗi kết nối server!");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAnswers({});
    setResult(null);
  };

  // --- Render Giao diện ---
  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1>Hệ Thống Đánh Giá Sàng Lọc </h1>
        <p>Phần mềm hỗ trợ phòng ngừa sử dụng ma túy trong cộng đồng</p>
      </header>

      <main style={styles.main}>
        {/* Nếu chưa có kết quả thì hiện câu hỏi */}
        {!result ? (
          <div style={styles.card}>
            {QUESTIONS.map((q, index) => (
              <div key={q.id} style={styles.questionBlock}>
                <h3 style={styles.questionTitle}>Câu {index + 1}: {q.text}</h3>
                <div style={styles.optionsGrid}>
                  {q.options.map((opt, i) => (
                    <button
                      key={i}
                      onClick={() => handleSelect(q.id, opt.score)}
                      style={{
                        ...styles.optionBtn,
                        backgroundColor: answers[q.id] === opt.score ? '#007bff' : '#f8f9fa',
                        color: answers[q.id] === opt.score ? '#fff' : '#333',
                        borderColor: answers[q.id] === opt.score ? '#0056b3' : '#ddd',
                      }}
                    >
                      {opt.label}
                    </button>
                  ))}
                </div>
              </div>
            ))}

            <div style={styles.footer}>
              <button onClick={handleSubmit} style={styles.submitBtn} disabled={loading}>
                {loading ? "Đang phân tích..." : "Xem Kết Quả Đánh Giá"}
              </button>
            </div>
          </div>
        ) : (
          // Nếu có kết quả thì hiện màn hình kết quả
          <div style={styles.resultCard}>
            <div style={{...styles.scoreCircle, borderColor: getColor(result.action_type)}}>
              <span style={{fontSize: '40px', fontWeight: 'bold', color: getColor(result.action_type)}}>
                {result.score}
              </span>
              <span style={{fontSize: '14px', color: '#666'}}>Điểm</span>
            </div>
            
            <h2 style={{color: getColor(result.action_type), marginBottom: '10px'}}>
              {result.risk_level}
            </h2>
            
            <div style={styles.recommendationBox}>
              <h3>Khuyến nghị hành động:</h3>
              <p>{result.recommendation}</p>
            </div>

            <div style={styles.actionButtons}>
               {result.action_type !== 'info' && (
                 <button style={styles.primaryBtn}>Đặt lịch hẹn Chuyên gia</button>
               )}
               <button style={styles.secondaryBtn}>Xem khóa học phù hợp</button>
               <button onClick={handleReset} style={styles.textBtn}>Làm lại khảo sát</button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

// Helper chọn màu dựa trên mức độ rủi ro
const getColor = (type) => {
  if (type === 'danger') return '#dc3545';
  if (type === 'warning') return '#ffc107';
  return '#28a745';
};

// CSS Styles (Viết dạng Object trong JS)
const styles = {
  container: { fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", backgroundColor: '#f0f2f5', minHeight: '100vh', padding: '20px' },
  header: { textAlign: 'center', marginBottom: '30px', color: '#333' },
  main: { maxWidth: '700px', margin: '0 auto' },
  card: { backgroundColor: '#fff', padding: '30px', borderRadius: '15px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' },
  questionBlock: { marginBottom: '25px', paddingBottom: '20px', borderBottom: '1px solid #eee' },
  questionTitle: { fontSize: '18px', marginBottom: '15px', color: '#2c3e50' },
  optionsGrid: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' },
  optionBtn: { padding: '12px', border: '1px solid #ddd', borderRadius: '8px', cursor: 'pointer', transition: 'all 0.2s', fontSize: '14px', fontWeight: '500' },
  footer: { textAlign: 'center', marginTop: '20px' },
  submitBtn: { padding: '15px 40px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '30px', fontSize: '16px', fontWeight: 'bold', cursor: 'pointer', boxShadow: '0 4px 6px rgba(0,123,255,0.3)' },
  
  // Styles cho trang kết quả
  resultCard: { backgroundColor: '#fff', padding: '40px', borderRadius: '15px', boxShadow: '0 10px 25px rgba(0,0,0,0.1)', textAlign: 'center' },
  scoreCircle: { width: '120px', height: '120px', borderRadius: '50%', border: '5px solid #ddd', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', margin: '0 auto 20px auto' },
  recommendationBox: { backgroundColor: '#f8f9fa', padding: '20px', borderRadius: '10px', margin: '20px 0', textAlign: 'left', borderLeft: '4px solid #007bff' },
  actionButtons: { display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '30px' },
  primaryBtn: { padding: '12px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' },
  secondaryBtn: { padding: '12px', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer' },
  textBtn: { padding: '10px', backgroundColor: 'transparent', color: '#666', border: 'none', cursor: 'pointer', textDecoration: 'underline' }
};

export default App;