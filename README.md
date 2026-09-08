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

</div>

<br>

Nền tảng hướng nghiệp cho học sinh THPT và sinh viên: trắc nghiệm đánh giá năng lực, trợ lý AI,
gợi ý trường - ngành và đặt lịch tư vấn với mentor. Tên miền riêng, Google Analytics, đầy đủ điều khoản
sử dụng - chính sách bảo mật - chính sách hoàn tiền. Tôi làm cả backend, frontend, hạ tầng và toàn bộ tầng AI.

<table>
<tr><td width="17%"><b>Quy mô</b></td><td><b>824 file · ~107.000 dòng code</b> — 310 file Python backend, 300 file TypeScript/TSX frontend, <b>75 migration Alembic</b>, 19 domain nghiệp vụ</td></tr>
<tr><td><b>AI</b></td><td>Anthropic · OpenAI · Google Gemini · DeepSeek — dispatch đa nhà cung cấp, agent có tool, structured output</td></tr>
<tr><td><b>Backend</b></td><td>FastAPI · PostgreSQL · SQLAlchemy async · Alembic · Redis · WebSocket · JWT</td></tr>
<tr><td><b>Frontend</b></td><td>Next.js 14 App Router · TypeScript · Zustand · Tailwind CSS</td></tr>
<tr><td><b>Hạ tầng</b></td><td>Docker · Render · Vercel · GitHub Actions · Sentry</td></tr>
</table>

> 🔒 Repo để private vì đây là sản phẩm đang phục vụ người dùng. Cần xem code khi phỏng vấn, tôi mở quyền truy cập ngay — cứ email cho tôi.

<br>

---

<div align="center">

# 🧠 Generative AI — tầng `ai_core`

</div>

Tôi tự viết module `ai_core` làm tầng trung gian giữa sản phẩm và các nhà cung cấp LLM.
Đây là phần tôi tâm đắc nhất, vì nó giải quyết đúng những vấn đề chỉ lộ ra khi hệ thống chạy thật.

<div align="center">
  <img src="assets/ai-core.png" alt="Kiến trúc ai_core — routing theo tier, structured output, tính chi phí, phân loại lỗi" width="100%">
</div>

### Bốn vấn đề thật và cách tôi xử lý

<table>
<tr>
<td width="27%"><b>💸 Chi phí LLM<br>không kiểm soát được</b></td>
<td>
Chia tác vụ theo <b>tier</b>: việc khối lượng lớn, ít rủi ro (chẩn đoán nhanh, chat theo dõi, diễn giải
kết quả) đi <b>DeepSeek</b>; việc quan trọng, mỗi phiên chỉ chạy một lần (lời khuyên cuối, tường thuật
ma trận năng lực) mới dùng <b>Anthropic Opus</b>. Đây là <i>soft preference</i> — thiếu key thì tự lùi
sang key khác rồi tới key môi trường, nên deployment cấu hình dở dang vẫn chạy.
</td>
</tr>
<tr>
<td><b>📉 Không biết mỗi<br>request tốn bao nhiêu</b></td>
<td>
Bảng giá USD/1.000 token cho <b>13 model</b> của 4 nhà cung cấp. Mỗi lời gọi ghi lại
<code>tokens_in</code>, <code>tokens_out</code> và cost vào sổ cái <code>AIUsageLog</code>, tách theo
<b>người dùng · tính năng · provider · model</b>. Model lạ ngoài bảng thì <b>lùi về mức giá thận trọng</b>
chứ không ghi cost bằng 0 — tôi không muốn hoá đơn bất ngờ vì một model chưa kịp cập nhật giá.
</td>
</tr>
<tr>
<td><b>🕳 Fallback im lặng —<br>lỗi khó chịu nhất</b></td>
<td>
Trước đây gọi model hỏng là hệ thống lặng lẽ trả về dữ liệu mock. Người dùng cắm API key xong vẫn thấy
kết quả demo mà <b>không hiểu tại sao</b>. Giờ lỗi được phân thành 8 nhóm —
<code>sdk_missing</code> · <code>auth</code> · <code>quota</code> · <code>rate_limit</code> ·
<code>bad_model</code> · <code>bad_request</code> · <code>parse</code> · <code>network</code> —
ghi vào sổ cái và trả lý do lên tận giao diện quản trị.
</td>
</tr>
<tr>
<td><b>🔓 Output tự do<br>làm vỡ backend</b></td>
<td>
Mọi lời gọi đi qua một hàm chung với <b>output ràng buộc theo JSON schema</b>, nên tầng dưới luôn nhận
đúng cấu trúc đã định. Kèm <b>quota theo từng key theo ngày</b>, và prompt tách hẳn khỏi logic chain
(<code>ai_core/prompts/</code>) để sửa prompt không phải đụng vào code xử lý.
</td>
</tr>
</table>

