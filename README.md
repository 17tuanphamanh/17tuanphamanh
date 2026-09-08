## Chào, tôi là Tuấn Anh 👋

Sinh viên ở Hà Nội, đang đi theo hướng **AI Engineer — làm sản phẩm AI chạy thật**, không phải nghiên cứu.

Tôi đã làm vài dự án machine learning tương đối đầy đủ (bên dưới). Nhưng làm xong tôi nhận ra một điều:
**tôi hiểu quy trình mà chưa hiểu bản chất.** Nên từ 23/08/2026 tôi quay lại học lại từ gốc — Python,
giải tích, backpropagation viết tay — theo một lộ trình 126 ngày tự đặt ra. Trang này ghi lại cả hai:
những gì đã làm, và những gì đang học.

---

### Đang học

**Lộ trình 126 ngày · 4 giờ/ngày · bắt đầu 23/08/2026**

| Giai đoạn | Nội dung |
|---|---|
| Tuần 0 | Python từ số 0 |
| Tuần 1–2 | Đại số tuyến tính, gradient descent, quy trình ML & overfitting |
| Tuần 3–5 | Backpropagation dẫn xuất tay, MLP, CNN — **không dùng thư viện dựng sẵn** |
| Tuần 6–10 | Tối ưu hoá, RNN, Transformer, attention, dựng GPT nhỏ từ đầu |
| Tuần 11–14 | PyTorch, fine-tuning, LoRA, RAG |
| Tuần 15–17 | LLM application: agent, evaluation, observability, triển khai |

Quy tắc tôi tự đặt: **tuần 3, 4, 5, 9, 10, 12 cấm dùng thư viện dựng sẵn** cho bài chính.
Backprop, attention, LoRA phải tự viết được bằng NumPy trước khi cho phép mình gọi `torch.nn`.

> Tiến độ hiện tại: **Tuần 0** — đang học Python. Đo bằng số ngày đã tick, không đo bằng lịch.

---

### Dự án

#### Explainable ML cho dự đoán khách hàng rời bỏ
[`churn-explainable-ml`](https://github.com/17tuanphamanh/churn-explainable-ml) · [`Churn_Data_Processing`](https://github.com/17tuanphamanh/Churn_Data_Processing)

Dự đoán churn trên 10.000 khách hàng ngân hàng (churn rate 20,37%), rồi dùng SHAP để giải thích
mô hình quyết định dựa trên cái gì — mục tiêu cuối là **thiết kế chiến lược giữ chân theo phân khúc**,
không dừng ở con số accuracy.

| | |
|---|---|
| Mô hình tốt nhất | HistGradientBoosting + `class_weight` |
| Test PR-AUC / ROC-AUC | **0,674 / 0,846** |
| Ngưỡng chọn theo recall ≥ 0,70 | 0,475 → Recall **0,690**, Precision 0,513, F1 0,589 |
| Yếu tố chi phối (SHAP) | Age > NumOfProducts > Geography |

Hai chi tiết tôi quan tâm nhất khi làm:
- **Chống rò rỉ dữ liệu (leakage):** preprocessor chỉ `fit` trên tập train, rồi mới `transform` cho val/test. Tách stratified 70/15/15.
- **SMOTE không phải lúc nào cũng tốt:** với mức mất cân bằng nhẹ này, SMOTE *không* cải thiện so với `class_weight`. Tôi giữ lại kết quả âm tính đó trong báo cáo thay vì giấu đi.

#### Phát hiện cháy thời gian thực + cảnh báo Telegram
[`YOLOv9-FireDetection`](https://github.com/17tuanphamanh/YOLOv9-FireDetection)

Nhận diện lửa và khói theo thời gian thực bằng YOLOv8n, tự động gửi ảnh có bounding box
kèm mốc thời gian về Telegram, lưu snapshot cục bộ. Python 3.8+.

#### Dự đoán giá nhà — Kaggle
[`House-Price-Prediction-using-Linear-Regression`](https://github.com/17tuanphamanh/House-Price-Prediction-using-Linear-Regression)

Bài toán *House Prices – Advanced Regression Techniques* với 80+ feature. Đi từ Linear Regression
làm baseline (CV RMSE ~36.000) rồi so sánh Ridge, Lasso, Random Forest, XGBoost.
Tuning bằng `GridSearchCV`, dựng pipeline sklearn theo module.

#### Hệ thống đặt món trước & POS cho cửa hàng đồ ăn nhanh
[`swp301-block`](https://github.com/17tuanphamanh/swp301-block) · Đồ án SWP301

Java 17 · Servlet 4 · JSTL · SQL Server (JDBC thuần) · Tomcat 9 · Maven · HikariCP · bcrypt · ZXing

**Không dùng framework** — toàn bộ tầng controller, DAO và view viết tay để thấy rõ MVC ba tầng vận hành.
Điểm nghiệp vụ thú vị: đơn đặt trước *không* xuống bếp ngay khi thanh toán. Hệ thống giữ đơn lại và
chỉ đẩy xuống bếp **trước giờ khách hẹn 20 phút** — đủ để món vừa xong khi khách tới, không sớm tới mức nguội.
Có xử lý thanh toán trùng (idempotency) và 4 vai trò: khách, thu ngân, bếp, quản trị.

---

### Công cụ đang dùng

**Ngôn ngữ** Python · Java · SQL
**ML / DL** scikit-learn · XGBoost · SHAP · YOLO (Ultralytics) · pandas · NumPy
**Khác** Jupyter · Git · SQL Server · Tomcat · Maven

Máy làm việc: MacBook Apple M2 (không CUDA, chỉ MPS) — nên tôi phải để ý chuyện
model chạy được ở đâu, chứ không mặc định có GPU.

---

### Liên hệ

📍 Hà Nội · 📧 [phamtuana160324@gmail.com](mailto:phamtuana160324@gmail.com)

Đang tìm **thực tập / vị trí junior về AI Engineer, Machine Learning hoặc Data**.
Nếu bạn thấy chỗ nào trong các dự án trên làm chưa đúng, mở issue giúp tôi — tôi đang học, và học từ chỗ sai là nhanh nhất.
