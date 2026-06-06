import streamlit as st
import pandas as pd
from datetime import datetime

# Cấu hình trang ứng dụng
st.set_page_config(page_title="Hệ thống Quản lý Dòng tiền & Quỹ thưởng 2026", layout="wide")

# --- MOCKUP DATA KHỞI TẠO ---
if 'transactions' not in st.session_state:
    st.session_state.transactions = [
        {
            "id": "KDTC-2026-001",
            "phap_nhan": "SHQT",
            "luong_tctd": "Vietcombank ➔ BIDV",
            "hinh_thuc": "Mục 2a: Chênh lệch lãi suất VND - VND giữa các pháp nhân",
            "gia_tri": 50000000000,
            "thuong": 15000000,
            "tai_khoan": "Nguyễn Văn A",
            "trang_thai": "Đã phê duyệt"
        },
        {
            "id": "KDTC-2026-002",
            "phap_nhan": "SHQT, SYV",
            "luong_tctd": "Vietcombank ➔ Techcombank",
            "hinh_thuc": "Mục 6: Tận dụng nguồn tiền dư thừa theo thời điểm",
            "gia_tri": 120000000000,
            "thuong": 45000000,
            "tai_khoan": "Trần Thị B (Đại diện)",
            "trang_thai": "Đang trình"
        }
    ]

# --- SIDEBAR: ĐIỀU HƯỚNG ---
st.sidebar.title("MENU HỆ THỐNG")
page = st.sidebar.radio("Di chuyển đến màn hình:", ["Trang 1: Dashboard & Tổng quan", "Trang 2: Chi tiết & Tạo Giao dịch"])

# --- TRANG 1: DASHBOARD ---
if page == "Trang 1: Dashboard & Tổng quan":
    st.title("📊 HỆ THỐNG QUẢN LÝ DÒNG TIỀN & QUY CHẾ THƯỞNG TẬP ĐOÀN")
    st.caption(f"🕒 Dữ liệu cập nhật lần cuối lúc: {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}")
    st.markdown("---")
    
    # 1. Thanh bộ lọc thông minh (Advanced Filter Bar)
    st.subheader("🔍 Bộ lọc nâng cao")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.multiselect("Pháp nhân phát sinh", ["SHQT", "SYV", "SHM", "Aluba", "KK"], default=["SHQT", "SYV"])
    with col2:
        st.multiselect("Tổ chức tín dụng (TCTD)", ["Vietcombank", "BIDV", "Techcombank", "MB Bank"], default=["Vietcombank", "BIDV"])
    with col3:
        st.multiselect("Trạng thái phê duyệt", ["Đang trình", "Đã kiểm tra", "Đã phê duyệt", "Đã xác nhận chi thưởng"], default=["Đang trình", "Đã phê duyệt"])
    with col4:
        st.date_input("Khoảng thời gian giao dịch", [datetime(2026, 1, 1), datetime(2026, 12, 31)])

    # 2. Khu vực hiển thị chỉ số tổng quan (KPI Cards)
    st.markdown("### 📈 Chỉ số sức khỏe dòng tiền & Quỹ thưởng")
    tab_cash, tab_reward = st.tabs(["Sức khỏe Dòng tiền Tập đoàn", "Quản lý Quỹ thưởng KDTC"])
    
    with tab_cash:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Tồn thực thời điểm hiện tại", "1,420.5 Tỷ VNĐ", "+12.3%")
        kpi2.metric("Dòng tiền CFO (Kinh doanh)", "850.2 Tỷ VNĐ", "+5.1%")
        kpi3.metric("Dòng tiền CFF (Tài chính)", "410.3 Tỷ VNĐ", "-2.4%")
        kpi4.metric("Dòng tiền CFI (Đầu tư)", "160.0 Tỷ VNĐ", "+0.8%")
        
    with tab_reward:
        kpi5, kpi6, kpi7 = st.columns(3)
        total_val = sum(item['gia_tri'] for item in st.session_state.transactions)
        total_rew = sum(item['thuong'] for item in st.session_state.transactions)
        kpi5.metric("Tổng dòng tiền giao dịch", f"{total_val:,.0f} VNĐ")
        kpi6.metric("Tổng quỹ thưởng phát sinh", f"{total_rew:,.0f} VNĐ")
        kpi7.metric("Số lượng giao dịch phức tạp", f"{len(st.session_state.transactions)} GD")

    # 3. Bảng danh sách giao dịch
    st.markdown("### 📋 Danh sách tình huống dòng tiền phát sinh")
    df = pd.DataFrame(st.session_state.transactions)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Hiện chưa có giao dịch nào được tạo.")