**Chín chain đang phục vụ người dùng:** `career_recommender` · `school_recommender` · `roadmap_generator` ·
`profile_analyzer` · `expert_matcher` · `expert_review` · `consultation` · `advisor` · `base`

<br>

---

<div align="center">

# 🤖 AI Agent — tự gọi tool, vừa chạy vừa trả lời

</div>

Chain `advisor` không chỉ sinh chữ. Nó là một **agent có công cụ**: model tự quyết định cần tra dữ liệu gì,
gọi tool, đọc kết quả, rồi vòng lại cho tới khi đủ thông tin mới trả lời.

<div align="center">
  <img src="assets/ai-agent.png" alt="Agent loop — function calling, streaming, 6 tool, giới hạn 5 vòng lặp" width="100%">
</div>

- **Stream và tool use chạy đồng thời.** Chữ được đẩy ra cho người dùng đọc *ngay trong lúc* model vẫn đang
  cân nhắc gọi tool. Nếu chờ agent chạy xong hết mới trả về thì người dùng ngồi nhìn màn hình trống mất nhiều giây.
- **Vòng lặp có trần cứng.** `MAX_TOOL_ITERS = 5` — một agent không giới hạn có thể quay vòng vô hạn và đốt sạch token.
- **Neo câu trả lời vào dữ liệu thật.** Sáu tool đọc thẳng PostgreSQL (nghề, ngành, trường, điểm chuẩn, hồ sơ
  người dùng) cộng một tool tìm web **bắt buộc trích nguồn**. Đây là cách chặn model bịa tên ngành hay bịa điểm
  chuẩn — vấn đề chí mạng của một sản phẩm tư vấn hướng nghiệp.
- **Viết cho cả hai nhà cung cấp.** Cùng bộ tool được khai báo lại theo định dạng riêng của Anthropic và của OpenAI.

<br>

---

<div align="center">

# ⚡ Vài chỗ khó khác trong hệ thống

</div>

<table>
<tr>
<td width="27%"><b>🔌 WebSocket scale ngang</b></td>
<td>
Chat và notification chạy trên WebSocket. Vấn đề: khi có nhiều instance, người dùng nối vào instance B
sẽ không nhận được tin nhắn sinh ra ở instance A. Tôi giải bằng <b>Redis pub/sub fan-out</b> — instance
tạo tin <i>chỉ publish</i>, không tự gửi cục bộ; listener trên mọi instance kể cả chính nó mới lo phần gửi.
Nhờ vậy mỗi socket nhận <b>đúng một lần</b>. Tắt Redis thì tự lùi về quản lý trong bộ nhớ, đủ dùng cho môi trường dev.
</td>
</tr>
<tr>
<td><b>💳 Cổng thanh toán SePay</b></td>
<td>
Tích hợp thanh toán QR, <b>xác thực webhook bằng chữ ký HMAC</b> để không ai giả được thông báo
"đã thanh toán". Có xử lý giao dịch trùng, payout cho mentor, hoàn tiền và luồng rút tiền.
</td>
</tr>
<tr>
<td><b>📅 Google Calendar</b></td>
<td>
Đồng bộ lịch hẹn qua <b>OAuth2 + Calendar API v3 gọi REST trực tiếp bằng <code>httpx</code></b>,
không kéo thêm thư viện client của Google. Toàn bộ tính năng nằm sau một cổng kiểm tra cấu hình —
thiếu credentials thì mọi lối vào thành no-op an toàn, nền tảng chạy y nguyên. Có sinh file <code>.ics</code> kèm theo.
</td>
</tr>
<tr>
<td><b>🎙 Hệ thống giọng nói</b></td>
<td>
Đọc câu trả lời bằng <code>speechSynthesis</code> và nhập liệu bằng giọng nói qua <code>SpeechRecognition</code>.
Tầng STT thiết kế theo <b>provider cắm rời</b>: một provider dùng sẵn API trình duyệt, một provider chạy
<b>Whisper trên WebAssembly ngay trong trình duyệt</b>. Có dò khả năng thiết bị (WebAssembly, WebGPU) và
an toàn với SSR — trên server mọi thứ trả về false nên import ở đâu cũng được.
</td>
</tr>
</table>

