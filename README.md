<div align="center">
  <img src="assets/banner.png" alt="Phạm Tuấn Anh — AI Engineer & Machine Learning" width="100%">
</div>

<div align="center">

<a href="https://www.voca.io.vn"><img src="https://img.shields.io/badge/Sản_phẩm_AI_đang_chạy-voca.io.vn-2563EB?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=0B1120"></a>
<a href="mailto:phamtuana160324@gmail.com"><img src="https://img.shields.io/badge/Email-phamtuana160324@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0B1120"></a>

<br><br>

### Tôi đưa mô hình vào sản phẩm chạy thật — không dừng lại ở notebook.

Việc khó của AI trong sản phẩm không nằm ở lúc gọi model, mà ở những gì bao quanh nó:<br>
định tuyến chi phí, ràng buộc output, xử lý khi provider hỏng, và đo xem mỗi request tốn bao nhiêu tiền.

<br>

<a href="https://www.voca.io.vn">
  <img src="assets/voca-preview.png" alt="VOCA — nền tảng hướng nghiệp có AI" width="88%">
</a>

## VOCA — nền tảng hướng nghiệp có AI

**[www.voca.io.vn](https://www.voca.io.vn)** &nbsp;·&nbsp; đang chạy production

**824 file · ~107.000 dòng code · 75 migration · 19 domain** — tôi làm cả tầng AI, backend, frontend và hạ tầng

</div>

Trắc nghiệm đánh giá năng lực, trợ lý AI, gợi ý trường - ngành và đặt lịch tư vấn với mentor.
Tên miền riêng, có thanh toán, có điều khoản và chính sách hoàn tiền.

> 🔒 Repo private vì đang phục vụ người dùng thật. Cần xem code khi phỏng vấn, tôi mở quyền ngay — email cho tôi.

<br>

---

<div align="center">

# 🧠 Generative AI

Tôi tự viết `ai_core` — tầng trung gian giữa sản phẩm và các nhà cung cấp LLM.

<img src="assets/ai-core.png" alt="Kiến trúc ai_core" width="100%">

<br><br>

<img src="assets/panel-problems.png" alt="Bốn vấn đề chỉ lộ ra khi hệ thống chạy thật" width="100%">

</div>

**Chín chain đang phục vụ người dùng:** `career_recommender` · `school_recommender` · `roadmap_generator` ·
`profile_analyzer` · `expert_matcher` · `expert_review` · `consultation` · `advisor` · `base`

<br>

---

<div align="center">

# 🤖 AI Agent

Chain `advisor` không chỉ sinh chữ — model tự quyết định cần tra dữ liệu gì, gọi tool, đọc kết quả, rồi vòng lại.

<img src="assets/ai-agent.png" alt="Agent loop" width="100%">

</div>

- **Stream và tool use chạy đồng thời.** Chữ đẩy ra cho người dùng đọc *ngay trong lúc* model còn đang cân nhắc gọi tool — chờ agent xong hết mới trả về thì người dùng nhìn màn hình trống mất nhiều giây.
- **Vòng lặp có trần cứng.** `MAX_TOOL_ITERS = 5`; agent không giới hạn có thể quay vòng vô hạn và đốt sạch token.
- **Neo câu trả lời vào dữ liệu thật.** Sáu tool đọc thẳng PostgreSQL, thêm một tool tìm web **bắt buộc trích nguồn** — chặn model bịa tên ngành hay bịa điểm chuẩn, vấn đề chí mạng của một sản phẩm tư vấn.

<br>

---

<div align="center">

# 📊 Machine Learning & Computer Vision

</div>

### Explainable ML — dự đoán khách hàng rời bỏ

<a href="https://github.com/17tuanphamanh/churn-explainable-ml"><img src="https://img.shields.io/badge/churn--explainable--ml-181717?style=flat-square&logo=github&logoColor=white"></a>
<a href="https://github.com/17tuanphamanh/Churn_Data_Processing"><img src="https://img.shields.io/badge/Churn__Data__Processing-181717?style=flat-square&logo=github&logoColor=white"></a>

10.000 hồ sơ khách hàng ngân hàng, churn rate 20,37%. HistGradientBoosting + `class_weight` →
**test PR-AUC 0,674 · ROC-AUC 0,846**. SHAP cho thấy Age > NumOfProducts > Geography.

- **Chọn ngưỡng theo mục tiêu nghiệp vụ, không lấy mặc định 0,5.** Bỏ sót khách sắp rời tốn hơn gọi nhầm khách đang ở lại, nên đặt ràng buộc recall ≥ 0,70 rồi mới dò ra ngưỡng 0,475 → recall 0,690, precision 0,513.
- **Chống rò rỉ dữ liệu.** Preprocessor chỉ `fit` trên train rồi mới `transform` cho val/test; pipeline 8 bước, stratified 70/15/15, `random_state=42`, chạy lại ra đúng số cũ.
- **Giữ lại kết quả âm tính.** SMOTE *không* cải thiện so với `class_weight` ở mức mất cân bằng này — tôi ghi thẳng vào báo cáo thay vì lược đi cho đẹp.

### Computer Vision — phát hiện cháy thời gian thực

<a href="https://github.com/17tuanphamanh/YOLOv8n-FireDetection"><img src="https://img.shields.io/badge/YOLOv8n--FireDetection-181717?style=flat-square&logo=github&logoColor=white"></a>

YOLOv8n trên camera IP, cảnh báo Telegram kèm ảnh có bounding box.

- **Cảnh báo theo chuyển trạng thái, không theo khung hình** — bắn mỗi khung thì một đám cháy 10 giây tạo hàng trăm tin nhắn. Chỉ gửi khi `An toàn → Nguy hiểm`, cộng cooldown 20 giây.
- **Ngưỡng `conf=0.7` đặt cao có chủ đích** — đổi chút recall lấy việc giảm mạnh báo động giả, vì lửa thật xuất hiện liên tục qua nhiều khung. Inference chạy thread riêng nên giao diện không đứng hình.

### Regression — dự đoán giá nhà

<a href="https://github.com/17tuanphamanh/House-Price-Prediction-using-Linear-Regression"><img src="https://img.shields.io/badge/House--Price--Prediction-181717?style=flat-square&logo=github&logoColor=white"></a>

Kaggle *House Prices*, 80+ feature. Linear Regression làm baseline (CV RMSE ~36.000), so sánh Ridge, Lasso,
Random Forest, XGBoost; tuning bằng `GridSearchCV`.

<br>

---

<div align="center">

# ⚡ Vài chỗ khó khác

<img src="assets/panel-system.png" alt="WebSocket scale ngang, SePay HMAC, Google Calendar, hệ thống giọng nói" width="100%">

</div>

<br>

---

<div align="center">

# 🛠 Công nghệ

<img src="assets/panel-stack.png" alt="Tech stack" width="100%">

<br><br>

## 📬 Liên hệ

### Đang tìm vị trí **AI Engineer · Machine Learning Engineer · Data Scientist**

<a href="mailto:phamtuana160324@gmail.com"><img src="https://img.shields.io/badge/Gmail-phamtuana160324@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0B1120"></a>
<a href="https://www.voca.io.vn"><img src="https://img.shields.io/badge/Website-voca.io.vn-2563EB?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=0B1120"></a>

📍 Hà Nội, Việt Nam

</div>
