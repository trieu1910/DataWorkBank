"""
Knowing-Doing Gap trong Khoa học Máy tính
Nghiên cứu: Người làm CS hiểu AI, dùng AI, nhưng không muốn AI thay thế mình.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# CẤU HÌNH
# ============================================================

st.set_page_config(page_title="Khoảng trống Ứng dụng AI", page_icon="🤖", layout="wide")

CS_OCCUPATIONS = [
    'Computer Hardware Engineers', 'Computer Network Architects',
    'Computer Network Support Specialists', 'Computer Programmers',
    'Computer Science Teachers, Postsecondary', 'Computer Systems Analysts',
    'Computer Systems Engineers/Architects', 'Computer User Support Specialists',
    'Computer and Information Research Scientists',
    'Computer and Information Systems Managers',
    'Data Entry Keyers', 'Data Warehousing Specialists',
    'Database Administrators', 'Database Architects',
    'Geographic Information Systems Technologists and Technicians',
    'Information Security Analysts', 'Information Technology Project Managers',
    'Network and Computer Systems Administrators',
    'Software Quality Assurance Analysts and Testers',
    'Web Administrators', 'Web Developers',
]

INCOME_ORDER = ['0-30K', '30-60K', '60-86K', '86K-165K', '165K-209K', '209K-529K', '529K+', 'Prefer not to say']
EXP_ORDER = ['Less than 1 year', '1-2 year', '3-5 years', '6-10 years', 'More than 10 years']

# ============================================================
# LOAD DỮ LIỆU
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    desires = pd.read_csv(os.path.join(BASE_DIR, "data", "domain_worker_desires.csv"))
    metadata = pd.read_csv(os.path.join(BASE_DIR, "data", "domain_worker_metadata.csv"))
    expert = pd.read_csv(os.path.join(BASE_DIR, "data", "expert_rated_technological_capability.csv"))
    tasks = pd.read_csv(os.path.join(BASE_DIR, "data", "task_statement_with_metadata.csv"))
    cs_d = desires[desires['Occupation (O*NET-SOC Title)'].isin(CS_OCCUPATIONS)]
    cs_m = metadata[metadata['Occupation (O*NET-SOC Title)'].isin(CS_OCCUPATIONS)]
    cs_e = expert[expert['Occupation (O*NET-SOC Title)'].isin(CS_OCCUPATIONS)]
    cs_t = tasks[tasks['Occupation (O*NET-SOC Title)'].isin(CS_OCCUPATIONS)]
    return cs_d, cs_m, cs_e, cs_t

cs_d, cs_m, cs_e, cs_t = load_data()

# ============================================================
# TÍNH TOÁN SỐ LIỆU CHÍNH
# ============================================================

desire = cs_d.groupby('Occupation (O*NET-SOC Title)')['Automation Desire Rating'].mean()
capacity = cs_e.groupby('Occupation (O*NET-SOC Title)')['Automation Capacity Rating'].mean()

df = pd.DataFrame({'Ky_Vong': desire, 'Nang_Luc': capacity}).dropna()
df['Chenh_Lech'] = df['Nang_Luc'] - df['Ky_Vong']

avg_d, avg_c = df['Ky_Vong'].mean(), df['Nang_Luc'].mean()
avg_gap = df['Chenh_Lech'].mean()

def phan_loai_chien_luoc(row):
    if row['Ky_Vong'] >= avg_d and row['Nang_Luc'] >= avg_c:
        return 'Sẵn sàng triển khai'
    elif row['Ky_Vong'] < avg_d and row['Nang_Luc'] >= avg_c:
        return 'Rào cản tâm lý'
    elif row['Ky_Vong'] >= avg_d and row['Nang_Luc'] < avg_c:
        return 'Cần nâng cấp AI'
    else:
        return 'Vùng lõi của con người'

df['Nhom_Chien_Luoc'] = df.apply(phan_loai_chien_luoc, axis=1)

# ============================================================
# TIÊU ĐỀ
# ============================================================

st.title("🤖 Khoảng trống Ứng dụng AI trong ngành Công nghệ")

merged_all = cs_d.merge(cs_m, on='User ID', suffixes=('', '_m'))
total_users = merged_all['User ID'].nunique()
daily_weekly = merged_all[merged_all['LLM Use in Work'].isin([
    'Yes, I use them every day in my work.', 'Yes, I use them every week in my work.'
])]['User ID'].nunique()
pct_use = daily_weekly / total_users * 100

st.markdown(f"**Nghịch lý thực tế:** {pct_use:.0f}% nhân sự IT sử dụng AI hàng ngày/tuần, nhưng mức độ sẵn sàng giao việc cho AI chỉ đạt {avg_d:.2f}/5 điểm.")
st.markdown("---")

# ============================================================
# SECTION 1: DỮ LIỆU
# ============================================================

st.header("1. Quy mô khảo sát")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Số nhân sự tham gia", f"{cs_d['User ID'].nunique()}")
c2.metric("Số lượng tác vụ", f"{cs_t['Task ID'].nunique()}")
c3.metric("Vị trí chuyên môn", f"{len(df)}")
c4.metric("Chuyên gia đánh giá", f"{cs_e['User ID'].nunique()}")

st.markdown("### Top 10 ngành CS (theo số đánh giá)")
top = cs_d['Occupation (O*NET-SOC Title)'].value_counts().head(10)
st.dataframe(top.rename("Số đánh giá").to_frame(), use_container_width=True)

st.markdown("---")

# ============================================================
# SECTION 2: KNOWING-DOING GAP (TRỌNG TÂM)
# ============================================================

st.header("2. AI làm được bao nhiêu vs Người chịu giao bao nhiêu?")

c1, c2, c3 = st.columns(3)
c1.metric("Người chịu giao cho AI", f"{avg_d:.2f}/5", help="Mức độ người lao động sẵn sàng để AI làm thay việc của mình")
c2.metric("AI thực sự làm được", f"{avg_c:.2f}/5", help="Chuyên gia đánh giá AI có khả năng tự động hóa ở mức nào")
c3.metric("Phần AI bị lãng phí", f"{avg_gap:.2f}", help="AI làm được nhiều hơn mức người ta chịu giao — đây là phần bị bỏ phí")

st.info(f"**Tóm lại:** AI được chuyên gia đánh giá ở mức **{avg_c:.2f}/5** về khả năng tự động hóa, "
         f"nhưng nhân sự IT chỉ sẵn sàng giao việc cho AI ở mức **{avg_d:.2f}/5** — thấp hơn đáng kể. "
         f"Chênh lệch {avg_gap:.2f} điểm cho thấy **AI đang bị lãng phí**: đủ khả năng nhưng chưa được khai thác đúng mức.")

# Biểu đồ 1: Horizontal bar chart so sánh Kỳ vọng vs Năng lực (dễ đọc hơn vertical với 21 ngành)
st.markdown("### Mỗi ngành: AI làm được bao nhiêu vs Người chịu giao bao nhiêu?")
df_sorted = df.sort_values('Chenh_Lech', ascending=True)
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(name='Người chịu giao', y=df_sorted.index, x=df_sorted['Ky_Vong'],
                         marker_color='#636EFA', orientation='h'))
fig_bar.add_trace(go.Bar(name='AI làm được', y=df_sorted.index, x=df_sorted['Nang_Luc'],
                         marker_color='#EF553B', orientation='h'))
fig_bar.update_layout(barmode='group', height=600, xaxis_title="Điểm (1-5)", yaxis_title="",
                      margin=dict(l=300))
st.plotly_chart(fig_bar, use_container_width=True)

# Biểu đồ 2: Ma trận Phân loại Chiến lược Ứng dụng AI
st.markdown("### Ma trận Phân loại Chiến lược Ứng dụng AI")
mau_sac = {'Sẵn sàng triển khai': '#00CC96', 'Rào cản tâm lý': '#EF553B',
           'Cần nâng cấp AI': '#FFA15A', 'Vùng lõi của con người': '#636EFA'}

fig_quad = px.scatter(
    df.reset_index(), x='Ky_Vong', y='Nang_Luc', color='Nhom_Chien_Luoc',
    color_discrete_map=mau_sac,
    hover_name='Occupation (O*NET-SOC Title)',
    labels={'Occupation (O*NET-SOC Title)': 'Vị trí', 'Ky_Vong': 'Mức độ kỳ vọng', 'Nang_Luc': 'Năng lực của AI'},
    title="Trục ngang: Sự chấp nhận của con người | Trục dọc: Năng lực của công nghệ"
)
fig_quad.add_hline(y=avg_c, line_dash="dash", line_color="gray", opacity=0.5)
fig_quad.add_vline(x=avg_d, line_dash="dash", line_color="gray", opacity=0.5)
fig_quad.update_layout(height=500)
st.plotly_chart(fig_quad, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    st.success("**Sẵn sàng triển khai:** Người muốn dùng + AI đã đủ giỏi → Cho AI làm luôn, không cần đợi.")
    st.error("**Rào cản tâm lý:** AI làm được nhưng người không chịu giao → Phải thuyết phục người, không phải nâng cấp AI.")
with c2:
    st.warning("**Cần nâng cấp AI:** Người muốn dùng nhưng AI chưa đủ giỏi → Cần đầu tư công nghệ thêm.")
    st.info("**Vùng lõi của con người:** AI chưa làm được + người cũng không muốn giao → Để người làm, AI chỉ phụ.")

st.markdown("---")

# ============================================================
# PHẦN 2: TÌM KIẾM NGUYÊN NHÂN GỐC RỄ
# ============================================================

st.header("3. Tại sao người ta không chịu giao việc cho AI?")

merged = cs_d.merge(cs_m, on='User ID', suffixes=('', '_m'))
for t in ['Decision', 'Coding', 'Information Access', 'Data Processing']:
    col = 'LLM Usage by Type - ' + t
    merged[t + '_n'] = merged[col].map({'Daily': 5, 'Weekly': 4, 'Monthly': 3, 'Never': 1}).fillna(0)

# ==============================
# LUẬN ĐIỂM 1: RÀO CẢN TÂM LÝ, KHÔNG PHẢI THIẾU NĂNG LỰC
# ==============================
st.markdown("### 3.1. Vấn đề không phải \"không biết dùng\" — mà là \"sợ\"")
st.markdown("**Câu hỏi:** Nếu AI đã đủ giỏi và người ta cũng biết dùng, vậy tại sao vẫn không chịu giao việc?")

merged['high_use'] = merged['LLM Use in Work'].isin(
    ['Yes, I use them every day in my work.', 'Yes, I use them every week in my work.'])
merged['high_fear'] = merged['AI Suffering Attitude'].isin(['Somewhat agree', 'Strongly agree'])

cross_data = []
for hu, hf, label in [(True, False, 'Dùng AI nhiều + Không sợ'),
                       (True, True, 'Dùng AI nhiều + Sợ AI'),
                       (False, False, 'Dùng AI ít + Không sợ'),
                       (False, True, 'Dùng AI ít + Sợ AI')]:
    sub = merged[(merged['high_use'] == hu) & (merged['high_fear'] == hf)]
    cross_data.append({'Nhóm nhân sự': label, 'Chịu giao việc cho AI': sub['Automation Desire Rating'].mean(), 'Số lượng': len(sub)})

cross_df = pd.DataFrame(cross_data)
fig_cross = px.bar(
    cross_df, x='Nhóm nhân sự', y='Chịu giao việc cho AI', color='Chịu giao việc cho AI',
    color_continuous_scale='RdYlGn', range_y=[0, 5],
    title='Dùng AI nhiều nhưng vẫn sợ AI thì vẫn ít chịu giao việc thôi'
)
st.plotly_chart(fig_cross, use_container_width=True)

grp_high_use_fear = cross_df[cross_df['Nhóm nhân sự'] == 'Dùng AI nhiều + Sợ AI']['Chịu giao việc cho AI'].iloc[0]
grp_low_use_ok = cross_df[cross_df['Nhóm nhân sự'] == 'Dùng AI ít + Không sợ']['Chịu giao việc cho AI'].iloc[0]
st.error(f"**Nhận xét:** Người dùng AI hàng ngày nhưng trong lòng **sợ AI** thì chỉ sẵn sàng giao việc ở mức {grp_high_use_fear:.2f}/5 — "
         f"còn **thấp hơn** cả người ít dùng AI nhưng không sợ ({grp_low_use_ok:.2f}/5). "
         "Nghĩa là: **biết dùng AI không có nghĩa là chịu giao việc cho AI**. "
         "Muốn người ta chấp nhận AI, đừng chỉ dạy cách dùng — phải **làm họ hết lo** trước đã.")

# ==============================
# LUẬN ĐIỂM 2: NGHỊCH LÝ CỦA SỰ KIỂM SOÁT
# ==============================
st.markdown("### 3.2. \"Tôi muốn tôi là người quyết định, không phải máy\"")

control_col = 'Reasons for Human Agency - Control'
ctrl_true = merged[merged[control_col] == True]
ctrl_false = merged[merged[control_col] == False]

ctrl_true_desire = ctrl_true['Automation Desire Rating'].mean()
ctrl_false_desire = ctrl_false['Automation Desire Rating'].mean()
ctrl_true_agency = ctrl_true['Human Agency Scale Rating'].mean()
ctrl_false_agency = ctrl_false['Human Agency Scale Rating'].mean()

c1, c2 = st.columns(2)
with c1:
    st.metric("Người lo ngại mất quyền kiểm soát", f"Kỳ vọng = {ctrl_true_desire:.2f}")
    st.write(f"Nhóm này có điểm Human Agency cao hơn ({ctrl_true_agency:.2f})")
    st.write(f"Số lượng: {len(ctrl_true)} đánh giá")
with c2:
    st.metric("Người KHÔNG lo ngại mất quyền kiểm soát", f"Kỳ vọng = {ctrl_false_desire:.2f}")
    st.write(f"Human Agency thấp hơn ({ctrl_false_agency:.2f})")
    st.write(f"Số lượng: {len(ctrl_false)} đánh giá")

st.warning(f"**Nhận xét:** Ai sợ mất quyền kiểm soát thì ít chịu giao việc cho AI hơn ({ctrl_true_desire:.2f} vs {ctrl_false_desire:.2f}). "
           "Đây là tâm lý rất tự nhiên: **\"Tôi muốn tôi là người quyết định, không phải máy.\"** "
           "Dù AI giỏi đến mấy, nếu người ta cảm thấy mất quyền làm chủ công việc, họ sẽ từ chối dùng.")

# So sánh: dùng AI cho Decision vs không
dec_daily = merged[merged['LLM Usage by Type - Decision'] == 'Daily']
dec_low = merged[merged['LLM Usage by Type - Decision'].isin(['Never', 'Monthly'])]

dec_daily_desire = dec_daily['Automation Desire Rating'].mean()
dec_daily_agency = dec_daily['Human Agency Scale Rating'].mean()
dec_low_desire = dec_low['Automation Desire Rating'].mean()
dec_low_agency = dec_low['Human Agency Scale Rating'].mean()

dec_data = pd.DataFrame([
    {'Nhóm': 'Dùng AI để ra quyết định hàng ngày', 'Chịu giao việc cho AI': dec_daily_desire,
     'Muốn làm chủ công việc': dec_daily_agency},
    {'Nhóm': 'Ít dùng AI để ra quyết định', 'Chịu giao việc cho AI': dec_low_desire,
     'Muốn làm chủ công việc': dec_low_agency},
])
fig_dec = px.bar(dec_data, x='Nhóm', y=['Chịu giao việc cho AI', 'Muốn làm chủ công việc'], barmode='group',
                  color_discrete_map={'Chịu giao việc cho AI': '#636EFA', 'Muốn làm chủ công việc': '#EF553B'},
                  range_y=[0, 5], title='Ai muốn AI hỗ trợ quyết định — nhưng vẫn muốn làm chủ?')
st.plotly_chart(fig_dec, use_container_width=True)
st.info(f"**Nhận xét:** Nhóm dùng AI ra quyết định hàng ngày vừa **muốn AI giúp** ({dec_daily_desire:.2f}/5) "
        f"vừa **muốn mình vẫn là người quyết** ({dec_daily_agency:.2f}/5). "
        "Họ không muốn AI thay thế — họ muốn AI kiểu **\"phụ tá thông minh\"**: "
        "AI chuẩn bị dữ liệu, gợi ý phương án, nhưng quyết định cuối cùng vẫn là của người.")

# ==============================
# LUẬN ĐIỂM 3: NHÓM 6-10 NĂM
# ==============================
st.markdown("### 3.3. Người đi làm 6-10 năm: nhóm sợ AI nhất")

exp_deep = []
for exp in EXP_ORDER:
    sub = merged[merged['Experience'] == exp]
    if len(sub) == 0:
        continue
    suf = (sub['AI Suffering Attitude'].isin(['Somewhat agree', 'Strongly agree'])).mean() * 100
    ctrl = (sub[control_col] == True).mean() * 100
    high_inc = sub[sub['Income'].isin(['165K-209K', '209K-529K', '529K+'])].shape[0] / len(sub) * 100
    exp_d = sub['Automation Desire Rating'].mean()
    exp_deep.append({'Kinh nghiệm': exp, 'Lo ngại AI gây khổ (%)': suf,
                     'Lo ngại mất kiểm soát (%)': ctrl, 'Thu nhập cao 165K+ (%)': high_inc,
                     'Kỳ vọng': exp_d})

exp_df = pd.DataFrame(exp_deep)
exp_6_10 = exp_df[exp_df['Kinh nghiệm'] == '6-10 years'].iloc[0]
exp_10_plus = exp_df[exp_df['Kinh nghiệm'] == 'More than 10 years'].iloc[0]

st.markdown(f"Tại sao 6-10 năm có Kỳ vọng thấp nhất ({exp_6_10['Kỳ vọng']:.2f}) "
            f"trong khi >10 năm lại cao nhất ({exp_10_plus['Kỳ vọng']:.2f})?")

fig_deep = px.line(
    exp_df, x='Kinh nghiệm',
    y=['Lo ngại AI gây khổ (%)', 'Lo ngại mất kiểm soát (%)', 'Thu nhập cao 165K+ (%)'],
    title='Tại sao nhóm 6-10 năm e ngại AI nhất?'
)
fig_deep.update_layout(height=400, legend=dict(orientation='h'))
st.plotly_chart(fig_deep, use_container_width=True)
st.error(f"**Nhận xét:** Người đi làm 6-10 năm là nhóm **sợ AI nhất**: "
         f"{exp_6_10['Lo ngại AI gây khổ (%)']:.0f}% lo AI sẽ gây khổ cho mình, "
         f"nhưng chỉ {exp_6_10['Thu nhập cao 165K+ (%)']:.0f}% có thu nhập cao. "
         "Họ đang ở giai đoạn **leo dốc sự nghiệp**: đã đầu tư nhiều năm học nghề, "
         "nhưng chưa lên đến vị trí an toàn — nên sợ AI \"đá\" mình ra nhiều nhất. "
         f"Ngược lại, nhóm >10 năm đã ổn định ({exp_10_plus['Thu nhập cao 165K+ (%)']:.0f}% thu nhập cao), "
         "nên thoải mái giao việc cho AI hơn.")

# ==============================
# LUẬN ĐIỂM 4: CÁC TÁC VỤ ĐỊNH DANH NGHỀ NGHIỆP
# ==============================
st.markdown("### 3.4. Việc nào người ta \"chết cũng không giao\" cho AI?")

task_d = cs_d.groupby('Task ID').agg({
    'Automation Desire Rating': 'mean',
    'Occupation (O*NET-SOC Title)': 'first',
    'Task': 'first',
    'Domain Expertise Requirement': 'mean',
    'Involved Uncertainty': 'mean',
})
task_c = cs_e.groupby('Task ID')['Automation Capacity Rating'].mean()
task_df = task_d.join(task_c).dropna()
task_df['Chenh_Lech'] = task_df['Automation Capacity Rating'] - task_df['Automation Desire Rating']

high_gap = task_df[task_df['Chenh_Lech'] > 1.5]
low_gap = task_df[task_df['Chenh_Lech'] < -1.0]

high_gap_domain = high_gap['Domain Expertise Requirement'].mean()
high_gap_uncert = high_gap['Involved Uncertainty'].mean()
low_gap_domain = low_gap['Domain Expertise Requirement'].mean()
low_gap_uncert = low_gap['Involved Uncertainty'].mean()

comp_data = pd.DataFrame([
    {'Tiêu chí đánh giá': 'Mức độ chuyên môn cần thiết',
     'Việc người ta GIỮ LẠI cho mình': low_gap_domain,
     'Việc người ta SẴN SÀNG giao cho AI': high_gap_domain},
    {'Tiêu chí đánh giá': 'Mức độ phức tạp & rủi ro',
     'Việc người ta GIỮ LẠI cho mình': low_gap_uncert,
     'Việc người ta SẴN SÀNG giao cho AI': high_gap_uncert},
])
fig_comp = px.bar(comp_data, x='Tiêu chí đánh giá',
                   y=['Việc người ta GIỮ LẠI cho mình', 'Việc người ta SẴN SÀNG giao cho AI'],
                   barmode='group',
                   color_discrete_map={'Việc người ta GIỮ LẠI cho mình': '#00CC96',
                                       'Việc người ta SẴN SÀNG giao cho AI': '#EF553B'},
                   title='Việc giữ lại vs Việc giao cho AI: khác nhau ở đâu?')
st.plotly_chart(fig_comp, use_container_width=True)
st.error(f"**Nhận xét:** Những việc mà con người **giữ lại không giao cho AI** (cột xanh) lại đòi hỏi "
         f"chuyên môn cao hơn ({low_gap_domain:.2f} vs {high_gap_domain:.2f}) và phức tạp hơn ({low_gap_uncert:.2f} vs {high_gap_uncert:.2f}). "
         "Đây là những việc kiểu: lập kế hoạch bảo mật, quản lý ngân sách, nghiên cứu công nghệ mới — "
         "tức là những việc **\"định nghĩa bạn là ai trong nghề\"**. "
         "Giao mấy việc này cho AI = cảm giác mất đi giá trị bản thân.")

# ==============================
# LUẬN ĐIỂM 5: "BẪY THU NHẬP TRUNG BÌNH"
# ==============================
st.markdown("### 3.5. Ai sợ AI nhất? Người lương trung bình")

inc_data = []
for inc in INCOME_ORDER:
    sub = merged[merged['Income'] == inc]
    if len(sub) == 0:
        continue
    suf = (sub['AI Suffering Attitude'].isin(['Somewhat agree', 'Strongly agree'])).mean() * 100
    d = sub['Automation Desire Rating'].mean()
    inc_data.append({'Thu nhập': inc, 'Kỳ vọng': d, 'Lo ngại AI gây khổ (%)': suf, 'n': len(sub)})

inc_df = pd.DataFrame(inc_data)

# Tách 2 biểu đồ vì thang đo khác nhau (Kỳ vọng 1-5, Lo ngại 0-100%)
col_left, col_right = st.columns(2)
with col_left:
    fig_inc_desire = px.bar(inc_df, x='Thu nhập', y='Kỳ vọng',
                             color_discrete_sequence=['#636EFA'],
                             range_y=[0, 5],
                             title='Kỳ vọng giao việc cho AI (theo thu nhập)')
    fig_inc_desire.update_layout(height=400, xaxis_tickangle=-30)
    st.plotly_chart(fig_inc_desire, use_container_width=True)
with col_right:
    fig_inc_fear = px.bar(inc_df, x='Thu nhập', y='Lo ngại AI gây khổ (%)',
                           color_discrete_sequence=['#EF553B'],
                           range_y=[0, 50],
                           title='Lo ngại AI gây khổ (theo thu nhập)')
    fig_inc_fear.update_layout(height=400, xaxis_tickangle=-30)
    st.plotly_chart(fig_inc_fear, use_container_width=True)

inc_low = inc_df[inc_df['Thu nhập'] == '0-30K'].iloc[0]
inc_mid = inc_df[inc_df['Thu nhập'] == '60-86K'].iloc[0]
inc_high = inc_df[inc_df['Thu nhập'] == '165K-209K'].iloc[0]

st.info(f"**Nhận xét:** "
        f"Thu nhập thấp (0-30K): Sẵn sàng dùng AI ({inc_low['Kỳ vọng']:.2f}/5), ít lo ({inc_low['Lo ngại AI gây khổ (%)']:.0f}%) — vì **cần AI giúp kiếm thêm**. "
        f"Thu nhập cao (165K+): Cũng OK ({inc_high['Kỳ vọng']:.2f}/5), ít lo ({inc_high['Lo ngại AI gây khổ (%)']:.0f}%) — vì **đã ở vị trí an toàn**. "
        f"Thu nhập giữa (60-86K): Ngại nhất ({inc_mid['Kỳ vọng']:.2f}/5), lo nhất ({inc_mid['Lo ngại AI gây khổ (%)']:.0f}%) — "
        "vì **đủ để có gì mất, nhưng chưa đủ để yên tâm**. "
        "Giống như mua nhà trả góp: người chưa mua thì không lo, người trả xong rồi thì không lo — "
        "chỉ người đang trả giữa chừng mới sợ mất việc nhất.")

# ==============================
# TỔNG KẾT MÔ HÌNH GỐC RỄ
# ==============================
st.markdown("### Tổng hợp: Gốc rễ là gì?")

top_task_gap = task_df.nlargest(1, 'Chenh_Lech')['Chenh_Lech'].iloc[0]

st.markdown(f"""
```
GỐC RỄ CỦA VẤN ĐỀ: "AI sẽ thay thế tôi"

  1. Sợ AI → Không giao việc (dù biết dùng AI)
     └── Dùng AI nhiều + Sợ = chỉ {grp_high_use_fear:.2f}/5
         (thấp hơn cả người ít dùng nhưng không sợ: {grp_low_use_ok:.2f}/5)

  2. Người 6-10 năm kinh nghiệm sợ nhất
     └── Đang leo dốc sự nghiệp, chưa ổn định → Kỳ vọng chỉ {exp_6_10['Kỳ vọng']:.2f}/5

  3. Thu nhập 60-86K lo nhất
     └── Đủ để có gì mất, chưa đủ để yên tâm → Kỳ vọng chỉ {inc_mid['Kỳ vọng']:.2f}/5

  4. Việc càng "định nghĩa nghề" thì càng không muốn giao cho AI
     └── Chênh lệch lớn nhất lên đến {top_task_gap:.2f} điểm
```