<br>

---

<div align="center">

# 📊 Machine Learning & Computer Vision

</div>

### Explainable ML — Dự đoán khách hàng rời bỏ

<a href="https://github.com/17tuanphamanh/churn-explainable-ml"><img src="https://img.shields.io/badge/churn--explainable--ml-181717?style=flat-square&logo=github&logoColor=white"></a>
<a href="https://github.com/17tuanphamanh/Churn_Data_Processing"><img src="https://img.shields.io/badge/Churn__Data__Processing-181717?style=flat-square&logo=github&logoColor=white"></a>

Dự đoán churn trên **10.000 hồ sơ khách hàng ngân hàng** (churn rate 20,37%), rồi dùng **SHAP** để giải thích
mô hình dựa vào đâu mà quyết định. Đích đến là **playbook giữ chân theo từng phân khúc** — mô hình phải nói
được *nên làm gì*, chứ không chỉ đưa ra một con số.

<table>
<tr><td width="34%">Mô hình tốt nhất</td><td>HistGradientBoosting + <code>class_weight</code></td></tr>
<tr><td>Test PR-AUC / ROC-AUC</td><td><b>0,674 / 0,846</b></td></tr>
<tr><td>Ngưỡng chọn theo recall ≥ 0,70</td><td>0,475 → Recall <b>0,690</b> · Precision 0,513 · F1 0,589</td></tr>
<tr><td>Yếu tố chi phối (SHAP)</td><td>Age &gt; NumOfProducts &gt; Geography</td></tr>
</table>

- **Chọn ngưỡng theo mục tiêu nghiệp vụ, không lấy mặc định 0,5.** Bài toán giữ chân thì bỏ sót khách sắp rời
  tốn kém hơn gọi nhầm một khách vẫn đang ở lại, nên tôi đặt ràng buộc recall ≥ 0,70 rồi mới dò ra ngưỡng 0,475.
- **Chống rò rỉ dữ liệu.** Preprocessor chỉ `fit` trên tập train rồi mới `transform` cho val/test.
  Split stratified 70/15/15, `random_state=42`, chạy lại ra đúng con số cũ.
- **Giữ lại kết quả âm tính.** SMOTE *không* cải thiện so với `class_weight` ở mức mất cân bằng này.
  Tôi ghi thẳng vào báo cáo thay vì lược đi cho đẹp — biết một kỹ thuật *không* hiệu quả ở đâu cũng là kết quả.

### Computer Vision — Phát hiện cháy thời gian thực

<a href="https://github.com/17tuanphamanh/YOLOv8n-FireDetection"><img src="https://img.shields.io/badge/YOLOv8n--FireDetection-181717?style=flat-square&logo=github&logoColor=white"></a>

Nhận diện lửa và khói từ camera IP bằng **YOLOv8n**, dashboard toàn màn hình, cảnh báo Telegram kèm ảnh có
bounding box. Ba quyết định xuất phát từ chuyện chạy thật:

- **Cảnh báo theo chuyển trạng thái, không theo khung hình.** Bắn mỗi khung thì một đám cháy 10 giây tạo ra
  hàng trăm tin nhắn. Chỉ gửi khi trạng thái chuyển `An toàn → Nguy hiểm`, cộng cooldown 20 giây.
- **Inference chạy thread riêng** tách khỏi luồng giao diện, nên UI không đứng hình mỗi lần model xử lý.
- **Ngưỡng `conf=0.7` đặt cao có chủ đích** — đổi một chút recall lấy việc giảm mạnh báo động giả, vì lửa thật
  xuất hiện liên tục qua nhiều khung chứ không chỉ một.

### Regression — Dự đoán giá nhà (Kaggle)

<a href="https://github.com/17tuanphamanh/House-Price-Prediction-using-Linear-Regression"><img src="https://img.shields.io/badge/House--Price--Prediction-181717?style=flat-square&logo=github&logoColor=white"></a>

