<div align="center">
  <img src="assets/banner.png" alt="Phạm Tuấn Anh — AI Engineer & Machine Learning" width="100%">
</div>

<div align="center">

  <a href="https://www.voca.io.vn">
    <img src="https://img.shields.io/badge/Sản_phẩm_AI_đang_chạy-voca.io.vn-2563EB?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=0B1120">
  </a>
  <a href="mailto:phamtuana160324@gmail.com">
    <img src="https://img.shields.io/badge/Email-phamtuana160324@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0B1120">
  </a>

<br><br>

### Tôi đưa mô hình vào sản phẩm chạy thật — không dừng lại ở notebook.

Việc khó của AI trong sản phẩm không nằm ở lúc gọi model, mà ở những gì bao quanh nó:<br>
định tuyến chi phí, ràng buộc output, xử lý khi provider hỏng, và đo xem mỗi request tốn bao nhiêu tiền.

</div>

<br>

---

<div align="center">

# 🧠 LLM Engineering — chạy production

</div>

Trong VOCA, tôi tự viết module **`ai_core`** làm tầng trung gian giữa sản phẩm và các nhà cung cấp LLM.
Đây là phần tôi tâm đắc nhất, vì nó giải quyết đúng những vấn đề chỉ lộ ra khi hệ thống chạy thật.

<div align="center">
  <img src="assets/ai-core.png" alt="Kiến trúc ai_core — routing theo tier, structured output, tính chi phí, phân loại lỗi" width="100%">
</div>

### Bốn vấn đề thật và cách tôi xử lý

<table>
<tr>
<td width="30%"><b>💸 Chi phí LLM<br>không kiểm soát được</b></td>
<td>
<code>routing.py</code> chia tác vụ theo <b>tier</b>: việc khối lượng lớn, ít rủi ro (chẩn đoán nhanh,
chat theo dõi, diễn giải kết quả) đi <b>DeepSeek</b>; việc quan trọng, mỗi phiên chỉ chạy một lần
(lời khuyên cuối, tường thuật ma trận năng lực) mới dùng <b>Anthropic Opus</b>.
Đây là <i>soft preference</i> — thiếu key thì tự lùi xuống key khác rồi tới key môi trường,
nên deployment cấu hình dở dang vẫn chạy được.
</td>
</tr>
<tr>
<td><b>📉 Không biết mỗi<br>request tốn bao nhiêu</b></td>
<td>
<code>pricing.py</code> giữ bảng giá USD/1.000 token cho <b>13 model</b> của 4 nhà cung cấp,
mỗi lời gọi đều ghi lại <code>tokens_in</code>, <code>tokens_out</code> và cost.
Model lạ không nằm trong bảng thì <b>lùi về mức giá thận trọng</b> chứ không ghi cost bằng 0 —
tôi không muốn hoá đơn bất ngờ vì một model chưa kịp cập nhật giá.
</td>
</tr>
<tr>
<td><b>🕳 Fallback im lặng —<br>lỗi khó chịu nhất</b></td>
<td>
Trước đây gọi model hỏng là hệ thống lặng lẽ trả về dữ liệu mock. Người dùng cắm API key xong
vẫn thấy kết quả demo mà <b>không hiểu tại sao</b>. Giờ <code>classify_error()</code> phân loại thành
8 nhóm — <code>sdk_missing</code> · <code>auth</code> · <code>quota</code> · <code>rate_limit</code> ·
<code>bad_model</code> · <code>bad_request</code> · <code>parse</code> · <code>network</code> —
và trả lý do lên tận giao diện.
</td>
</tr>
<tr>
<td><b>🔓 Output tự do<br>làm vỡ backend</b></td>
<td>
Mọi lời gọi đều đi qua <code>dispatch_json()</code> với <b>output ràng buộc theo JSON schema</b>,
nên tầng dưới luôn nhận đúng cấu trúc đã định. Kèm theo là <b>quota theo từng key theo ngày</b>
và bảng ghi nhận usage cùng loại lỗi, để theo dõi sức khoẻ hệ thống.
</td>
</tr>
</table>

### Chín AI chain đang phục vụ người dùng

`career_recommender` · `school_recommender` · `roadmap_generator` · `profile_analyzer` ·
`expert_matcher` · `expert_review` · `consultation` · `advisor` · `base`

