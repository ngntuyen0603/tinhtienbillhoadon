import os
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Order Nhà Hàng",
    layout="wide"
)

# =========================================================
# 🎨 GIAO DIỆN NHÀ HÀNG
# =========================================================

st.markdown("""
<style>

/* ===== NỀN ===== */

.stApp {
    background-image:
        linear-gradient(
            rgba(255, 248, 240, 0.88),
            rgba(255, 248, 240, 0.88)
        ),
        url("chie.jpg");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;

    font-size: 17px;
}


/* ===== TIÊU ĐỀ CHÍNH ===== */

h1 {
    color: #7B3F00 !important;
    font-size: 34px !important;
    font-weight: 800 !important;
}


/* ===== TIÊU ĐỀ PHỤ ===== */

h2 {
    color: #8B4513 !important;
    font-size: 28px !important;
    font-weight: 800 !important;
}

h3 {
    color: #8B4513 !important;
    font-size: 23px !important;
    font-weight: 700 !important;
}


/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #D8B08C,
        #C99A72
    );
}


/* Chữ Sidebar */

section[data-testid="stSidebar"] * {
    color: #3E2723 !important;
    font-size: 17px !important;
    font-weight: 700 !important;
}


/* ===== RADIO / MENU SIDEBAR ===== */

section[data-testid="stSidebar"] label {
    font-size: 18px !important;
    font-weight: 800 !important;
}


/* ===== NÚT BẤM ===== */

.stButton > button {
    font-size: 17px !important;
    font-weight: 800 !important;

    border-radius: 10px;
    border: none;

    padding: 10px 18px;
}


/* ===== Ô NHẬP ===== */

input {
    font-size: 17px !important;
    font-weight: 600 !important;
}


/* ===== SELECTBOX ===== */

div[data-baseweb="select"] {
    font-size: 17px !important;
    font-weight: 600 !important;
}


/* ===== METRIC ===== */

div[data-testid="stMetric"] {
    background-color: rgba(255, 255, 255, 0.88);

    padding: 18px;

    border-radius: 15px;
}


/* Số trong Metric */

div[data-testid="stMetricValue"] {
    font-size: 27px !important;
    font-weight: 800 !important;
}


/* Tên Metric */

div[data-testid="stMetricLabel"] {
    font-size: 17px !important;
    font-weight: 700 !important;
}


/* ===== BẢNG ===== */

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}


/* ===== TEXT THƯỜNG ===== */

p {
    font-size: 17px !important;
}


/* ===== CAPTION ===== */

.stCaption {
    font-size: 16px !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# 🏠 LOGO - GIỮ NGUYÊN KÍCH THƯỚC BAN ĐẦU
# =========================================================

st.image("logo1.jpg")


# =========================================================
# 📁 FILE DỮ LIỆU
# =========================================================

CSV_FILE = "history.csv"

menu = {
    "Đồ ăn": {
        "Pizza Hải Sản": 150000,
        "Pizza cá": 500000,
        "Mì Ý Bò Bằm": 95000,
        "GÀ CHIÊN MẮM TỎI": 29000,
        "Burger Gà": 35000,
        "Bít tết Bò Mỹ": 250000,
        "Lẩu Cá Đuối VŨNG TÀU": 99000,
        "Sườn nướng BBQ": 150000,
        "Cánh gà chiên mắm": 75000,
        "Lẩu cá diêu hồng": 200000,
        "Lẩu Thái hải sản": 300000,
    },

    "Thức uống": {
        "Coca Cola": 20000,
        "Trà sữa SV": 70000,
        "Trà Đào Cam Sả": 35000,
        "Cà Phê Sữa": 25000,
        "Nước Suối": 10000,
        "Sinh tố Bơ": 45000,
        "Nước ép cam": 40000,
        "Mojito chanh dây": 55000,
        "Bia Heineken": 30000,
    },
}

# =========================================================
# SESSION STATE
# =========================================================

if "order_dict" not in st.session_state:
    st.session_state.order_dict = {}

if "last_bill" not in st.session_state:
    st.session_state.last_bill = ""

if "history" not in st.session_state:

    if os.path.exists(CSV_FILE):

        try:
            df_loaded = pd.read_csv(CSV_FILE)

            st.session_state.history = df_loaded.to_dict(
                orient="records"
            )

        except Exception:
            st.session_state.history = []

    else:
        st.session_state.history = []


if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False


# =========================================================
# THANH ĐIỀU HƯỚNG
# =========================================================

page = st.sidebar.radio(
    "📋 Chọn trang hệ thống",
    [
        "🍽️ Order",
        "🔑 Admin"
    ]
)


# =========================================================
# TRANG ORDER
# =========================================================

if page == "🍽️ Order":

    st.title("🍽️ Hệ thống Order Nhà Hàng_Ngọc Tuyến")

    st.caption(
        "Ghi nhận order nhanh chóng và chính xác theo thời gian thực"
    )

    col1, col2 = st.columns([1, 1.3])


    # =====================================================
    # CỘT 1 - CHỌN MÓN
    # =====================================================

    with col1:

        st.subheader("🍽️ Chọn món")

        table_number = st.selectbox(
            "🪑 Chọn số bàn",
            [f"Bàn {i}" for i in range(1, 21)]
        )

        category = st.selectbox(
            "Chọn loại:",
            list(menu.keys())
        )

        item = st.selectbox(
            "Chọn món:",
            list(menu[category].keys())
        )

        quantity = st.number_input(
            "Số lượng:",
            min_value=1,
            step=1,
            value=1
        )


        if st.button(
            "➕ Thêm vào giỏ",
            use_container_width=True
        ):

            price = menu[category][item]


            if item in st.session_state.order_dict:

                st.session_state.order_dict[item]["Số lượng"] += quantity

                st.session_state.order_dict[item]["Thành tiền"] = (
                    st.session_state.order_dict[item]["Số lượng"]
                    * price
                )

                st.session_state.order_dict[item]["Bàn"] = table_number


            else:

                st.session_state.order_dict[item] = {

                    "Bàn": table_number,

                    "Tên món": item,

                    "Đơn giá": price,

                    "Số lượng": quantity,

                    "Thành tiền": price * quantity,

                }


            st.success(
                f"Đã thêm {item} vào giỏ!"
            )

            st.rerun()


    # =====================================================
    # CỘT 2 - GIỎ HÀNG
    # =====================================================

    with col2:

        st.subheader("🛒 Giỏ hàng hiện tại")


        if st.session_state.order_dict:

            df = pd.DataFrame.from_dict(
                st.session_state.order_dict,
                orient="index"
            )


            st.dataframe(
                df[
                    [
                        "Bàn",
                        "Tên món",
                        "Đơn giá",
                        "Số lượng",
                        "Thành tiền"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )


            # =================================================
            # TÍNH TIỀN
            # =================================================

            tam_tinh = df["Thành tiền"].sum()


            # =================================================
            # 🎟️ VOUCHER
            # =================================================

            st.subheader("🎟️ Khuyến mãi")


            voucher = st.selectbox(
                "Chọn mã giảm giá",
                [
                    "Không sử dụng",
                    "NGOC10 - Giảm 10%",
                    "NGOC15 - Giảm 15%"
                ]
            )


            if voucher == "NGOC10 - Giảm 10%":

                phan_tram_giam = 10


            elif voucher == "NGOC15 - Giảm 15%":

                phan_tram_giam = 15


            else:

                phan_tram_giam = 0


            giam_gia = (
                tam_tinh
                * phan_tram_giam
                / 100
            )


            tong_thanh_toan = (
                tam_tinh
                - giam_gia
            )


            st.write(
                f"**Tạm tính:** "
                f"{tam_tinh:,.0f} VNĐ"
            )


            if giam_gia > 0:

                st.write(
                    f"**🎟️ Giảm giá {phan_tram_giam}%:** "
                    f"-{giam_gia:,.0f} VNĐ"
                )

            else:

                st.write(
                    "**Giảm giá:** 0 VNĐ"
                )


            st.metric(
                "💰 Tổng thanh toán thực tế",
                f"{tong_thanh_toan:,.0f} VNĐ"
            )


            # =================================================
            # 👤 THÔNG TIN KHÁCH HÀNG
            # =================================================

            st.subheader(
                "👤 Thông tin thanh toán"
            )


            customer_name = st.text_input(
                "Tên khách hàng",
                placeholder="Nhập tên khách hàng"
            )


            payment_method = st.selectbox(
                "💳 Phương thức thanh toán",
                [
                    "💵 Tiền mặt",
                    "🏦 Chuyển khoản",
                    "📱 Ví điện tử"
                ]
            )


            # =================================================
            # NÚT THANH TOÁN / XÓA GIỎ
            # =================================================

            col_btn1, col_btn2 = st.columns(2)


            with col_btn1:

                thanh_toan = st.button(
                    "💳 Thanh toán",
                    use_container_width=True
                )


            with col_btn2:

                xoa_gio = st.button(
                    "🗑️ Xóa toàn bộ giỏ",
                    use_container_width=True
                )


            # =================================================
            # XÓA GIỎ
            # =================================================

            if xoa_gio:

                st.session_state.order_dict = {}

                st.rerun()


            # =================================================
            # THANH TOÁN
            # =================================================

            if thanh_toan:

                # Kiểm tra tên khách hàng

                if customer_name.strip() == "":

                    st.warning(
                        "⚠️ Vui lòng nhập tên khách hàng trước khi thanh toán."
                    )

                else:

                    now_str = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )


                    # =================================================
                    # TẠO MÃ HÓA ĐƠN
                    # =================================================

                    invoice_id = datetime.now().strftime(
                        "%Y%m%d%H%M%S"
                    )


                    # =================================================
                    # TẠO NỘI DUNG HÓA ĐƠN
                    # =================================================

                    bill = ""

                    bill += "====================================\n"
                    bill += "       NHÀ HÀNG NGỌC TUYẾN\n"
                    bill += "====================================\n"

                    bill += (
                        f"Mã hóa đơn: {invoice_id}\n"
                    )

                    bill += (
                        f"Thời gian: {now_str}\n"
                    )

                    bill += (
                        f"Khách hàng: {customer_name}\n"
                    )

                    bill += (
                        f"Bàn: {table_number}\n"
                    )

                    bill += "------------------------------------\n"


                    # Danh sách món

                    for row in st.session_state.order_dict.values():

                        bill += (
                            f"{row['Tên món']} x "
                            f"{row['Số lượng']} = "
                            f"{row['Thành tiền']:,.0f} VNĐ\n"
                        )


                    bill += "------------------------------------\n"


                    bill += (
                        f"Tạm tính: "
                        f"{tam_tinh:,.0f} VNĐ\n"
                    )


                    bill += (
                        f"Giảm giá: "
                        f"-{giam_gia:,.0f} VNĐ\n"
                    )


                    bill += (
                        f"TỔNG THANH TOÁN: "
                        f"{tong_thanh_toan:,.0f} VNĐ\n"
                    )


                    bill += (
                        f"Phương thức: "
                        f"{payment_method}\n"
                    )


                    bill += "====================================\n"
                    bill += "       CẢM ƠN QUÝ KHÁCH!\n"
                    bill += "====================================\n"


                    # =================================================
                    # LƯU VÀO HISTORY
                    # =================================================

                    for row in st.session_state.order_dict.values():

                        st.session_state.history.append(
                            {

                                "Mã hóa đơn": invoice_id,

                                "Thời gian": now_str,

                                "Khách hàng": customer_name,

                                "Bàn": row["Bàn"],

                                "Tên món": row["Tên món"],

                                "Số lượng": row["Số lượng"],

                                "Thành tiền": row["Thành tiền"],

                                "Giảm giá": giam_gia,

                                "Tổng thanh toán": tong_thanh_toan,

                                "Phương thức": payment_method

                            }
                        )


                    # =================================================
                    # LƯU CSV
                    # =================================================

                    try:

                        df_history = pd.DataFrame(
                            st.session_state.history
                        )


                        df_history.to_csv(
                            CSV_FILE,
                            index=False,
                            encoding="utf-8-sig"
                        )


                    except Exception as e:

                        st.error(
                            f"Lỗi ghi dữ liệu xuống máy chủ: {e}"
                        )


                    # =================================================
                    # LƯU HÓA ĐƠN
                    # =================================================

                    st.session_state.last_bill = bill


                    st.success(
                        f"🎉 Thanh toán thành công! "
                        f"Mã hóa đơn: {invoice_id}"
                    )


                    # Xóa giỏ hàng

                    st.session_state.order_dict = {}


                    # Không dùng rerun ở đây ngay lập tức
                    # để hóa đơn có thể hiển thị


        else:

            st.info(
                "🛒 Giỏ hàng đang trống. "
                "Hãy chọn món ăn/đồ uống bên trái để lên đơn."
            )


    # =====================================================
    # 🧾 HIỂN THỊ HÓA ĐƠN SAU KHI THANH TOÁN
    # =====================================================

    if st.session_state.last_bill:

        st.divider()

        st.subheader(
            "🧾 Hóa đơn điện tử"
        )


        st.code(
            st.session_state.last_bill,
            language="text"
        )


        st.download_button(
            label="📥 Tải hóa đơn về máy",
            data=st.session_state.last_bill,
            file_name="hoa_don_nha_hang.txt",
            mime="text/plain",
            use_container_width=True
        )


        if st.button(
            "❌ Đóng hóa đơn",
            use_container_width=True
        ):

            st.session_state.last_bill = ""

            st.rerun()


# =========================================================
# TRANG ADMIN
# =========================================================

elif page == "🔑 Admin":

    st.title(
        "🔑 Trang Quản Trị & Phân Tích Doanh Thu"
    )


    # =====================================================
    # ĐĂNG NHẬP
    # =====================================================

    if not st.session_state.admin_logged_in:

        with st.form("admin_login_form"):

            password = st.text_input(
                "Nhập mật khẩu quản trị",
                type="password"
            )


            login_submitted = st.form_submit_button(
                "🔑 Đăng nhập"
            )


            if login_submitted:

                if password == "123456":

                    st.session_state.admin_logged_in = True

                    st.success(
                        "Đăng nhập thành công!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Mật khẩu không chính xác!"
                    )


        st.warning(
            "Vui lòng nhập mật khẩu và bấm đăng nhập "
            "để xem dữ liệu kinh doanh."
        )

        st.stop()


    # =====================================================
    # HEADER ADMIN
    # =====================================================

    col_header_title, col_header_btn = st.columns(
        [4, 1]
    )


    with col_header_title:

        st.success(
            "Xác thực quyền Quản trị viên thành công!"
        )


    with col_header_btn:

        if st.button("🔒 Đăng xuất"):

            st.session_state.admin_logged_in = False

            st.rerun()


    # =====================================================
    # TABS ADMIN
    # =====================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "📋 Danh sách thực đơn",
            "💰 Doanh thu & Nhật ký giao dịch",
            "📊 Thống kê & Phân tích bán hàng REAL-TIME",
        ]
    )


    # =====================================================
    # TAB 1 - MENU
    # =====================================================

    with tab1:

        st.subheader(
            "Menu hiện hành của nhà hàng"
        )


        data = []


        for category in menu:

            for item, price in menu[category].items():

                data.append(
                    [
                        category,
                        item,
                        price
                    ]
                )


        df_menu = pd.DataFrame(
            data,
            columns=[
                "Phân loại",
                "Tên món",
                "Đơn giá (VNĐ)"
            ]
        )


        st.dataframe(
            df_menu,
            use_container_width=True,
            hide_index=True
        )


    # =====================================================
    # TAB 2 - DOANH THU
    # =====================================================

    with tab2:

        st.subheader(
            "💰 Doanh thu & Hóa đơn thực tế từ khách gọi"
        )


        if os.path.exists(CSV_FILE):

            try:

                df_history = pd.read_csv(
                    CSV_FILE
                )

            except Exception:

                df_history = pd.DataFrame()

        else:

            df_history = pd.DataFrame()


        if not df_history.empty:

            # Tổng tiền khách đã thanh toán

            if "Tổng thanh toán" in df_history.columns:

                tong_doanh_thu = (
                    df_history["Tổng thanh toán"].sum()
                )

            else:

                tong_doanh_thu = (
                    df_history["Thành tiền"].sum()
                )


            col_met1, col_met2 = st.columns(2)


            col_met1.metric(
                "💰 Tổng doanh thu tích lũy",
                f"{tong_doanh_thu:,.0f} VNĐ"
            )


            col_met2.metric(
                "🍽️ Số lượng món đã phục vụ",
                f"{df_history['Số lượng'].sum()} phần"
            )


            st.markdown("---")


            # =================================================
            # DOANH THU THEO NGÀY
            # =================================================

            st.subheader(
                "📅 Thống kê doanh thu theo ngày"
            )


            df_history["Ngày"] = pd.to_datetime(
                df_history["Thời gian"]
            ).dt.date


            revenue_column = (
                "Tổng thanh toán"
                if "Tổng thanh toán" in df_history.columns
                else "Thành tiền"
            )


            df_daily_revenue = (
                df_history
                .groupby("Ngày")[revenue_column]
                .sum()
                .reset_index()
            )


            df_daily_revenue.columns = [
                "Ngày",
                "Doanh thu (VNĐ)"
            ]


            col_chart_day, col_table_day = st.columns(
                [1.5, 1]
            )


            with col_chart_day:

                st.write(
                    "**📊 Biểu đồ doanh thu hàng ngày:**"
                )


                st.bar_chart(
                    df_daily_revenue.set_index(
                        "Ngày"
                    )["Doanh thu (VNĐ)"]
                )


            with col_table_day:

                st.write(
                    "**📋 Bảng kê doanh thu theo ngày:**"
                )


                st.dataframe(
                    df_daily_revenue.style.format(
                        {
                            "Doanh thu (VNĐ)": "{:,.0f} VNĐ"
                        }
                    ),
                    use_container_width=True,
                    hide_index=True
                )


            st.markdown("---")


            # =================================================
            # LỊCH SỬ THANH TOÁN
            # =================================================

            st.subheader(
                "📜 Chi tiết lịch sử thanh toán thực tế"
            )


            history_columns = [
                "Mã hóa đơn",
                "Thời gian",
                "Khách hàng",
                "Bàn",
                "Tên món",
                "Số lượng",
                "Thành tiền",
                "Giảm giá",
                "Tổng thanh toán",
                "Phương thức"
            ]


            existing_columns = [
                col
                for col in history_columns
                if col in df_history.columns
            ]


            st.dataframe(
                df_history[existing_columns],
                use_container_width=True,
                hide_index=True
            )


        else:

            st.info(
                "Hệ thống chưa ghi nhận bất kỳ "
                "giao dịch thanh toán nào từ khách hàng."
            )


    # =====================================================
    # TAB 3 - THỐNG KÊ
    # =====================================================

    with tab3:

        st.subheader(
            "📊 Phân tích số liệu và Khung giờ vàng"
        )


        if os.path.exists(CSV_FILE):

            try:

                df_anal = pd.read_csv(
                    CSV_FILE
                )

            except Exception:

                df_anal = pd.DataFrame()

        else:

            df_anal = pd.DataFrame()


        if not df_anal.empty:

            df_anal["Thời gian"] = pd.to_datetime(
                df_anal["Thời gian"]
            )


            df_anal["Giờ"] = (
                df_anal["Thời gian"].dt.hour
            )


            df_anal["Tháng-Năm"] = (
                df_anal["Thời gian"]
                .dt.strftime("%m/%Y")
            )


            # =================================================
            # MÓN BÁN CHẠY
            # =================================================

            best_seller = (
                df_anal
                .groupby("Tên món")["Số lượng"]
                .sum()
                .idxmax()
            )


            best_seller_qty = (
                df_anal
                .groupby("Tên món")["Số lượng"]
                .sum()
                .max()
            )


            # =================================================
            # KHUNG GIỜ
            # =================================================

            hourly_sales = (
                df_anal
                .groupby("Giờ")["Số lượng"]
                .sum()
            )


            best_hour = hourly_sales.idxmax()


            best_hour_qty = hourly_sales.max()


            # =================================================
            # THÁNG DOANH THU
            # =================================================

            revenue_column = (
                "Tổng thanh toán"
                if "Tổng thanh toán" in df_anal.columns
                else "Thành tiền"
            )


            best_month = (
                df_anal
                .groupby("Tháng-Năm")[revenue_column]
                .sum()
                .idxmax()
            )


            best_month_rev = (
                df_anal
                .groupby("Tháng-Năm")[revenue_column]
                .sum()
                .max()
            )


            # =================================================
            # KPI
            # =================================================

            col_kpi1, col_kpi2, col_kpi3 = st.columns(3)


            with col_kpi1:

                st.info(
                    "🏆 MÓN BÁN CHẠY NHẤT"
                )


                st.metric(
                    label=best_seller,
                    value=f"{best_seller_qty} phần"
                )


            with col_kpi2:

                st.warning(
                    "⚡ KHUNG GIỜ VÀNG"
                )


                st.metric(
                    label=(
                        f"Khung giờ: "
                        f"{best_hour:02d}:00 - "
                        f"{(best_hour + 1):02d}:00"
                    ),
                    value=f"{best_hour_qty} phần"
                )


            with col_kpi3:

                st.success(
                    "📅 THÁNG DOANH THU ĐỈNH ĐIỂM"
                )


                st.metric(
                    label=f"Tháng {best_month}",
                    value=f"{best_month_rev:,.0f} VNĐ"
                )


            st.markdown("---")


            # =================================================
            # THỐNG KÊ TỪNG MÓN
            # =================================================

            st.write(
                "### 🍔 Doanh thu & Số lượng tiêu thụ từng món"
            )


            summary_mon = (
                df_anal
                .groupby("Tên món")
                .agg(
                    Số_lượng_bán=(
                        "Số lượng",
                        "sum"
                    ),

                    Doanh_thu=(
                        revenue_column,
                        "sum"
                    )
                )
                .reset_index()
            )


            summary_mon = summary_mon.sort_values(
                by="Số_lượng_bán",
                ascending=False
            )


            col_chart1, col_table1 = st.columns(
                [1.5, 1]
            )


            with col_chart1:

                st.write(
                    "**📊 Tổng số lượng bán ra:**"
                )


                st.bar_chart(
                    summary_mon.set_index(
                        "Tên món"
                    )["Số_lượng_bán"]
                )


            with col_table1:

                st.write(
                    "**💰 Doanh thu từng món:**"
                )


                st.dataframe(
                    summary_mon.style.format(
                        {
                            "Doanh_thu":
                            "{:,.0f} VNĐ"
                        }
                    ),
                    use_container_width=True,
                    hide_index=True
                )


            st.markdown("---")


            # =================================================
            # KHUNG GIỜ VÀNG
            # =================================================

            st.write(
                "### ⏰ Thống kê lượng khách đặt theo khung giờ"
            )


            summary_gio = (
                df_anal
                .groupby("Giờ")
                .agg(
                    Số_lượng_món=(
                        "Số lượng",
                        "sum"
                    ),

                    Doanh_thu=(
                        revenue_column,
                        "sum"
                    )
                )
                .reset_index()
            )


            all_hours = pd.DataFrame(
                {
                    "Giờ": range(24)
                }
            )


            summary_gio = pd.merge(
                all_hours,
                summary_gio,
                on="Giờ",
                how="left"
            ).fillna(0)


            col_chart2, col_info2 = st.columns(
                [1.5, 1]
            )


            with col_chart2:

                st.write(
                    "**📊 Biểu đồ lượng bán theo giờ:**"
                )


                st.bar_chart(
                    summary_gio.set_index(
                        "Giờ"
                    )["Số_lượng_món"]
                )


            with col_info2:

                st.write(
                    "**⏰ Thời điểm bán chạy nhất:**"
                )


                st.markdown(
                    f"""
                    👉 Khung giờ có số lượng món bán ra
                    cao nhất hiện tại là:

                    **{best_hour:02d}:00 - "
                    f"{(best_hour + 1):02d}:00**

                    với tổng cộng
                    **{best_hour_qty} phần**.
                    """
                )


                st.dataframe(
                    summary_gio[
                        summary_gio["Số_lượng_món"] > 0
                    ].style.format(
                        {
                            "Doanh_thu":
                            "{:,.0f} VNĐ"
                        }
                    ),
                    use_container_width=True,
                    hide_index=True
                )


            st.markdown("---")


            # =================================================
            # DOANH THU THEO THÁNG
            # =================================================

            st.write(
                "### 📅 Doanh thu bán hàng theo tháng"
            )


            df_anal["Tháng_Số"] = (
                df_anal["Thời gian"].dt.month
            )


            summary_thang = (
                df_anal
                .groupby(
                    [
                        "Tháng_Số",
                        "Tháng-Năm"
                    ]
                )
                .agg(
                    Số_lượng_bán=(
                        "Số lượng",
                        "sum"
                    ),

                    Doanh_thu=(
                        revenue_column,
                        "sum"
                    )
                )
                .reset_index()
                .sort_values("Tháng_Số")
            )


            col_chart3, col_table3 = st.columns(
                [1.5, 1]
            )


            with col_chart3:

                st.write(
                    "**📈 Biểu đồ doanh thu qua các tháng:**"
                )


                st.bar_chart(
                    summary_thang.set_index(
                        "Tháng-Năm"
                    )["Doanh_thu"]
                )


            with col_table3:

                st.write(
                    "**💰 Tổng doanh thu từng tháng:**"
                )


                st.dataframe(
                    summary_thang[
                        [
                            "Tháng-Năm",
                            "Số_lượng_bán",
                            "Doanh_thu"
                        ]
                    ].style.format(
                        {
                            "Doanh_thu":
                            "{:,.0f} VNĐ"
                        }
                    ),
                    use_container_width=True,
                    hide_index=True
                )


        else:

            st.info(
                "Chưa có dữ liệu giao dịch để thống kê. "
                "Hãy tiến hành thanh toán một vài đơn hàng trước."
            )