*House Prices – Advanced Regression Techniques*, 80+ feature. Đi từ Linear Regression làm baseline
(CV RMSE ~36.000) rồi so sánh Ridge, Lasso, Random Forest và XGBoost. Tuning bằng `GridSearchCV`.

<br>

---

<div align="center">

# 🗄 Data Engineering

</div>

<table>
<tr>
<td width="27%"><b>Pipeline dữ liệu reproducible</b></td>
<td>Quy trình 8 bước: raw snapshot → schema validation → khử trùng lặp → làm sạch → chọn feature → feature engineering → stratified split → xuất dữ liệu. <b>17 feature từ 14 cột gốc</b>, <code>random_state=42</code>, chạy lại cho ra đúng kết quả cũ.</td>
</tr>
<tr>
<td><b>Thiết kế & tiến hoá schema</b></td>
<td><b>75 migration Alembic</b> trên PostgreSQL của một sản phẩm đang chạy — thêm bảng, đổi tên, gộp nhiều head, đổi khoá ngoại sang <code>SET NULL</code>, gỡ bảng đã bỏ. Đây là kinh nghiệm sửa cơ sở dữ liệu <i>khi đã có dữ liệu thật bên trong</i>, khác hẳn dựng schema từ số 0.</td>
</tr>
<tr>
<td><b>Analytics & observability</b></td>
<td>Bảng analytics tổng hợp theo ngày, audit schema ghi vết thao tác, sổ cái usage và chi phí của từng lời gọi AI, xuất dữ liệu ra CSV, Sentry theo dõi lỗi và hiệu năng.</td>
</tr>
</table>

<br>

---

<div align="center">

# ⚙️ Backend Java — không dùng framework

</div>

<a href="https://github.com/17tuanphamanh/swp301-block"><img src="https://img.shields.io/badge/swp301--block-181717?style=flat-square&logo=github&logoColor=white"></a>

`Java 17` · `Servlet 4` · `JSTL` · `SQL Server (JDBC thuần)` · `Tomcat 9` · `Maven` · `HikariCP` · `bcrypt` · `ZXing`

Hệ thống đặt món trước và bán hàng tại quầy. **Cố ý không dùng framework** — controller, DAO và view viết tay
hết, để nắm chắc MVC ba tầng vận hành thế nào.

Điểm nghiệp vụ đáng nói: đơn đặt trước *không* xuống bếp ngay khi thanh toán. Hệ thống giữ đơn lại và chỉ đẩy
xuống bếp **trước giờ khách hẹn đúng 20 phút** — đủ để món vừa xong khi khách tới, không sớm tới mức nguội.
Có xử lý thanh toán trùng và 4 vai trò: khách, thu ngân, bếp, quản trị.

<br>

---

<div align="center">

# 🛠 Công nghệ

<img src="https://skillicons.dev/icons?i=python,fastapi,postgres,redis,docker,githubactions,sklearn,opencv,ts,nextjs,react,tailwind,java,git,vercel&perline=8&theme=dark" alt="Tech stack">

</div>

<table>
<tr>
  <td width="21%"><b>🧠 Generative AI</b></td>
  <td>SDK <code>anthropic</code> · <code>openai</code> · <code>google-generativeai</code> · DeepSeek — sinh nội dung tiếng Việt có kiểm soát · <b>structured output ràng buộc theo JSON schema</b> · <b>prompt engineering</b> với prompt tách thành module riêng · system prompt theo từng tác vụ · <b>streaming</b> thời gian thực · trừu tượng hoá đa nhà cung cấp và chuyển đổi khi hỏng</td>
</tr>
<tr>
  <td><b>🤖 AI Agent & Tool Use</b></td>
  <td><b>Function calling</b> viết cho cả Anthropic lẫn OpenAI · vòng lặp agent có trần cứng (<code>MAX_TOOL_ITERS = 5</code>) · <b>6 tool</b> truy vấn PostgreSQL thật cùng một tool tìm web bắt buộc trích nguồn · <b>grounding</b> câu trả lời vào dữ liệu nội bộ để chặn bịa đặt · hội thoại nhiều lượt · chạy song song stream và tool use</td>