**Vậy giải pháp là gì? Không phải dạy thêm AI — mà là thay đổi cách nói:**

| Đừng nói... | Hãy nói... |
|---|---|
| "AI sẽ thay bạn" | "AI giúp bạn rảnh tay làm việc quan trọng hơn" |
| "Tự động hóa" | "AI là phụ tá cho chuyên gia" |
| "Giảm người" | "Mỗi người làm được nhiều hơn" |
""")

st.markdown("---")

# ============================================================
# PHẦN 3: KẾT LUẬN & ĐỀ XUẤT HÀNH ĐỘNG
# ============================================================

st.header("4. Thông điệp Quản trị & Đề xuất Mô hình Trợ lý AI")

st.markdown("""
Đừng nói với nhân viên rằng *"AI sẽ tự động hóa công việc của bạn"* — câu đó nghe như đang đe dọa.

Hãy nói: **"AI sẽ xử lý mấy việc nhàm chán, để bạn tập trung vào mấy việc chỉ bạn mới làm được."**

Cùng một công cụ, nhưng cách đặt vấn đề khác nhau sẽ tạo ra mức độ chấp nhận hoàn toàn khác.
""")

rec = [
    {'Vị trí chuyên môn': 'Lập trình viên Web (Web Developers)', 'Phân nhóm chiến lược': 'Sẵn sàng triển khai', 'Giải pháp đề xuất': 'Trợ lý AI hỗ trợ viết mã (Code Copilot)'},
    {'Vị trí chuyên môn': 'Quản trị Web (Web Administrators)', 'Phân nhóm chiến lược': 'Sẵn sàng triển khai', 'Giải pháp đề xuất': 'WebAdmin Automation Agent'},
    {'Vị trí chuyên môn': 'Nhân viên Nhập liệu (Data Entry Keyers)', 'Phân nhóm chiến lược': 'Sẵn sàng triển khai', 'Giải pháp đề xuất': 'Data Entry Agent'},
    {'Vị trí chuyên môn': 'Kiểm thử Phần mềm (Software QA)', 'Phân nhóm chiến lược': 'Sẵn sàng triển khai', 'Giải pháp đề xuất': 'QA Automation Agent'},
    {'Vị trí chuyên môn': 'Hỗ trợ Người dùng (User Support)', 'Phân nhóm chiến lược': 'Sẵn sàng triển khai', 'Giải pháp đề xuất': 'IT Support Chatbot'},
    {'Vị trí chuyên môn': 'Lập trình viên (Computer Programmers)', 'Phân nhóm chiến lược': 'Cần nâng cấp AI', 'Giải pháp đề xuất': 'Code Assistant Agent'},
    {'Vị trí chuyên môn': 'Quản trị CSDL (Database Administrators)', 'Phân nhóm chiến lược': 'Cần nâng cấp AI', 'Giải pháp đề xuất': 'DBA Automation Agent'},
    {'Vị trí chuyên môn': 'Quản trị Mạng (Network Admins)', 'Phân nhóm chiến lược': 'Cần nâng cấp AI', 'Giải pháp đề xuất': 'Network Admin Agent'},
    {'Vị trí chuyên môn': 'Kiến trúc sư Hệ thống (Systems Engineers)', 'Phân nhóm chiến lược': 'Cần nâng cấp AI', 'Giải pháp đề xuất': 'Architecture Assistant'},
    {'Vị trí chuyên môn': 'Phân tích Bảo mật (Security Analysts)', 'Phân nhóm chiến lược': 'Cần nâng cấp AI', 'Giải pháp đề xuất': 'Security Monitoring Agent'},
    {'Vị trí chuyên môn': 'Phân tích Hệ thống (Systems Analysts)', 'Phân nhóm chiến lược': 'Rào cản tâm lý', 'Giải pháp đề xuất': 'Systems Analysis Agent'},
    {'Vị trí chuyên môn': 'Quản lý Dự án IT (IT Project Managers)', 'Phân nhóm chiến lược': 'Vùng lõi của con người', 'Giải pháp đề xuất': 'PM Assistant Agent'},
    {'Vị trí chuyên môn': 'Quản lý Hệ thống TT (IS Managers)', 'Phân nhóm chiến lược': 'Vùng lõi của con người', 'Giải pháp đề xuất': 'IT Dashboard Agent'},
    {'Vị trí chuyên môn': 'Nhà nghiên cứu (Research Scientists)', 'Phân nhóm chiến lược': 'Vùng lõi của con người', 'Giải pháp đề xuất': 'Research Assistant Agent'},
]

st.dataframe(pd.DataFrame(rec), use_container_width=True, hide_index=True)

# Kết luận
st.markdown("---")

ready_occs = df[df['Nhom_Chien_Luoc'] == 'Sẵn sàng triển khai'].index.tolist()
barrier_occs = df[df['Nhom_Chien_Luoc'] == 'Rào cản tâm lý'].index.tolist()
human_occs = df[df['Nhom_Chien_Luoc'] == 'Vùng lõi của con người'].index.tolist()

st.markdown(f"""
### Kết luận

- **AI đang bị lãng phí {avg_gap:.2f} điểm** — đủ khả năng nhưng chưa được dùng đúng mức
- **Nhóm sẵn sàng dùng ngay**: {', '.join(ready_occs[:4])} → Cho AI làm luôn
- **Nhóm cần thuyết phục**: {', '.join(barrier_occs[:3]) if barrier_occs else 'N/A'} → Bắt đầu từ việc nhỏ, cho thấy lợi ích
- **Nhóm nên để người làm**: {', '.join(human_occs[:3]) if human_occs else 'N/A'} → AI chỉ phụ, không thay

> **Bài học:** Không phải cứ giao hết cho AI là tốt — mà phải giao **đúng việc, đúng người, đúng lúc**.
""")
