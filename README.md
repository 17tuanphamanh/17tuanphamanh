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

</div>

<br>

---

<div align="center">

# VOCA — nền tảng hướng nghiệp có AI

<a href="https://www.voca.io.vn">
  <img src="assets/voca-preview.png" alt="Giao diện VOCA" width="86%">
</a>

### → **[www.voca.io.vn](https://www.voca.io.vn)** ← &nbsp;·&nbsp; đang chạy production

**824 file · ~107.000 dòng code · 75 migration · 19 domain nghiệp vụ** — tôi làm cả backend, frontend, hạ tầng và tầng AI.

</div>

Nền tảng hướng nghiệp cho học sinh THPT và sinh viên: trắc nghiệm năng lực, trợ lý AI, gợi ý trường - ngành,
đặt lịch tư vấn với mentor. Tên miền riêng, có thanh toán, có điều khoản và chính sách hoàn tiền.

> 🔒 Repo private vì đang phục vụ người dùng thật. Cần xem code khi phỏng vấn, tôi mở quyền ngay — email cho tôi.

<br>

---

<div align="center">

# 🧠 Generative AI — tầng `ai_core`

Tầng trung gian giữa sản phẩm và các nhà cung cấp LLM, tôi tự viết.

<img src="assets/ai-core.png" alt="Kiến trúc ai_core" width="100%">

</div>

<table>
<tr>
<td width="26%"><b>💸 Chi phí không kiểm soát được</b></td>
<td>Chia tác vụ theo <b>tier</b>: việc khối lượng lớn đi DeepSeek, việc quan trọng mỗi phiên một lần mới dùng Anthropic Opus. Thiếu key thì tự lùi sang key khác, deployment dở dang vẫn chạy.</td>
</tr>
<tr>
<td><b>📉 Không biết mỗi request tốn bao nhiêu</b></td>
<td>Bảng giá <b>13 model</b>, mỗi lời gọi ghi tokens và cost vào sổ cái theo <b>người dùng · tính năng · model</b>. Model lạ lùi về mức giá thận trọng, <b>không bao giờ ghi cost bằng 0</b>.</td>
</tr>
<tr>
<td><b>🕳 Fallback im lặng</b></td>
<td>Gọi model hỏng mà lặng lẽ trả mock thì người dùng cắm key xong vẫn thấy demo, không hiểu vì sao. Giờ lỗi phân thành <b>8 nhóm</b> và trả lý do lên tận giao diện quản trị.</td>
</tr>
<tr>
<td><b>🔓 Output tự do làm vỡ backend</b></td>
<td>Mọi lời gọi ràng buộc theo <b>JSON schema</b>, tầng dưới luôn nhận đúng cấu trúc. Kèm quota theo key theo ngày; prompt tách khỏi logic chain nên sửa prompt không đụng code.</td>
</tr>
</table>

**Chín chain đang chạy:** `career_recommender` · `school_recommender` · `roadmap_generator` · `profile_analyzer` ·
`expert_matcher` · `expert_review` · `consultation` · `advisor` · `base`

<br>

---

<div align="center">

# 🤖 AI Agent — tự gọi tool, vừa chạy vừa trả lời

<img src="assets/ai-agent.png" alt="Agent loop" width="100%">

</div>

- **Stream và tool use chạy đồng thời.** Chữ đẩy ra cho người dùng đọc *ngay trong lúc* model còn đang cân nhắc gọi tool — chờ agent xong hết mới trả về thì người dùng nhìn màn hình trống mất nhiều giây.
- **Vòng lặp có trần cứng.** `MAX_TOOL_ITERS = 5`; agent không giới hạn có thể quay vòng vô hạn và đốt sạch token.
- **Neo câu trả lời vào dữ liệu thật.** Sáu tool đọc thẳng PostgreSQL, thêm một tool tìm web **bắt buộc trích nguồn** — chặn model bịa tên ngành hay bịa điểm chuẩn, vấn đề chí mạng của sản phẩm tư vấn.

<br>

---

<div align="center">

# ⚡ Vài chỗ khó khác