Prompt tách riêng khỏi logic chain (`ai_core/prompts/`), nên sửa prompt không phải đụng vào code xử lý.

<br>

<div align="center">
  <a href="https://www.voca.io.vn">
    <img src="assets/voca-preview.png" alt="Giao diện VOCA" width="86%">
  </a>

### Sản phẩm: → **[www.voca.io.vn](https://www.voca.io.vn)** ←

</div>

Nền tảng hướng nghiệp cho học sinh THPT và sinh viên: trắc nghiệm đánh giá năng lực, trợ lý AI,
gợi ý trường - ngành và đặt lịch tư vấn với mentor. Tên miền riêng, Google Analytics, đầy đủ điều
khoản sử dụng - chính sách bảo mật - chính sách hoàn tiền.

<table>
<tr><td width="22%"><b>AI</b></td><td>Anthropic · OpenAI · Google Gemini · DeepSeek — dispatch đa nhà cung cấp, structured output</td></tr>
<tr><td><b>Backend</b></td><td>FastAPI · PostgreSQL · SQLAlchemy · Alembic · JWT (kèm <code>token_version</code> để thu hồi token)</td></tr>
<tr><td><b>Frontend</b></td><td>Next.js 14 App Router · TypeScript · Zustand · Tailwind CSS</td></tr>
<tr><td><b>Hạ tầng</b></td><td>Docker · docker-compose · Render · Vercel · 3 workflow GitHub Actions</td></tr>
<tr><td><b>Quy mô</b></td><td><b>824 file</b> — 317 backend · 378 frontend · <b>78 migration Alembic</b></td></tr>
</table>

> 🔒 Repo để private. Cần xem code khi phỏng vấn, tôi mở quyền truy cập ngay — cứ email cho tôi.

<br>

---

<div align="center">

# 📊 Machine Learning & Data Science

</div>

### Explainable ML — Dự đoán khách hàng rời bỏ

<a href="https://github.com/17tuanphamanh/churn-explainable-ml"><img src="https://img.shields.io/badge/churn--explainable--ml-181717?style=flat-square&logo=github&logoColor=white"></a>
<a href="https://github.com/17tuanphamanh/Churn_Data_Processing"><img src="https://img.shields.io/badge/Churn__Data__Processing-181717?style=flat-square&logo=github&logoColor=white"></a>

Dự đoán churn trên **10.000 hồ sơ khách hàng ngân hàng** (churn rate 20,37%), rồi dùng **SHAP** để
giải thích mô hình dựa vào đâu mà quyết định. Đích đến là **playbook giữ chân theo từng phân khúc** —
mô hình phải nói được *nên làm gì*, chứ không chỉ đưa ra một con số.

<table>
<tr><td width="34%">Mô hình tốt nhất</td><td>HistGradientBoosting + <code>class_weight</code></td></tr>
<tr><td>Test PR-AUC / ROC-AUC</td><td><b>0,674 / 0,846</b></td></tr>
<tr><td>Ngưỡng chọn theo recall ≥ 0,70</td><td>0,475 → Recall <b>0,690</b> · Precision 0,513 · F1 0,589</td></tr>
<tr><td>Yếu tố chi phối (SHAP)</td><td>Age &gt; NumOfProducts &gt; Geography</td></tr>
</table>

**Ba điều tôi làm kỹ và sẽ bảo vệ được khi phỏng vấn:**

- **Chọn ngưỡng theo mục tiêu nghiệp vụ, không lấy mặc định 0,5.** Bài toán giữ chân thì bỏ sót khách
  sắp rời tốn kém hơn gọi nhầm một khách vẫn đang ở lại, nên tôi đặt ràng buộc recall ≥ 0,70 rồi mới
  dò ra ngưỡng 0,475 — chấp nhận precision 0,513.
- **Chống rò rỉ dữ liệu.** Preprocessor chỉ `fit` trên tập train rồi mới `transform` cho val/test.
  Split stratified 70/15/15, `random_state=42`, chạy lại ra đúng con số cũ.
- **Giữ lại kết quả âm tính.** SMOTE *không* cải thiện so với `class_weight` ở mức mất cân bằng này.
  Tôi ghi thẳng vào báo cáo thay vì lược đi cho đẹp — biết một kỹ thuật *không* hiệu quả ở đâu cũng là kết quả.

<br>