</tr>
<tr>
  <td><b>📈 LLM Ops</b></td>
  <td>Sổ cái <code>AIUsageLog</code> ghi từng lời gọi theo <b>người dùng · tính năng · provider · model</b> — <code>tokens_in</code>, <code>tokens_out</code>, <code>cost_usd</code>, thành công hay thất bại, thật hay mock · bảng giá 13 model · định tuyến theo tier chi phí · quota theo key theo ngày · <b>phân loại lỗi 8 nhóm</b> · suy giảm có kiểm soát</td>
</tr>
<tr>
  <td><b>👁 Computer Vision</b></td>
  <td><b>Ultralytics YOLOv8</b> · <b>OpenCV</b> — nhận diện <b>thời gian thực</b> từ camera IP · inference chạy thread riêng · tinh chỉnh ngưỡng <code>conf</code>/<code>iou</code> đánh đổi recall lấy việc giảm báo động giả · tính diện tích vùng cháy từ bounding box · cảnh báo theo chuyển trạng thái kèm cooldown</td>
</tr>
<tr>
  <td><b>📊 Machine Learning</b></td>
  <td>scikit-learn · XGBoost · <b>SHAP</b> (explainable AI) · pandas · NumPy · gradient boosting và ensemble · xử lý mất cân bằng bằng SMOTE và <code>class_weight</code> · <code>GridSearchCV</code> · <b>chọn ngưỡng theo mục tiêu nghiệp vụ</b> · đánh giá bằng PR-AUC / ROC-AUC / F1</td>
</tr>
<tr>
  <td><b>🗄 Dữ liệu</b></td>
  <td>PostgreSQL · SQL Server · <b>SQLAlchemy</b> async qua <code>asyncpg</code> · <b>Alembic — 75 migration</b> trên sản phẩm đang chạy · Redis (cache và pub/sub) · pipeline chống rò rỉ dữ liệu · stratified split · feature engineering · xuất CSV</td>
</tr>
<tr>
  <td><b>⚙️ Backend</b></td>
  <td><b>FastAPI</b> · Python 3.12 · uvicorn + uvloop · Pydantic v2 · <b>WebSocket có Redis pub/sub scale ngang</b> · JWT kèm <code>token_version</code> để thu hồi token · bcrypt · <b>rate limiting</b> · CORS và GZip middleware · scheduler chạy nền · <b>webhook ký HMAC</b> · OAuth2 (Google) · Java 17 Servlet + JSTL</td>
</tr>
<tr>
  <td><b>🎨 Frontend</b></td>
  <td><b>Next.js 14 App Router</b> · React · TypeScript · Tailwind CSS · Zustand · Framer Motion · react-markdown · dark mode theo <code>prefers-color-scheme</code> · <b>Web Speech API</b> (TTS và STT) · <b>Whisper chạy WebAssembly trong trình duyệt</b></td>
</tr>
<tr>
  <td><b>🧪 Kiểm thử</b></td>
  <td><b>Playwright</b> (E2E) · <b>Vitest</b> · React Testing Library · <b>MSW</b> để mock tầng API · jsdom · <b>17 file test</b> phủ auth, ví, thanh toán, notification, admin và các hàm tiện ích</td>
</tr>
<tr>
  <td><b>🚀 DevOps & Observability</b></td>
  <td>Docker · docker-compose · Vercel · Render · <b>GitHub Actions</b> — frontend chạy typecheck → unit test → production build; backend <b>dựng schema bằng đúng entrypoint deploy</b> rồi mới chạy test, nên CI xanh đồng nghĩa với deploy chạy được · <b>Sentry</b> error tracking kèm performance tracing</td>
</tr>
</table>

> Mọi mục ở trên đều lấy từ code đang chạy, không phải từ danh sách "đã từng nghe qua".

<br>

---

<div align="center">

## 📬 Liên hệ

### Đang tìm vị trí **AI Engineer · Machine Learning Engineer · Data Scientist**

<a href="mailto:phamtuana160324@gmail.com"><img src="https://img.shields.io/badge/Gmail-phamtuana160324@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0B1120"></a>
<a href="https://www.voca.io.vn"><img src="https://img.shields.io/badge/Website-voca.io.vn-2563EB?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=0B1120"></a>

📍 Hà Nội, Việt Nam

</div>