</div>

<table>
<tr>
<td width="26%"><b>🔌 WebSocket scale ngang</b></td>
<td>Nhiều instance thì người dùng nối vào B không nhận được tin sinh ra ở A. Giải bằng <b>Redis pub/sub fan-out</b>: instance tạo tin <i>chỉ publish</i>, listener trên mọi instance mới lo gửi — mỗi socket nhận <b>đúng một lần</b>.</td>
</tr>
<tr>
<td><b>💳 Thanh toán SePay</b></td>
<td>Thanh toán QR, <b>webhook xác thực bằng chữ ký HMAC</b> nên không ai giả được thông báo "đã thanh toán". Có chống giao dịch trùng, payout cho mentor, hoàn tiền.</td>
</tr>
<tr>
<td><b>📅 Google Calendar</b></td>
<td><b>OAuth2 + Calendar API v3 gọi REST thẳng bằng <code>httpx</code></b>, không kéo thư viện client. Thiếu credentials thì mọi lối vào thành no-op, nền tảng chạy y nguyên.</td>
</tr>
<tr>
<td><b>🎙 Giọng nói</b></td>
<td>TTS và STT trên trình duyệt, tầng STT thiết kế <b>provider cắm rời</b>: một dùng Web Speech API, một chạy <b>Whisper trên WebAssembly ngay trong trình duyệt</b>.</td>
</tr>
</table>

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

- **Chọn ngưỡng theo nghiệp vụ, không lấy mặc định 0,5.** Bỏ sót khách sắp rời tốn hơn gọi nhầm khách đang ở lại, nên đặt ràng buộc recall ≥ 0,70 rồi mới dò ra ngưỡng 0,475 → recall 0,690, precision 0,513.
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

# ⚙️ Backend Java — không dùng framework

</div>

<a href="https://github.com/17tuanphamanh/swp301-block"><img src="https://img.shields.io/badge/swp301--block-181717?style=flat-square&logo=github&logoColor=white"></a>

Hệ thống đặt món trước và POS. Controller, DAO, view viết tay hết để nắm chắc MVC ba tầng.
Đơn đặt trước *không* xuống bếp khi thanh toán — hệ thống giữ lại, chỉ đẩy xuống bếp **trước giờ hẹn 20 phút**,
đủ để món vừa xong khi khách tới mà không nguội.

<br>

---

<div align="center">

# 🛠 Công nghệ

<img src="https://skillicons.dev/icons?i=python,fastapi,postgres,redis,docker,githubactions,sklearn,opencv,ts,nextjs,react,tailwind,java,git,vercel&perline=8&theme=dark" alt="Tech stack">

</div>

| | |
|---|---|
| **Ngôn ngữ** | Python · TypeScript · Java · SQL |
| **AI / LLM** | Anthropic · OpenAI · Gemini · DeepSeek · function calling · structured output · streaming · prompt engineering · token & cost accounting |
| **ML / CV** | scikit-learn · XGBoost · SHAP · YOLOv8 · OpenCV · pandas · NumPy |
| **Backend** | FastAPI · SQLAlchemy async · Alembic · Redis · WebSocket · JWT · OAuth2 · Java Servlet |
| **Cơ sở dữ liệu** | PostgreSQL · SQL Server |
| **Frontend** | Next.js 14 · React · TypeScript · Tailwind · Zustand |
| **Kiểm thử** | Playwright · Vitest · React Testing Library · MSW |
| **DevOps** | Docker · GitHub Actions · Vercel · Render · Sentry |

<br>

---

<div align="center">

## 📬 Liên hệ

### Đang tìm vị trí **AI Engineer · Machine Learning Engineer · Data Scientist**

<a href="mailto:phamtuana160324@gmail.com"><img src="https://img.shields.io/badge/Gmail-phamtuana160324@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0B1120"></a>
<a href="https://www.voca.io.vn"><img src="https://img.shields.io/badge/Website-voca.io.vn-2563EB?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=0B1120"></a>

📍 Hà Nội, Việt Nam

</div>