### Computer Vision — Phát hiện cháy thời gian thực

<a href="https://github.com/17tuanphamanh/YOLOv8n-FireDetection"><img src="https://img.shields.io/badge/YOLOv8n--FireDetection-181717?style=flat-square&logo=github&logoColor=white"></a>

Nhận diện lửa và khói từ camera IP bằng **YOLOv8n**, dashboard Tkinter toàn màn hình, cảnh báo Telegram
kèm ảnh có bounding box. Ba quyết định thiết kế xuất phát từ chuyện chạy thật:

- **Cảnh báo theo chuyển trạng thái, không theo khung hình.** Bắn mỗi khung thì một đám cháy 10 giây
  tạo ra hàng trăm tin nhắn. Chỉ gửi khi trạng thái chuyển `An toàn → Nguy hiểm`, cộng cooldown 20 giây.
- **Inference chạy thread riêng** tách khỏi luồng giao diện, nên UI không đứng hình mỗi lần model xử lý.
- **Ngưỡng `conf=0.7` đặt cao có chủ đích** — đổi một chút recall lấy việc giảm mạnh báo động giả,
  vì lửa thật xuất hiện liên tục qua nhiều khung chứ không chỉ một.

<br>

### Regression — Dự đoán giá nhà (Kaggle)

<a href="https://github.com/17tuanphamanh/House-Price-Prediction-using-Linear-Regression"><img src="https://img.shields.io/badge/House--Price--Prediction-181717?style=flat-square&logo=github&logoColor=white"></a>

*House Prices – Advanced Regression Techniques*, 80+ feature. Đi từ Linear Regression làm baseline
(CV RMSE ~36.000) rồi so sánh Ridge, Lasso, Random Forest và XGBoost. Tuning bằng `GridSearchCV`,
pipeline sklearn dựng theo module.

<br>

---

<div align="center">

# 🗄 Data Engineering

</div>

Phần ít được khoe nhưng chiếm nhiều thời gian nhất trong cả hai mảng trên:

<table>
<tr>
<td width="34%"><b>Pipeline dữ liệu reproducible</b></td>
<td>
Quy trình 8 bước từ raw snapshot → schema validation → khử trùng lặp → làm sạch → chọn feature →
feature engineering → stratified split → xuất dữ liệu. <b>17 feature từ 14 cột gốc</b>,
<code>random_state=42</code>, chạy lại cho ra đúng kết quả cũ.
</td>
</tr>
<tr>
<td><b>Thiết kế & tiến hoá schema</b></td>
<td>
<b>78 migration Alembic</b> trên PostgreSQL cho một sản phẩm đang chạy — thêm bảng, đổi tên,
gộp nhiều head, đổi khoá ngoại sang <code>SET NULL</code>, gỡ bảng đã bỏ. Đây là kinh nghiệm
sửa cơ sở dữ liệu <i>khi đã có dữ liệu thật bên trong</i>, khác hẳn dựng schema từ số 0.
</td>
</tr>
<tr>
<td><b>Analytics & observability</b></td>
<td>
Bảng analytics tổng hợp theo ngày, audit schema ghi vết thao tác, theo dõi usage và
phân loại lỗi của từng lời gọi AI, quota theo key theo ngày.
</td>
</tr>
</table>

<br>

---

<div align="center">

# ⚙️ Ngoài AI — Backend

</div>

### Hệ thống đặt món trước & POS

<a href="https://github.com/17tuanphamanh/swp301-block"><img src="https://img.shields.io/badge/swp301--block-181717?style=flat-square&logo=github&logoColor=white"></a>

`Java 17` · `Servlet 4` · `JSTL` · `SQL Server (JDBC thuần)` · `Tomcat 9` · `Maven` · `HikariCP` · `bcrypt` · `ZXing`

**Cố ý không dùng framework** — controller, DAO và view viết tay hết, để nắm chắc MVC ba tầng vận hành thế nào.

Điểm nghiệp vụ đáng nói: đơn đặt trước *không* xuống bếp ngay khi thanh toán. Hệ thống giữ đơn lại và
chỉ đẩy xuống bếp **trước giờ khách hẹn đúng 20 phút** — đủ để món vừa xong khi khách tới, không sớm
tới mức nguội. Có xử lý thanh toán trùng (idempotency) và 4 vai trò: khách, thu ngân, bếp, quản trị.