# --- TRANG 2: CHI TIẾT & TẠO MỚI ---
elif page == "Trang 2: Chi tiết & Tạo Giao dịch":
    st.title("📝 XỬ LÝ CHI TIẾT & CẤU HÌNH GIAO DỊCH DÒNG TIỀN")
    st.markdown("---")
    
    # KHỐI 1: CẤU TRÚC GIAO DỊCH
    st.header("Khối 1: Thông tin cấu trúc & Phân luồng dòng tiền")
    col_k1_1, col_k1_2 = st.columns(2)
    
    with col_k1_1:
        phuong_thuc = st.selectbox("Chọn Phương thức Giao dịch", [
            "1 Pháp nhân - 1 TCTD", 
            "1 Pháp nhân - Nhiều TCTD", 
            "Nhiều Pháp nhân - 1 TCTD", 
            "Nhiều Pháp nhân - Nhiều TCTD"
        ])
        
        # Xử lý hiển thị động cho Pháp nhân dựa trên phương thức được chọn
        if "Nhiều Pháp nhân" in phuong_thuc:
            danh_sach_pn = st.multiselect("Chọn các Pháp nhân tham gia thuộc Tập đoàn", ["SHQT", "SYV", "SHM", "Aluba", "KK"], default=["SHQT", "SYV"])
            phap_nhan_str = ", ".join(danh_sach_pn)
            
            # Ô nhập tỷ lệ động cho từng pháp nhân
            st.markdown("**Phân bổ tỷ lệ đóng góp dòng tiền giữa các pháp nhân:**")
            for pn in danh_sach_pn:
                st.number_input(f"Tỷ lệ đóng góp của {pn} (%)", min_value=0.0, max_value=100.0, value=50.0, key=f"rate_{pn}")
        else:
            pn_single = st.selectbox("Chọn Pháp nhân tham gia thuộc Tập đoàn", ["SHQT", "SYV", "SHM", "Aluba", "KK"])
            phap_nhan_str = pn_single
            
    with col_k1_2:
        st.markdown("**Cấu hình Phân luồng luân chuyển TCTD:**")
        bank_source = st.selectbox("Ngân hàng gốc (Từ)", ["Vietcombank", "BIDV", "Techcombank", "MB Bank"])
        bank_dest = st.multiselect("Ngân hàng đích/trung gian (Đến)", ["Vietcombank", "BIDV", "Techcombank", "MB Bank"], default=["Techcombank"])
        luong_tctd_str = f"{bank_source} ➔ " + " ➔ ".join(bank_dest)
        st.info(f"Luồng di chuyển dòng tiền đã thiết lập: **{luong_tctd_str}**")

    st.markdown("---")
    
    # KHỐI 2: TÀI CHÍNH & ĐIỀU KHOẢN THƯỞNG
    st.header("Khối 2: Thông tin Tài chính & Kích hoạt Quy chế")
    col_k2_1, col_k2_2 = st.columns(2)
    
    with col_k2_1:
        hinh_thuc_kdtc = st.selectbox("Chọn Hình thức Kinh doanh Tài chính (Theo quy chế thưởng)", [
            "Mục 1: Tận dụng nguồn USD dư thừa",
            "Mục 2a: Chênh lệch lãi suất VND - VND giữa các pháp nhân",
            "Mục 2b: Chênh lệch lãi suất VND - USD giữa các pháp nhân",
            "Mục 2c: Chênh lệch lãi suất USD - USD giữa các pháp nhân",
            "Mục 3: Chênh lệch lãi suất giữa các nước (VD: TQ - VN)",
            "Mục 4: Các gói vay ưu đãi của Nhà nước cho DN",
            "Mục 5: Hedging NVL trên sàn",
            "Mục 6: Tận dụng nguồn tiền dư thừa theo thời điểm (Gửi tiền tối ưu dòng tiền)",
            "Mục 7: Mua, bán tỷ giá cho các hoạt động trong tương lai (Forward)"
        ])
        
        loai_tien = st.selectbox("Loại tiền tệ", ["VND", "USD", "NDT", "JPY", "EURO"])
        ty_gia = st.number_input("Tỷ giá giao dịch quy đổi sang VNĐ", min_value=1.0, value=25000.0 if loai_tien == "USD" else 1.0)
        
    with col_k2_2:
        ky_han = st.selectbox("Kỳ hạn dòng tiền", ["Ngắn hạn (< 3 tháng)", "Trung hạn", "Dài hạn (> 1 năm)"])
        so_tien_goc = st.number_input(f"Tổng số tiền giao dịch ({loai_tien})", min_value=0.0, value=1000000.0)
        tien_quy_doi = so_tien_goc * ty_gia
        st.metric("Tổng giá trị giao dịch quy đổi (VNĐ)", f"{tien_quy_doi:,.0f} VNĐ")
        
        chi_phi_van_hanh = st.number_input("Chi phí vận hành phát sinh (VNĐ)", min_value=0, value=0)

    st.markdown("---")
    
    # KHỐI 3: HỆ THỐNG TÍNH TOÁN THƯỞNG TỰ ĐỘNG
    st.header("Khối 3: Kết quả tính toán Quỹ thưởng tự động (Read-only)")
    
    # Giả lập logic tính toán ngầm dựa trên hình thức quy chế đã chọn
    st.success(f"✔️ Điều khoản quy chế áp dụng: **{hinh_thuc_kdtc.split(':')[0]}**")
    
    # Giả lập công thức hiệu quả tính toán ngầm từ file Excel
    hieu_qua_gia_lap = tien_quy_doi * 0.005 - chi_phi_van_hanh # Giả lập tỷ lệ hiệu quả 0.5%
    quy_thuong_gia_lap = hieu_qua_gia_lap * 0.10 # Giả lập trích lập 10% quỹ thưởng từ hiệu quả mang lại
    
    col_k3_1, col_k3_2 = st.columns(2)
    with col_k3_1:
        st.metric("Hiệu quả kinh tế mang lại cho Tập đoàn (Dự kiến)", f"{hieu_qua_gia_lap:,.0f} VNĐ")
    with col_k3_2:
        st.metric("Giá trị quỹ thưởng phát sinh (Dự kiến)", f"{quy_thuong_gia_lap:,.0f} VNĐ")
        
    phuong_an_bo_tri = st.selectbox("Dropdown Phương án Phân bổ thưởng", [
        "Chia đều theo đầu người tham gia", 
        "Chia theo tỷ lệ dòng tiền đóng góp của từng Pháp nhân", 
        "Thưởng toàn bộ cho Pháp nhân chủ trì giao dịch"
    ])
    
    st.markdown("**Danh sách nhân sự được thụ hưởng phân rã từ hệ thống:**")
    mock_nhan_su = pd.DataFrame([
        {"Tên nhân sự": "Nguyễn Văn A", "Vai trò": "Chủ trì", "Bộ phận": "Ban Tài chính Tập đoàn", "Số tiền nhận (VNĐ)": quy_thuong_gia_lap * 0.6},
        {"Tên nhân sự": "Trần Thị B", "Vai trò": "Hỗ trợ", "Bộ phận": "Kế toán trưởng SHQT", "Số tiền nhận (VNĐ)": quy_thuong_gia_lap * 0.4}
    ])
    st.table(mock_nhan_su)
    
    st.text_input("Tài khoản đại diện nhận thưởng", value="Nguyễn Văn A")

    st.markdown("---")
    
    # KHỐI 4: TÁC VỤ (ACTION BUTTONS)
    st.header("Khối 4: Tác vụ quy trình phê duyệt")
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        if st.button("💾 Lưu tạm (Draft)", use_container_width=True):
            st.info("Đã lưu tạm bản nháp giao dịch dòng tiền!")
            
    with col_btn2:
        if st.button("🔍 Kiểm tra (Verify)", use_container_width=True):
            st.warning("Đã chuyển trạng thái sang: Đã kiểm tra (Chờ duyệt hạn mức)!")
            
    with col_btn3:
        if st.button("🚀 Gửi trình triển khai", use_container_width=True):
            st.success("Đã gửi tờ trình luân chuyển dòng tiền tới Ban Giám Đốc!")
            
    with col_btn4:
        if st.button("💰 Gửi duyệt thưởng", use_container_width=True):
            # Thêm bản ghi mới vào danh sách tổng tại trang 1
            new_id = f"KDTC-2026-00{len(st.session_state.transactions) + 1}"
            st.session_state.transactions.append({
                "id": new_id,
                "phap_nhan": phap_nhan_str if phap_nhan_str else "SHQT",
                "luong_tctd": luong_tctd_str,
                "hinh_thuc": hinh_thuc_kdtc,
                "gia_tri": tien_quy_doi,
                "thuong": quy_thuong_gia_lap,
                "tai_khoan": "Nguyễn Văn A",
                "trang_thai": "Đang trình"
            })
            st.balloons()
            st.success(f"Đã gửi hồ sơ duyệt thưởng giao dịch {new_id} lên cấp Quản lý thành công!")