# Knowing-Doing Gap trong Khoa học Máy tính

Nghiên cứu nghịch lý: **Người làm CS hiểu AI, dùng AI hàng ngày, nhưng không muốn AI thay thế công việc.**

70% nhân sự IT dùng AI hàng ngày/tuần, nhưng mức sẵn sàng giao việc cho AI chỉ đạt **3.14/5**.

## Chạy ứng dụng

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dữ liệu

Bộ dữ liệu **O*NET WorkBank** — khảo sát thực tế với 240 nhân sự IT và 16 chuyên gia, đánh giá 205 tác vụ trên 21 ngành CS.

| File | Nội dung | Số dòng |
|---|---|---|
| `domain_worker_desires.csv` | Người lao động đánh giá: "Muốn AI làm thay?" | 5,731 |
| `domain_worker_metadata.csv` | Thông tin cá nhân: kinh nghiệm, thu nhập, thái độ AI | 1,500 |
| `expert_rated_technological_capability.csv` | Chuyên gia đánh giá: "AI có làm được?" | 2,057 |
| `task_statement_with_metadata.csv` | Mô tả chi tiết từng tác vụ công việc | 2,131 |

## Kết quả chính

| Chỉ số | Điểm |
|---|---|
| Người chịu giao cho AI | 3.14/5 |
| AI thực sự làm được | 3.43/5 |
| **Phần AI bị lãng phí** | **0.29** |

## Nội dung Dashboard

### 1. Quy mô khảo sát
Tổng quan dataset: số người, số tác vụ, top 10 ngành.

### 2. AI làm được bao nhiêu vs Người chịu giao bao nhiêu?
- Bar chart so sánh 15 ngành
- Ma trận 4 nhóm chiến lược (Sẵn sàng / Rào cản tâm lý / Cần nâng cấp AI / Vùng lõi con người)

### 3. Tại sao người ta không chịu giao việc cho AI?
5 nguyên nhân gốc rễ:
1. **Sợ AI** — Dùng AI nhiều + Sợ (2.86/5) < Dùng ít + Không sợ (3.06/5)
2. **Muốn giữ quyền kiểm soát** — Người lo mất kiểm soát chỉ giao 2.99/5
3. **Nhóm 6-10 năm kinh nghiệm** — Sợ nhất (30% lo AI gây khổ), chưa ổn định tài chính
4. **Việc "định nghĩa nghề"** — Việc càng cần chuyên môn sâu thì càng không giao cho AI
5. **Lương trung bình (60-86K)** — Lo nhất (33%), đủ để mất nhưng chưa đủ để an tâm

### 4. Đề xuất AI Agent
Bảng khuyến nghị mô hình AI trợ lý cho 14 vị trí chuyên môn.

## Tài liệu

- [`BAI_PHAN_TICH.md`](BAI_PHAN_TICH.md) — Báo cáo phân tích chi tiết
- [`KY_THUAT.md`](KY_THUAT.md) — Tài liệu kỹ thuật: code, sơ đồ luồng, phương pháp

## Kết luận

> Rào cản lớn nhất của AI không phải là công nghệ — mà là tâm lý con người.
> Không phải cứ giao hết cho AI là tốt — mà phải giao **đúng việc, đúng người, đúng lúc**.