<br>

---

<div align="center">

# 🛠 Công nghệ

<img src="https://skillicons.dev/icons?i=python,fastapi,postgres,redis,docker,githubactions,sklearn,opencv,ts,nextjs,react,tailwind,java,git,vercel&perline=8&theme=dark" alt="Tech stack">

</div>

<table>
<tr>
  <td width="21%"><b>🧠 AI / LLM</b></td>
  <td>
  <code>anthropic</code> · <code>openai</code> · <code>google-generativeai</code> · DeepSeek —
  dispatch đa nhà cung cấp · <b>structured output theo JSON schema</b> · prompt tách khỏi logic chain ·
  định tuyến theo tier chi phí · đo <code>tokens_in</code>/<code>tokens_out</code> và quy ra cost USD ·
  quota theo từng key theo ngày · phân loại lỗi 8 nhóm và suy giảm có kiểm soát khi provider hỏng
  </td>
</tr>
<tr>
  <td><b>📊 ML & Computer Vision</b></td>
  <td>
  scikit-learn · XGBoost · <b>SHAP</b> · Ultralytics YOLOv8 · OpenCV · pandas · NumPy ·
  SMOTE và <code>class_weight</code> cho dữ liệu mất cân bằng · <code>GridSearchCV</code> ·
  chọn ngưỡng theo mục tiêu nghiệp vụ thay vì lấy mặc định 0,5
  </td>
</tr>
<tr>
  <td><b>🗄 Dữ liệu</b></td>
  <td>
  PostgreSQL · SQL Server · <b>SQLAlchemy</b> (async qua <code>asyncpg</code>) ·
  <b>Alembic — 78 migration</b> trên sản phẩm đang chạy, gồm gộp nhiều head và đổi khoá ngoại sang <code>SET NULL</code> ·
  Redis · pipeline chống rò rỉ dữ liệu · stratified split · feature engineering
  </td>
</tr>
<tr>
  <td><b>⚙️ Backend</b></td>
  <td>
  <b>FastAPI</b> · Python 3.12 · uvicorn + uvloop · Pydantic v2 và <code>pydantic-settings</code> ·
  JWT qua <code>python-jose</code> kèm <code>token_version</code> để thu hồi token · bcrypt/passlib ·
  <b>rate limiting bằng slowapi</b> · CORS và GZip middleware · scheduler chạy nền ·
  xử lý riêng lỗi mất kết nối DB để vẫn trả về đúng CORS header · Java 17 Servlet + JSTL
  </td>
</tr>
<tr>
  <td><b>🎨 Frontend</b></td>
  <td>
  <b>Next.js 14 App Router</b> · React · TypeScript · Tailwind CSS · Zustand ·
  Framer Motion · react-markdown · axios · dark mode theo <code>prefers-color-scheme</code>
  </td>
</tr>
<tr>
  <td><b>🧪 Kiểm thử</b></td>
  <td>
  <b>Playwright</b> (E2E) · <b>Vitest</b> · React Testing Library · <b>MSW</b> để mock tầng API ·
  jsdom · <b>20 file test</b> phủ auth, ví, thanh toán, notification, admin và các hàm tiện ích
  </td>
</tr>
<tr>
  <td><b>🚀 DevOps & Observability</b></td>
  <td>
  Docker · docker-compose · Vercel · Render ·
  <b>GitHub Actions</b> — frontend chạy typecheck → unit test → production build;
  backend <b>dựng schema bằng đúng entrypoint deploy</b> rồi mới chạy test, nên CI xanh
  đồng nghĩa với deploy chạy được · <b>Sentry</b> error tracking kèm performance tracing
  </td>
</tr>
</table>

> Mọi mục ở trên đều lấy từ code đang chạy, không phải từ danh sách "đã từng nghe qua".

<br>

---

<div align="center">

## 📬 Liên hệ

### Đang tìm vị trí **AI Engineer · Machine Learning Engineer · Data Scientist**

<a href="mailto:phamtuana160324@gmail.com">
  <img src="https://img.shields.io/badge/Gmail-phamtuana160324@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0B1120">
</a>
<a href="https://www.voca.io.vn">
  <img src="https://img.shields.io/badge/Website-voca.io.vn-2563EB?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=0B1120">
</a>

📍 Hà Nội, Việt Nam

</div>
