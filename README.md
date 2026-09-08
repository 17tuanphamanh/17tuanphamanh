<div align="center">

# Phạm Tuấn Anh

**Full-stack & Machine Learning Developer** · Hà Nội, Việt Nam

Tôi xây sản phẩm chạy thật, có người dùng thật — không dừng ở notebook.

[![Website](https://img.shields.io/badge/Sản_phẩm_đang_chạy-voca.io.vn-0A66C2?style=for-the-badge)](https://www.voca.io.vn)
[![Email](https://img.shields.io/badge/Email-phamtuana160324@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:phamtuana160324@gmail.com)

</div>

---

## 🚀 VOCA — Nền tảng hướng nghiệp · **đang chạy production**

### 🔗 **[www.voca.io.vn](https://www.voca.io.vn)**

Nền tảng hướng nghiệp cho học sinh - sinh viên: đánh giá năng lực, gợi ý ngành học,
đặt lịch tư vấn với mentor và xây lộ trình sự nghiệp. Tên miền riêng, có Google Analytics,
có điều khoản - chính sách bảo mật - chính sách hoàn tiền. **Một sản phẩm hoàn chỉnh, không phải đồ án.**

**Bốn mảng sản phẩm:** Hành trình Ikigai · Trợ lý hướng nghiệp AI · Sàn Mentor · Gói thành viên

<table>
<tr><td><b>Frontend</b></td><td>Next.js 14 (App Router) · TypeScript · Zustand · Tailwind CSS · dark mode · SSR</td></tr>
<tr><td><b>Backend</b></td><td>FastAPI · PostgreSQL · SQLAlchemy · Alembic · JWT auth</td></tr>
<tr><td><b>Hạ tầng</b></td><td>Docker · docker-compose · Render · Vercel · 3 workflow GitHub Actions (CI, keepalive, migrate DB)</td></tr>
<tr><td><b>Quy mô</b></td><td><b>824 file</b> · 378 frontend · 317 backend · <b>78 migration Alembic</b></td></tr>
</table>

**Những bài toán khó tôi đã phải tự giải trong dự án này:**

| Bài toán | Cách xử lý |
|---|---|
| 💳 **Thanh toán & chi trả** | Payment transaction, payout cho mentor, thông tin ngân hàng, luồng rút tiền, coupon |
| ⚖️ **Tranh chấp booking** | Bảng dispute riêng, cho đính kèm bằng chứng, admin note, phạt huỷ lịch phía chuyên gia |
| 🕐 **Lịch hẹn đa múi giờ** | Booking gắn timezone, buffer & time-off của mentor, group session giới hạn số người |
| 🔐 **Xác thực & phân quyền** | JWT + `token_version` để thu hồi token, xác thực email, 4 vai trò (học viên / mentor / chuyên gia / admin) |
| 📊 **Vận hành** | Audit schema, analytics theo ngày, hệ thống báo cáo nội dung, notification, chat |

> Repo hiện để private. Cần xem code khi phỏng vấn, tôi sẵn sàng mở quyền truy cập — cứ email cho tôi.

---

## 🤖 Machine Learning

### Explainable ML — Dự đoán khách hàng rời bỏ
**[`churn-explainable-ml`](https://github.com/17tuanphamanh/churn-explainable-ml)** · **[`Churn_Data_Processing`](https://github.com/17tuanphamanh/Churn_Data_Processing)**

Dự đoán churn trên 10.000 hồ sơ khách hàng ngân hàng (churn rate 20,37%), rồi dùng SHAP để giải thích
mô hình dựa vào đâu mà quyết định — mục tiêu cuối là **playbook giữ chân theo từng phân khúc**, không dừng ở accuracy.

| Chỉ số | Kết quả |
|---|---|
| Mô hình tốt nhất | HistGradientBoosting + `class_weight` |
| Test PR-AUC / ROC-AUC | **0,674 / 0,846** |
| Ngưỡng theo recall ≥ 0,70 | 0,475 → Recall **0,690** · Precision 0,513 · F1 0,589 |
| Yếu tố chi phối (SHAP) | Age > NumOfProducts > Geography |

Hai điểm tôi làm kỹ:
- **Chống rò rỉ dữ liệu:** preprocessor chỉ `fit` trên train rồi mới `transform` cho val/test. Split stratified 70/15/15, `random_state=42`, chạy lại ra đúng số cũ.
- **Giữ lại kết quả âm tính:** SMOTE *không* cải thiện so với `class_weight` ở mức mất cân bằng này. Tôi ghi thẳng vào báo cáo thay vì bỏ đi cho đẹp.

### Phát hiện cháy thời gian thực
**[`YOLOv8n-FireDetection`](https://github.com/17tuanphamanh/YOLOv8n-FireDetection)**

Nhận diện lửa và khói từ camera IP bằng YOLOv8n, dashboard Tkinter toàn màn hình, cảnh báo Telegram
kèm ảnh có bounding box. Luồng nhận diện chạy thread riêng tách khỏi luồng giao diện để UI không đứng hình.
Cảnh báo bắn theo **chuyển trạng thái** An toàn → Nguy hiểm chứ không bắn mỗi khung hình, cộng cooldown 20 giây.

`Python` · `Ultralytics YOLOv8` · `OpenCV` · `Tkinter` · `Telegram Bot API` · `threading`

### Dự đoán giá nhà — Kaggle
**[`House-Price-Prediction-using-Linear-Regression`](https://github.com/17tuanphamanh/House-Price-Prediction-using-Linear-Regression)**

*House Prices – Advanced Regression Techniques*, 80+ feature. Đi từ Linear Regression làm baseline
(CV RMSE ~36.000) rồi so sánh Ridge, Lasso, Random Forest, XGBoost. Tuning bằng `GridSearchCV`,
pipeline sklearn dựng theo module.

---

## ☕ Backend Java

### Hệ thống đặt món trước & POS
**[`swp301-block`](https://github.com/17tuanphamanh/swp301-block)**

`Java 17` · `Servlet 4` · `JSTL` · `SQL Server (JDBC thuần)` · `Tomcat 9` · `Maven` · `HikariCP` · `bcrypt` · `ZXing`

**Cố ý không dùng framework** — controller, DAO và view viết tay hết để nắm chắc MVC ba tầng vận hành thế nào.

Điểm nghiệp vụ đáng nói: đơn đặt trước *không* xuống bếp ngay khi thanh toán. Hệ thống giữ đơn lại,
chỉ đẩy xuống bếp **trước giờ khách hẹn đúng 20 phút** — đủ để món vừa xong khi khách tới, không sớm tới mức nguội.
Có xử lý thanh toán trùng (idempotency) và 4 vai trò: khách, thu ngân, bếp, quản trị.

---

## 🛠 Công nghệ

| | |
|---|---|
| **Ngôn ngữ** | Python · TypeScript · Java · SQL |
| **Frontend** | Next.js 14 · React · Tailwind CSS · Zustand |
| **Backend** | FastAPI · SQLAlchemy · Alembic · Java Servlet · JWT |
| **Cơ sở dữ liệu** | PostgreSQL · SQL Server |
| **ML / DL** | scikit-learn · XGBoost · SHAP · Ultralytics YOLO · OpenCV · pandas · NumPy |
| **DevOps** | Docker · GitHub Actions · Vercel · Render · Alembic migration |

---

<div align="center">

### 📬 Liên hệ

Đang tìm vị trí **Full-stack Developer**, **AI/ML Engineer** hoặc **Backend Developer**

📍 Hà Nội &nbsp;·&nbsp; 📧 **[phamtuana160324@gmail.com](mailto:phamtuana160324@gmail.com)** &nbsp;·&nbsp; 🌐 **[www.voca.io.vn](https://www.voca.io.vn)**

</div>
