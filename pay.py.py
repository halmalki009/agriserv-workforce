import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime
import re
import json
from io import BytesIO


st.set_page_config(
    page_title="لوحة تكلفة رأس المال البشري",
    page_icon="📊",
    layout="wide"
)


# =========================
# حماية الدخول بكلمة مرور
# =========================
PASSWORD = "Nemer@2030"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.markdown("""
    <div style='text-align:center; padding-top:120px;'>
        <h1 style='color:#0B3C5D;'>🔐 Secure Dashboard Access</h1>
        <p style='color:gray;'>Please enter password to continue</p>
    </div>
    """, unsafe_allow_html=True)

    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        if password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()

        else:
            st.error("Incorrect Password")

    st.stop()


# =========================
# إعدادات الصفحة
# =========================

# ===== CSS هنا =====
st.markdown("""<style>.smart-card{background:linear-gradient(135deg,#ffffff 0%,#f7f9fc 100%);border-radius:22px;padding:22px 20px;min-height:140px;box-shadow:0 8px 24px rgba(0,0,0,0.08);border:1px solid rgba(0,0,0,0.05);direction:rtl;text-align:right;}.smart-card-title{font-size:14px;font-weight:700;color:#344054;margin-bottom:12px;}.smart-card-value{font-size:clamp(22px,3vw,38px);font-weight:900;color:#101828;line-height:1.2;word-break:break-word;}section[data-testid="stFileUploader"] div,section[data-testid="stFileUploader"] span,section[data-testid="stFileUploader"] p,section[data-testid="stFileUploader"] small{color:#334155 !important;}section[data-testid="stFileUploader"] svg{color:#0B3C5D !important;fill:#0B3C5D !important;opacity:0.95 !important;}section[data-testid="stFileUploader"]{background:#FFFFFF !important;border-radius:14px !important;padding:12px !important;border:1px solid rgba(255,255,255,0.35) !important;box-shadow:0 6px 16px rgba(0,0,0,0.12) !important;}section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"]{min-height:58px !important;border-radius:12px !important;background:#FFFFFF !important;border:1px dashed #CBD5E1 !important;}section[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"],section[data-testid="stFileUploader"] button[kind="secondary"]{background-color:#0B3C5D !important;border:1px solid #0B3C5D !important;color:#FFFFFF !important;border-radius:10px !important;opacity:1 !important;font-weight:800 !important;box-shadow:none !important;}section[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] *,section[data-testid="stFileUploader"] button[kind="secondary"] *{color:#FFFFFF !important;opacity:1 !important;}section[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"]:hover,section[data-testid="stFileUploader"] button[kind="secondary"]:hover{background-color:#0C8A73 !important;border-color:#0C8A73 !important;}section[data-testid="stFileUploader"] div,section[data-testid="stFileUploader"] span,section[data-testid="stFileUploader"] small{color:#0B3C5D !important;}.material-icons,.material-icons-outlined,.material-symbols-outlined,.material-symbols-rounded,span[data-testid="stIconMaterial"]{font-family:"Material Symbols Rounded","Material Symbols Outlined","Material Icons" !important;}:root{--app-font:"SST Arabic","SSTArabic","SST Arabic Roman","SST Arabic Medium","IBM Plex Sans Arabic","Tahoma","Arial",sans-serif;}html,body,.stApp,.block-container,.stMarkdown,.stDataFrame,.stMetric,p,div,span,label,h1,h2,h3,h4,h5,h6,button,input,textarea,[data-testid="stSidebar"],[data-testid="stTable"],[data-testid="stDataFrame"],[data-baseweb="tab"],[data-baseweb="select"],[data-baseweb="popover"],[data-baseweb="menu"],[data-baseweb="option"],[data-testid="stWidgetLabel"]{font-family:var(--app-font) !important;}div[data-testid="stDataFrame"] *,div[data-testid="stTable"] *{font-family:var(--app-font) !important;}section[data-testid="stSidebar"] *,section[data-testid="stSidebar"] input,section[data-testid="stSidebar"] textarea,section[data-testid="stSidebar"] div[data-baseweb="select"] *,section[data-testid="stSidebar"] label,section[data-testid="stSidebar"] p{font-family:var(--app-font) !important;}.material-icons,.material-icons-outlined,.material-symbols-outlined,.material-symbols-rounded,.material-symbols-sharp,span[class*="material"],span[data-testid="stIconMaterial"],[data-testid="stIconMaterial"]{font-family:"Material Symbols Rounded","Material Symbols Outlined","Material Icons" !important;font-weight:normal !important;font-style:normal !important;line-height:1 !important;letter-spacing:normal !important;text-transform:none !important;white-space:nowrap !important;word-wrap:normal !important;direction:ltr !important;-webkit-font-feature-settings:"liga" !important;-webkit-font-smoothing:antialiased !important;}.alert-card{background:#FFFFFF;border-radius:18px;padding:15px 14px;min-height:104px;box-shadow:0 8px 18px rgba(15,23,42,0.07);border:1px solid #E6EAF0;direction:rtl;text-align:center;}.alert-card.red{border-top:4px solid #F04438;}.alert-card.orange{border-top:4px solid #F79009;}.alert-card.green{border-top:4px solid #12B76A;}.alert-card.blue{border-top:4px solid #0B3C5D;}.alert-card-title{font-size:13px;font-weight:800;color:#475467;margin-bottom:8px;}.alert-card-value{font-size:clamp(20px,2.4vw,30px);font-weight:900;color:#101828;line-height:1.15;}.alert-note{background:#FFFFFF;border-right:5px solid #0B3C5D;border-radius:14px;padding:12px 16px;margin:8px 0 16px 0;color:#0B3C5D;font-weight:700;direction:rtl;text-align:right;box-shadow:0 6px 14px rgba(15,23,42,0.06);}div[data-testid="stDataFrame"] table{font-family:"SST Arabic","SSTArabic","IBM Plex Sans Arabic",Tahoma,Arial,sans-serif !important;}div[data-testid="stDataFrame"] th{text-align:center !important;vertical-align:middle !important;font-weight:800 !important;font-size:13px !important;}div[data-testid="stDataFrame"] td{text-align:center !important;vertical-align:middle !important;font-size:13px !important;font-weight:600 !important;padding-top:8px !important;padding-bottom:8px !important;}[data-testid="stDataFrameResizable"] *{font-family:"SST Arabic","SSTArabic","IBM Plex Sans Arabic",Tahoma,Arial,sans-serif !important;}.metric-label,.metric-value{text-align:center !important;width:100%;}.stTabs [data-baseweb="tab"]{justify-content:center !important;align-items:center !important;}.js-plotly-plot .plotly *{font-family:"SST Arabic","SSTArabic","IBM Plex Sans Arabic",Tahoma,Arial,sans-serif !important;}[data-testid="stDataFrame"]{direction:rtl !important;}[data-testid="stDataFrame"] *{font-family:"SST Arabic","SSTArabic","IBM Plex Sans Arabic",Tahoma,Arial,sans-serif !important;}[data-testid="stDataFrame"] div[role="gridcell"]{text-align:center !important;justify-content:center !important;align-items:center !important;display:flex !important;font-size:13px !important;font-weight:600 !important;}[data-testid="stDataFrame"] div[role="columnheader"]{text-align:center !important;justify-content:center !important;align-items:center !important;display:flex !important;font-size:13px !important;font-weight:800 !important;}[data-testid="stDataFrame"] div[role="columnheader"] *{text-align:center !important;justify-content:center !important;}[data-testid="stDataFrame"] div[role="gridcell"] *{text-align:center !important;justify-content:center !important;}.metric-label,.metric-value{text-align:center !important;width:100% !important;}.stTabs [data-baseweb="tab"]{justify-content:center !important;align-items:center !important;font-family:"SST Arabic","SSTArabic","IBM Plex Sans Arabic",Tahoma,Arial,sans-serif !important;}.js-plotly-plot .plotly *{font-family:"SST Arabic","SSTArabic","IBM Plex Sans Arabic",Tahoma,Arial,sans-serif !important;}[data-testid="stDataFrame"] div[role="grid"]{direction:rtl !important;}[data-testid="stDataFrame"] [role="columnheader"]{display:flex !important;align-items:center !important;justify-content:center !important;text-align:center !important;font-family:"SST Arabic","SSTArabic",Tahoma,Arial,sans-serif !important;font-weight:800 !important;}[data-testid="stDataFrame"] [role="gridcell"]{display:flex !important;align-items:center !important;justify-content:center !important;text-align:center !important;font-family:"SST Arabic","SSTArabic",Tahoma,Arial,sans-serif !important;font-weight:600 !important;}[data-testid="stDataFrame"] [role="row"]{min-height:42px !important;}[data-testid="stDataFrame"] canvas{font-family:"SST Arabic","SSTArabic",Tahoma,Arial,sans-serif !important;}.stApp{background-color:#F4F7F9;}html,body,.stApp,.block-container,.stMarkdown,.stDataFrame,.stMetric,p,h1,h2,h3,h4,h5,h6,label,input,textarea,[data-testid="stSidebar"],[data-testid="stTable"],[data-testid="stDataFrame"],[data-baseweb="tab"],[data-baseweb="select"]{font-family:"SST Arabic","SSTArabic","SST Arabic Roman","SST Arabic Medium","IBM Plex Sans Arabic","Tahoma","Arial",sans-serif !important;}html,body,[class*="css"],.stApp,.block-container,.stMarkdown,.stDataFrame,.stMetric{font-size:15px;}.material-icons,.material-icons-outlined,.material-symbols-outlined,.material-symbols-rounded,.material-symbols-sharp,span[class*="material"],span[data-testid="stIconMaterial"]{font-family:"Material Symbols Rounded","Material Symbols Outlined","Material Icons" !important;font-weight:normal !important;font-style:normal !important;line-height:1 !important;letter-spacing:normal !important;text-transform:none !important;white-space:nowrap !important;word-wrap:normal !important;direction:ltr !important;-webkit-font-feature-settings:"liga" !important;-webkit-font-smoothing:antialiased !important;}.block-container{padding-top:3.5rem !important;padding-bottom:1rem !important;}h1,h2,h3{margin-top:0 !important;padding-top:0 !important;line-height:1.4 !important;color:#0B3C5D;}.metric-card{background:linear-gradient(135deg,#0B3C5D 0%,#0C8A73 100%);border-radius:16px;padding:12px 16px;width:100%;max-width:260px;margin:0 auto 8px auto;box-shadow:0 6px 14px rgba(0,0,0,0.10);display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;}.metric-card.total{background:linear-gradient(135deg,#1B5E20 0%,#008000 100%);}.metric-card.light{background:#FFFFFF;box-shadow:0 8px 18px rgba(15,23,42,0.08);}.metric-card.light .metric-label{color:#25324D !important;}.metric-card.light .metric-value{color:#101124 !important;}.metric-label{font-size:12px;color:rgba(255,255,255,0.88) !important;font-weight:700;margin-bottom:5px;}.metric-value{font-size:clamp(16px,1.45vw,22px);font-weight:900;color:#FFFFFF !important;line-height:1.1;white-space:nowrap;}section[data-testid="stSidebar"]{background-color:#173A70;}section[data-testid="stSidebar"] *{color:white !important;}section[data-testid="stSidebar"] input,section[data-testid="stSidebar"] textarea,section[data-testid="stSidebar"] div[data-baseweb="select"] *{color:#0B3C5D !important;}section[data-testid="stSidebar"] input,section[data-testid="stSidebar"] textarea,section[data-testid="stSidebar"] div[data-baseweb="select"]{background-color:white !important;}section[data-testid="stFileUploader"]{background:rgba(255,255,255,0.96) !important;border-radius:14px !important;padding:12px !important;border:1px solid rgba(255,255,255,0.35) !important;box-shadow:0 6px 16px rgba(0,0,0,0.12) !important;}section[data-testid="stFileUploader"] label{color:#FFFFFF !important;font-size:13px !important;font-weight:700 !important;}section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"]{min-height:54px !important;padding:8px !important;border-radius:12px !important;background-color:#FFFFFF !important;border:1px dashed #CBD5E1 !important;}.stTabs [data-baseweb="tab-list"]{gap:10px;border-bottom:2px solid #D9E2EC;}.stTabs [data-baseweb="tab"]{height:50px;padding:0 18px;background-color:#EAF1F6;border-radius:12px 12px 0 0;color:#0B3C5D !important;font-weight:700;}.stTabs [data-baseweb="tab"] p{color:#0B3C5D !important;font-weight:700 !important;}.stTabs [aria-selected="true"]{background-color:#0B3C5D !important;color:white !important;}.stTabs [aria-selected="true"] p{color:white !important;}div[data-testid="stDataFrame"] div[role="grid"]{direction:rtl;}.drill-box{background:#FFFFFF;border:1px solid #D9E2EC;border-radius:16px;padding:14px 16px;margin-bottom:12px;box-shadow:0 6px 14px rgba(15,23,42,0.06);direction:rtl;text-align:right;}.drill-title{font-size:15px;font-weight:800;color:#0B3C5D;margin-bottom:6px;}.drill-path{background:#EAF1F6;border-right:5px solid #0C8A73;border-radius:12px;padding:12px 16px;margin:8px 0 18px 0;color:#0B3C5D;font-weight:800;direction:rtl;text-align:right;}.footer-signature{margin-top:18px;padding-top:10px;font-size:12px;color:#FFFFFF !important;opacity:0.75;background:transparent !important;pointer-events:none;text-align:left;}section[data-testid="stFileUploader"]{background:#FFFFFF !important;border-radius:14px !important;padding:10px !important;margin-bottom:10px !important;box-shadow:0 6px 14px rgba(0,0,0,0.14) !important;}section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"]{min-height:52px !important;height:52px !important;padding:8px 10px !important;background:#FFFFFF !important;border:1px dashed #94A3B8 !important;border-radius:12px !important;}section[data-testid="stFileUploader"] button,section[data-testid="stFileUploader"] button:disabled,section[data-testid="stFileUploader"] button[kind="secondary"],section[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"]{background:#F8FAFC !important;background-color:#F8FAFC !important;border:1px solid #CBD5E1 !important;border-radius:10px !important;color:#0B3C5D !important;-webkit-text-fill-color:#0B3C5D !important;opacity:1 !important;filter:none !important;min-height:34px !important;height:34px !important;min-width:96px !important;padding:0 12px !important;box-shadow:none !important;font-weight:800 !important;}section[data-testid="stFileUploader"] button *,section[data-testid="stFileUploader"] button:disabled *,section[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] *{color:#0B3C5D !important;-webkit-text-fill-color:#0B3C5D !important;fill:#0B3C5D !important;opacity:1 !important;filter:none !important;font-weight:800 !important;}section[data-testid="stFileUploader"] div,section[data-testid="stFileUploader"] span,section[data-testid="stFileUploader"] small,section[data-testid="stFileUploader"] p{color:#0B3C5D !important;-webkit-text-fill-color:#0B3C5D !important;opacity:1 !important;}section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"]{gap:0.35rem !important;}section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div{margin-bottom:0 !important;padding-bottom:0 !important;}section[data-testid="stSidebar"] .stMultiSelect,section[data-testid="stSidebar"] .stRadio{margin-bottom:4px !important;}section[data-testid="stSidebar"] label{margin-bottom:2px !important;}.material-icons,.material-icons-outlined,.material-symbols-outlined,.material-symbols-rounded,span[data-testid="stIconMaterial"]{font-family:"Material Symbols Rounded","Material Symbols Outlined","Material Icons" !important;}section[data-testid="stSidebar"] section[data-testid="stFileUploader"]{background:#FFFFFF !important;border-radius:14px !important;padding:10px !important;margin-bottom:12px !important;box-shadow:0 6px 14px rgba(0,0,0,0.14) !important;}section[data-testid="stSidebar"] section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"]{background:#FFFFFF !important;border:1px dashed #94A3B8 !important;border-radius:12px !important;min-height:54px !important;height:54px !important;padding:8px !important;}section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button,section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button:disabled,section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button[disabled],section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button[kind="secondary"],section[data-testid="stSidebar"] section[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"]{background:#0B3C5D !important;background-color:#0B3C5D !important;border:1px solid #0B3C5D !important;border-radius:10px !important;color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;opacity:1 !important;filter:none !important;box-shadow:0 5px 12px rgba(11,60,93,0.24) !important;min-width:112px !important;min-height:38px !important;height:38px !important;padding:0 14px !important;font-weight:800 !important;}section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button *,section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button:disabled *,section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button[disabled] *,section[data-testid="stSidebar"] section[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] *{color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;fill:#FFFFFF !important;opacity:1 !important;filter:none !important;font-weight:800 !important;}section[data-testid="stSidebar"] section[data-testid="stFileUploader"] div,section[data-testid="stSidebar"] section[data-testid="stFileUploader"] span:not([class*="material"]),section[data-testid="stSidebar"] section[data-testid="stFileUploader"] small,section[data-testid="stSidebar"] section[data-testid="stFileUploader"] p{color:#0B3C5D !important;-webkit-text-fill-color:#0B3C5D !important;opacity:1 !important;}section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button:hover{background:#0C8A73 !important;background-color:#0C8A73 !important;border-color:#0C8A73 !important;}div[data-testid="stMetric"]{text-align:center !important;}div[data-testid="stMetric"] > div{display:flex !important;flex-direction:column !important;align-items:center !important;justify-content:center !important;text-align:center !important;}div[data-testid="stMetricLabel"],div[data-testid="stMetricValue"]{width:100% !important;text-align:center !important;justify-content:center !important;}div[data-testid="stMetricLabel"] label,div[data-testid="stMetricLabel"] p,div[data-testid="stMetricValue"],div[data-testid="stMetricValue"] > div{text-align:center !important;justify-content:center !important;}.material-icons,.material-icons-outlined,.material-symbols-outlined,.material-symbols-rounded,.material-symbols-sharp,span[class*="material"],span[data-testid="stIconMaterial"],[data-testid="stIconMaterial"]{font-family:"Material Symbols Rounded","Material Symbols Outlined","Material Icons" !important;}section[data-testid="stSidebar"] .stButton button{background:#0B3C5D !important;color:#FFFFFF !important;border:1px solid rgba(255,255,255,0.25) !important;border-radius:12px !important;height:42px !important;font-weight:900 !important;box-shadow:0 6px 14px rgba(0,0,0,0.16) !important;}section[data-testid="stSidebar"] .stButton button:hover{background:#0C8A73 !important;color:#FFFFFF !important;border-color:#0C8A73 !important;}div[role="dialog"] *{font-family:"SST Arabic","SSTArabic","SST Arabic Roman","IBM Plex Sans Arabic","Tahoma","Arial",sans-serif !important;}div[role="dialog"] button{border-radius:10px !important;font-weight:800 !important;}div[role="dialog"] section[data-testid="stFileUploader"]{background:#F8FAFC !important;border-radius:16px !important;padding:14px !important;border:1px solid #E2E8F0 !important;}div[role="dialog"] section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"]{border-radius:14px !important;border:1.5px dashed #94A3B8 !important;background:#FFFFFF !important;}</style>""", unsafe_allow_html=True)

# =========================
# تنسيق الواجهة
# =========================


# =========================
# الهيدر مع اللوقو
# =========================
today = datetime.now().strftime("%Y-%m-%d")
logo_path = Path(__file__).parent / "logo.jpeg"

col_logo, col_title, col_date = st.columns([1.1, 5.2, 1.7])

with col_logo:
    if logo_path.exists():
        st.image(str(logo_path), width=130)

with col_title:
    st.markdown(
        """
        <div style='padding-top:8px; text-align:center; width:100%;'>
            <div style='font-size:32px; font-weight:800; color:#0B3C5D; line-height:1.3;'>
                لوحة تكلفة رأس المال البشري
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_date:
    st.markdown(
        f"""
        <div style='padding-top:12px; text-align:right;'>
            <div style='font-size:13px; color:gray;'>تاريخ اليوم</div>
            <div style='font-size:18px; font-weight:bold; color:#0B3C5D;'>{today}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<hr style='margin-top:8px; margin-bottom:22px;'>", unsafe_allow_html=True)


# =========================
# المسارات والثوابت
# =========================
DATA_DIR = Path(__file__).parent / "data"
APP_DIR = Path(__file__).parent
ALERTS_STATUS_PATH = DATA_DIR / "alerts_status.json"

# البحث عن ملف بيانات الموظفين سواء داخل مجلد data أو بجانب pay.py
# مع استبعاد ملفات التكاليف الإضافية مثل العمل الإضافي ورحلات العمل والتذاكر
EXCLUDED_DATA_PATTERNS = ("overtime", "business", "trip", "trips", "ticket", "tickets")

def _is_employee_data_file(path: Path) -> bool:
    name = path.name.lower()
    return path.suffix.lower() == ".xlsx" and not any(token in name for token in EXCLUDED_DATA_PATTERNS)

excel_files = [p for p in DATA_DIR.glob("*.xlsx") if _is_employee_data_file(p)] if DATA_DIR.exists() else []
if not excel_files:
    excel_files = [p for p in APP_DIR.glob("*.xlsx") if _is_employee_data_file(p)]

if not excel_files:
    st.error("لم يتم العثور على ملف Excel لبيانات الموظفين. تأكد من رفع ملف البيانات داخل مجلد data أو بجانب pay.py.")
    st.stop()

DATA_PATH = excel_files[0]

def find_latest_excel(patterns):
    """إرجاع أحدث ملف Excel يطابق أي نمط داخل data أو مجلد التطبيق."""
    candidates = []
    for pattern in patterns:
        if DATA_DIR.exists():
            candidates.extend(DATA_DIR.glob(pattern))
        candidates.extend(APP_DIR.glob(pattern))
    candidates = sorted(set(candidates), key=lambda path: path.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None

# ملفات التكاليف الإضافية المستقلة
OVERTIME_PATH = find_latest_excel(["Overtime*.xlsx", "overtime*.xlsx"])
BUSINESS_TRIPS_PATH = find_latest_excel([
    "مصروف الانتداب والتذاكر*.xlsx", "business_trip*.xlsx",
    "business_trips*.xlsx", "trips*.xlsx"
])

ARABIC_NUM_FORMAT = "{:,.0f}"

AGE_COLUMNS = ['العمر', 'العمر الحالي', 'أعمار الموظفين', 'Age', 'AGE']

MONTH_ORDER = {
    'January': 1, 'يناير': 1,
    'February': 2, 'فبراير': 2,
    'March': 3, 'مارس': 3,
    'April': 4, 'ابريل': 4, 'أبريل': 4,
    'May': 5, 'مايو': 5,
    'June': 6, 'يونيو': 6,
    'July': 7, 'يوليو': 7,
    'August': 8, 'أغسطس': 8, 'اغسطس': 8,
    'September': 9, 'سبتمبر': 9,
    'October': 10, 'أكتوبر': 10, 'اكتوبر': 10,
    'November': 11, 'نوفمبر': 11,
    'December': 12, 'ديسمبر': 12,
    'يوم تأسيس': 13, 'عيد الفطر': 14, 'عيد الأضحى': 15,
}

RENAME_MAP = {
    'الراتب الأساسي ': 'الراتب الأساسي',
    'بدل النقل من الوزارة‎': 'بدل النقل من الوزارة',
    'الإدارة ': 'الإدارة',
    'القسم ': 'القسم',
    'الإدارة العامة ': 'الإدارة العامة',
    'ادارة عامة': 'الإدارة العامة',
    'ادارة عامة ': 'الإدارة العامة',
    'بدل ضرر_وزارة': 'بدل الضرر من الوزارة',
    'مكافأة طبيب_وزارة': 'مكافأة الطبيب من الوزارة',
    'موقع العمل': 'مكان العمل',
    'الموقع الفعلي ': 'الموقع الفعلي',
    'موقع العمل ': 'مكان العمل',
    'تأينات اجتماعية': 'تأمينات اجتماعية',
    'تأمين طيبي': 'تأمين طبي',
    'بنوص': 'بونص',
    'تعويض اجازات': 'تعويض إجازات',
}

# إدارات عامة مستقلة لا تُعامل كقطاعات حتى لو ظهر اسمها في عمود القطاع بالملف
STANDALONE_GENERAL_ADMINS = {
    'الفروع',
    'الشؤون القانونية',
    'الشئون القانونية',
    'الاستراتيجية',
    'الحوكمة',
    'المراجعة الداخلية',
}

# =========================
# دوال مساعدة
# =========================
def clean_text_value(series: pd.Series) -> pd.Series:
    return (
        series.fillna('')
        .astype(str)
        .str.replace('\u200f', '', regex=False)
        .str.replace('\u200e', '', regex=False)
        .str.replace('\xa0', ' ', regex=False)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )

def normalize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """تنظيف أسماء الأعمدة من المسافات والعلامات غير المرئية."""
    dataframe = dataframe.copy()
    dataframe.columns = [
        re.sub(r'\s+', ' ', str(col).replace('\u200f', '').replace('\u200e', '').replace('\xa0', ' ')).strip()
        for col in dataframe.columns
    ]
    return dataframe


def render_financial_table(dataframe: pd.DataFrame):
    """عرض موحد لجميع الجداول المالية في اللوحة."""
    st.dataframe(format_financial_dataframe(dataframe), use_container_width=True, hide_index=True)


def render_tabbed_financial_tables(tables):
    """عرض مجموعة جداول مالية داخل تبويبات Streamlit بشكل موحد."""
    if not tables:
        return

    labels = [label for label, _ in tables]
    tabs = st.tabs(labels)
    for tab, (_, dataframe) in zip(tabs, tables):
        with tab:
            if dataframe is None or dataframe.empty:
                st.info("لا توجد بيانات متاحة حسب الفلاتر الحالية.")
            else:
                render_financial_table(dataframe)


def normalize_employee_type_value(value):
    """توحيد مسميات نوع/كادر الموظف حتى تعمل الفلاتر العامة على كل الملفات."""
    if pd.isna(value):
        return ""
    text_value = str(value)
    text_value = (
        text_value.replace('\u200f', '')
        .replace('\u200e', '')
        .replace('\xa0', ' ')
    )
    text_value = re.sub(r'\s+', ' ', text_value).strip()

    if not text_value or text_value == "0" or text_value.lower() == "nan":
        return ""

    normalized = (
        text_value.replace("أ", "ا")
        .replace("إ", "ا")
        .replace("آ", "ا")
        .replace("ة", "ه")
    )
    normalized = re.sub(r'\s+', ' ', normalized).strip().lower()

    if any(token in normalized for token in ["اعاره", "معار"]):
        return "إعارة"
    if any(token in normalized for token in ["عقد مؤقت", "مؤقت", "temporary", "temp"]):
        return "عقد مؤقت"
    if any(token in normalized for token in ["موظف مباشر", "مباشر", "employee", "موظف"]):
        return "موظف"

    return text_value


def fmt_int(x):
    return ARABIC_NUM_FORMAT.format(x)


def fmt_money(x):
    """تنسيق مختصر للكروت والمؤشرات."""
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "0"

    if x >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    if x >= 1_000:
        return f"{x/1_000:.1f}K"
    return f"{x:,.0f}"


def fmt_money_full(x):
    """تنسيق مالي كامل للتقارير والجداول فقط بفواصل وبدون رمز عملة."""
    try:
        return f"{float(x):,.0f}"
    except (TypeError, ValueError):
        return "0"


def dataframe_to_excel_bytes(dataframe: pd.DataFrame, sheet_name="Report") -> bytes:
    """تحويل DataFrame إلى ملف Excel قابل للتحميل."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    output.seek(0)
    return output.getvalue()


def format_financial_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """تنسيق أعمدة المبالغ والتواريخ في التقارير والجداول فقط، بدون التأثير على الداتا الأصلية."""
    result = dataframe.copy()

    # تنسيق أي عمود تاريخ ليظهر كتاريخ فقط بدون ساعات
    for col in result.columns:
        if 'تاريخ' in str(col):
            formatted_dates = pd.to_datetime(result[col], errors='coerce').dt.strftime('%Y-%m-%d')
            result[col] = formatted_dates.where(formatted_dates.notna(), '')

    financial_keywords = [
        'تكلفة', 'القيمة', 'الإجمالي', 'شهري', 'سنوي',
        'الراتب', 'بدل', 'مكافأة', 'تعويض', 'تأمين', 'بونص', 'علاوة'
    ]
    for col in result.columns:
        if any(keyword in str(col) for keyword in financial_keywords):
            if pd.api.types.is_numeric_dtype(result[col]):
                result[col] = result[col].map(fmt_money_full)
    return result


def valid_text_mask(series: pd.Series) -> pd.Series:
    """تمييز القيم النصية الصالحة واستبعاد الفراغ و0 وnan."""
    cleaned = clean_text_value(series)
    return (
        (cleaned != "") &
        (cleaned != "0") &
        (cleaned.str.lower() != "nan")
    )


def _safe_anniversary_date(hire_date, target_year):
    """إرجاع تاريخ الذكرى السنوية بشكل آمن، مع معالجة 29 فبراير."""
    if pd.isna(hire_date):
        return pd.NaT

    hire_ts = pd.to_datetime(hire_date, errors='coerce')
    if pd.isna(hire_ts):
        return pd.NaT

    month = int(hire_ts.month)
    day = int(hire_ts.day)

    try:
        return pd.Timestamp(year=int(target_year), month=month, day=day)
    except ValueError:
        # في حالة 29 فبراير والسنة القادمة ليست كبيسة
        return pd.Timestamp(year=int(target_year), month=2, day=28)


def build_anniversary_alerts(dataframe: pd.DataFrame, today_date=None) -> pd.DataFrame:
    """
    بناء تنبيهات الاستحقاق السنوي من تاريخ التعيين لجميع أنواع الموظفين.
    التصنيف اللوني:
    - أحمر: أقل من 60 يوم
    - برتقالي: من 60 إلى 70 يوم
    - أخضر: أكثر من 70 يوم
    """
    result = dataframe.copy()
    today_ts = pd.Timestamp(today_date or datetime.now().date()).normalize()

    if 'تاريخ التعيين' not in result.columns:
        result['تاريخ الاستحقاق القادم'] = pd.NaT
        result['الأيام المتبقية'] = pd.NA
        result['حالة الاستحقاق'] = 'غير محدد'
        result['مؤشر الاستحقاق'] = '⚪ غير محدد'
        result['الإجراء المقترح'] = 'التحقق من توفر تاريخ التعيين'
        return result

    hire_dates = pd.to_datetime(result['تاريخ التعيين'], errors='coerce')
    next_dates = hire_dates.apply(lambda x: _safe_anniversary_date(x, today_ts.year))

    # إذا كان تاريخ الذكرى لهذه السنة مضى، ننتقل للذكرى القادمة في السنة التالية
    passed_mask = next_dates.notna() & (next_dates < today_ts)
    next_dates.loc[passed_mask] = hire_dates.loc[passed_mask].apply(
        lambda x: _safe_anniversary_date(x, today_ts.year + 1)
    )

    result['تاريخ الاستحقاق القادم'] = pd.to_datetime(next_dates).dt.strftime('%Y-%m-%d')
    result['الأيام المتبقية'] = (next_dates - today_ts).dt.days.astype('Int64')

    def _status(days):
        if pd.isna(days):
            return 'غير محدد'
        if days < 60:
            return 'حرج'
        if 60 <= days <= 70:
            return 'تنبيه'
        return 'مستقر'

    result['حالة الاستحقاق'] = result['الأيام المتبقية'].apply(_status)
    result['مؤشر الاستحقاق'] = result['حالة الاستحقاق'].map({
        'حرج': '🔴 حرج',
        'تنبيه': '🟠 تنبيه',
        'مستقر': '🟢 مستقر',
        'غير محدد': '⚪ غير محدد',
    }).fillna('⚪ غير محدد')

    result['الإجراء المقترح'] = result['حالة الاستحقاق'].map({
        'حرج': 'مراجعة عاجلة واتخاذ قرار التمديد أو الإنهاء',
        'تنبيه': 'التحضير للإجراء ومراجعة الاحتياج والتكلفة',
        'مستقر': 'متابعة دورية دون إجراء عاجل',
        'غير محدد': 'التحقق من توفر تاريخ التعيين',
    }).fillna('التحقق من توفر تاريخ التعيين')

    return result


def alert_status_order(series: pd.Series) -> pd.Series:
    """ترتيب الحالات في جداول التنبيه من الأكثر أهمية إلى الأقل."""
    order_map = {'حرج': 1, 'تنبيه': 2, 'مستقر': 3, 'غير محدد': 4}
    return series.map(order_map).fillna(4)


def load_alerts_status() -> dict:
    """قراءة سجل الحالات المعالجة دون تعديل ملف بيانات الموظفين."""
    try:
        if ALERTS_STATUS_PATH.exists():
            with open(ALERTS_STATUS_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}
    return {}


def save_alerts_status(status_data: dict) -> None:
    """حفظ سجل الحالات المعالجة في ملف جانبي خاص باللوحة."""
    ALERTS_STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ALERTS_STATUS_PATH, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, ensure_ascii=False, indent=2)


def build_alert_key(row) -> str:
    """مفتاح فريد للحالة: الموظف + حالة الاستحقاق + تاريخ الاستحقاق القادم."""
    person_id = str(row.get('معرّف الشخص', '')).strip()
    status = str(row.get('حالة الاستحقاق', '')).strip()
    due_date = str(row.get('تاريخ الاستحقاق القادم', '')).strip()
    return f"{person_id}_{status}_{due_date}"


def build_org_unit(dataframe: pd.DataFrame) -> pd.Series:
    """بناء الجهة للـ تحليل القوى العاملة بدون ترك أي جهة فارغة."""
    result = pd.Series("غير محدد", index=dataframe.index, dtype="object")

    if 'القطاع' in dataframe.columns:
        sector = clean_text_value(dataframe['القطاع'])
        mask = valid_text_mask(dataframe['القطاع'])
        result = result.where(~mask, sector)

    if 'الإدارة العامة' in dataframe.columns:
        general_admin = clean_text_value(dataframe['الإدارة العامة'])
        mask_missing = result.eq("غير محدد")
        mask_ga = valid_text_mask(dataframe['الإدارة العامة'])
        result = result.where(~(mask_missing & mask_ga), general_admin)

    if 'الإدارة' in dataframe.columns:
        admin = clean_text_value(dataframe['الإدارة'])
        mask_missing = result.eq("غير محدد")
        mask_admin = valid_text_mask(dataframe['الإدارة'])
        result = result.where(~(mask_missing & mask_admin), admin)
    result = clean_text_value(result)
    result = result.where(valid_text_mask(result), "غير محدد")
    return result


@st.cache_data
def load_data(file_bytes=None):
    if file_bytes is None:
        xl = pd.ExcelFile(DATA_PATH)
    else:
        xl = pd.ExcelFile(file_bytes)

    raw = pd.read_excel(xl, sheet_name='ناتج ملف Excel', header=2)
    raw = normalize_columns(raw)
    raw = raw.rename(columns=RENAME_MAP)
    raw = raw.dropna(how='all')

    if 'معرّف الشخص' in raw.columns:
        raw = raw[raw['معرّف الشخص'].notna()].copy()

    required = [
        'معرّف الشخص', 'الدرجة الوظيفية', 'الإدارة', 'الإدارة العامة', 'القطاع', 'مكان العمل', 'الموقع الفعلي',
        'تاريخ التعيين', 'نوع الموظف',
        'الراتب الأساسي MEWA', 'الراتب الأساسي',
        'بدل النقل', 'بدل السكن', 'بدل إتصال', 'بدل تعليم',
        'تعويض إجازات', 'مكافأة نهاية خدمة', 'تأمينات اجتماعية', 'تأمين طبي',
        'علاوة 4%', 'بونص',
        'بدل النقل من الوزارة', 'بدل الضرر من الوزارة', 'مكافأة الطبيب من الوزارة',
        'بدل المناوبة', 'بدل طبيعة عمل',
        'الإجمالي الشهري', 'الإجمالي السنوي', 'الإجمالي السنوي+ MEWA',
        'العمر', 'العمر الحالي', 'أعمار الموظفين', 'Age', 'AGE'
    ]

    existing = [c for c in required if c in raw.columns]
    df = raw[existing].copy()

    text_cols = ['الإدارة', 'الإدارة العامة', 'القطاع', 'مكان العمل', 'الموقع الفعلي', 'نوع الموظف', 'الدرجة الوظيفية']
    for c in text_cols:
        if c in df.columns:
            df[c] = clean_text_value(df[c])

    if 'نوع الموظف' in df.columns:
        df['نوع الموظف'] = df['نوع الموظف'].apply(normalize_employee_type_value)

    # تصحيح هيكلي: الإدارات العامة المستقلة لا تظهر ضمن القطاعات
    # مثال: الفروع إدارة عامة بدون قطاع، لذلك إذا ظهر اسمها في عمود القطاع يتم تفريغه
    # لتبقى محسوبة في ملخص الإدارات العامة ولا تدخل في ملخص القطاعات.
    if 'القطاع' in df.columns and 'الإدارة العامة' in df.columns:
        standalone_mask = (
            df['الإدارة العامة'].isin(STANDALONE_GENERAL_ADMINS) &
            df['القطاع'].isin(STANDALONE_GENERAL_ADMINS)
        )
        df.loc[standalone_mask, 'القطاع'] = ''

    numeric_cols = [
        'معرّف الشخص',
        'الراتب الأساسي MEWA', 'الراتب الأساسي',
        'بدل النقل', 'بدل السكن', 'بدل إتصال', 'بدل تعليم',
        'تعويض إجازات', 'مكافأة نهاية خدمة', 'تأمينات اجتماعية', 'تأمين طبي',
        'علاوة 4%', 'بونص',
        'بدل النقل من الوزارة', 'بدل الضرر من الوزارة', 'مكافأة الطبيب من الوزارة',
        'بدل المناوبة', 'بدل طبيعة عمل',
        'الإجمالي الشهري', 'الإجمالي السنوي', 'الإجمالي السنوي+ MEWA',
        'العمر', 'العمر الحالي', 'أعمار الموظفين', 'Age', 'AGE'
    ]

    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

    if 'تاريخ التعيين' in df.columns:
        df['تاريخ التعيين'] = pd.to_datetime(df['تاريخ التعيين'], errors='coerce')

    # =========================
    # احتساب التكاليف بشكل موثوق
    # =========================
    company_component_cols = [
        'الراتب الأساسي', 'بدل النقل', 'بدل السكن', 'بدل إتصال', 'بدل تعليم',
        'تعويض إجازات', 'مكافأة نهاية خدمة', 'تأمينات اجتماعية', 'تأمين طبي',
        'علاوة 4%', 'بونص', 'بدل المناوبة', 'بدل طبيعة عمل'
    ]
    company_component_cols = [c for c in company_component_cols if c in df.columns]

    ministry_component_cols = [
        'الراتب الأساسي MEWA', 'بدل النقل من الوزارة',
        'بدل الضرر من الوزارة', 'مكافأة الطبيب من الوزارة'
    ]
    ministry_component_cols = [c for c in ministry_component_cols if c in df.columns]

    calculated_company_monthly = (
        df[company_component_cols].sum(axis=1) if company_component_cols else pd.Series(0, index=df.index)
    )
    calculated_ministry_monthly = (
        df[ministry_component_cols].sum(axis=1) if ministry_component_cols else pd.Series(0, index=df.index)
    )

    # نعتمد الإجمالي الشهري إذا كان موجوداً، وإذا كان صفراً أو فارغاً نحسبه من البنود التفصيلية
    if 'الإجمالي الشهري' in df.columns:
        df['تكلفة الشركة الشهرية'] = df['الإجمالي الشهري'].where(df['الإجمالي الشهري'] > 0, calculated_company_monthly)
    else:
        df['تكلفة الشركة الشهرية'] = calculated_company_monthly

    if 'الإجمالي السنوي' in df.columns:
        df['تكلفة الشركة السنوية'] = df['الإجمالي السنوي'].where(df['الإجمالي السنوي'] > 0, df['تكلفة الشركة الشهرية'] * 12)
    else:
        df['تكلفة الشركة السنوية'] = df['تكلفة الشركة الشهرية'] * 12

    # تكلفة الوزارة الشهرية من بنود الوزارة مباشرة؛ وإذا لم تتوفر البنود نستخدم الفرق السنوي كخطة بديلة
    if ministry_component_cols:
        df['تكلفة الوزارة الشهرية'] = calculated_ministry_monthly.clip(lower=0)
    elif 'الإجمالي السنوي+ MEWA' in df.columns and 'تكلفة الشركة السنوية' in df.columns:
        df['تكلفة الوزارة الشهرية'] = ((df['الإجمالي السنوي+ MEWA'] - df['تكلفة الشركة السنوية']) / 12).clip(lower=0)
    else:
        df['تكلفة الوزارة الشهرية'] = 0

    df['تكلفة الوزارة السنوية'] = (df['تكلفة الوزارة الشهرية'] * 12).clip(lower=0)
    df['التكلفة الشهرية الإجمالية'] = df['تكلفة الشركة الشهرية'] + df['تكلفة الوزارة الشهرية']
    df['التكلفة السنوية الإجمالية'] = df['تكلفة الشركة السنوية'] + df['تكلفة الوزارة السنوية']

    return df


def normalize_employee_status_value(value):
    """توحيد حالة الموظف مع إبقاء مصدرها من ملف العمل الإضافي/رحلات العمل نفسه."""
    if pd.isna(value):
        return "غير محدد"
    text = str(value).replace('\u200f', '').replace('\u200e', '').replace('\xa0', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    if not text or text == '0' or text.lower() == 'nan':
        return "غير محدد"
    normalized = (text.lower()
                  .replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه'))
    if normalized in {'active', 'نشط', 'فعال', 'على راس العمل', 'على رأس العمل'}:
        return 'نشط'
    if normalized in {'inactive', 'غير نشط', 'غير فعال', 'منتهي', 'انهاء خدمات', 'انهاء خدمه'}:
        return 'غير نشط'
    return text


@st.cache_data
def load_work_extra_data():
    """تحميل ملف العمل الإضافي المستقل وتحويله من شكل الأشهر كأعمدة إلى شكل تحليلي."""
    if OVERTIME_PATH is None:
        return pd.DataFrame(), pd.DataFrame()

    raw = pd.read_excel(OVERTIME_PATH)
    raw = normalize_columns(raw)

    rename_map = {
        'Personnel Number': 'الرقم الوظيفي',
        'معرف الشخص': 'الرقم الوظيفي',
        'معرّف الشخص': 'الرقم الوظيفي',
        'Employee ID': 'الرقم الوظيفي',
        'الإدارة العامة ': 'الإدارة العامة',
        'الإدارة ': 'الإدارة',
        'نوع الموظف ': 'نوع الموظف',
        'Employee Type': 'نوع الموظف',
        'employee type': 'نوع الموظف',
        'Status': 'حالة الموظف',
        'status': 'حالة الموظف',
        'Employee Status': 'حالة الموظف',
        'employee status': 'حالة الموظف',
        'حالة الموظف ': 'حالة الموظف',
        'كادر الموظف ': 'كادر الموظف',
        'Cadre': 'كادر الموظف',
        'cadre': 'كادر الموظف',
        'الموقع الفعلي ': 'الموقع الفعلي',
        'موقع العمل الفعلي': 'الموقع الفعلي',
        'Actual Location': 'الموقع الفعلي',
        'actual location': 'الموقع الفعلي',
        'عيد الفطر ': 'عيد الفطر',
        'الاجمالي الكلي': 'الإجمالي الكلي',
        'إجمالي كلي': 'الإجمالي الكلي',
        'total': 'الإجمالي الكلي',
    }
    raw = raw.rename(columns=rename_map).dropna(how='all')

    required_text_cols = ['القطاع', 'الإدارة العامة', 'الإدارة', 'نوع الموظف', 'كادر الموظف', 'الموقع الفعلي', 'حالة الموظف']
    for col in required_text_cols:
        if col in raw.columns:
            raw[col] = clean_text_value(raw[col])
        elif col in ['نوع الموظف', 'كادر الموظف', 'الموقع الفعلي']:
            pass
        else:
            raw[col] = ''

    if 'كادر الموظف' not in raw.columns and 'نوع الموظف' in raw.columns:
        raw['كادر الموظف'] = clean_text_value(raw['نوع الموظف'])
    if 'نوع الموظف' not in raw.columns and 'كادر الموظف' in raw.columns:
        raw['نوع الموظف'] = clean_text_value(raw['كادر الموظف'])
    if 'كادر الموظف' in raw.columns:
        raw['كادر الموظف'] = raw['كادر الموظف'].apply(normalize_employee_type_value)
    if 'نوع الموظف' in raw.columns:
        raw['نوع الموظف'] = raw['نوع الموظف'].apply(normalize_employee_type_value)
    if 'حالة الموظف' in raw.columns:
        raw['حالة الموظف'] = raw['حالة الموظف'].apply(normalize_employee_status_value)
    else:
        raw['حالة الموظف'] = 'غير محدد'

    if 'الرقم الوظيفي' not in raw.columns:
        return pd.DataFrame(), pd.DataFrame()

    raw['الرقم الوظيفي'] = pd.to_numeric(raw['الرقم الوظيفي'], errors='coerce')
    raw = raw[raw['الرقم الوظيفي'].notna()].copy()
    raw['الرقم الوظيفي'] = raw['الرقم الوظيفي'].astype('Int64')

    dimension_cols = ['م', 'الرقم الوظيفي', 'اسم الموظف', 'نوع الموظف', 'كادر الموظف', 'حالة الموظف', 'القطاع', 'الإدارة العامة', 'الإدارة', 'الموقع الفعلي', 'الإجمالي الكلي']
    amount_cols = [c for c in raw.columns if c not in dimension_cols]

    for col in amount_cols + (['الإجمالي الكلي'] if 'الإجمالي الكلي' in raw.columns else []):
        if col in raw.columns:
            raw[col] = pd.to_numeric(raw[col], errors='coerce').fillna(0)

    if 'الإجمالي الكلي' not in raw.columns:
        raw['الإجمالي الكلي'] = raw[amount_cols].sum(axis=1) if amount_cols else 0

    long_df = raw.melt(
        id_vars=[c for c in ['الرقم الوظيفي', 'اسم الموظف', 'نوع الموظف', 'كادر الموظف', 'حالة الموظف', 'القطاع', 'الإدارة العامة', 'الإدارة', 'الموقع الفعلي'] if c in raw.columns],
        value_vars=amount_cols,
        var_name='الشهر / المناسبة',
        value_name='مبلغ العمل الإضافي'
    )

    long_df['مبلغ العمل الإضافي'] = pd.to_numeric(long_df['مبلغ العمل الإضافي'], errors='coerce').fillna(0)
    long_df = long_df[long_df['مبلغ العمل الإضافي'] > 0].copy()

    long_df['_ترتيب_الشهر'] = long_df['الشهر / المناسبة'].map(MONTH_ORDER).fillna(99)

    return raw, long_df


@st.cache_data
def load_business_trips_data():
    """تحميل ملف رحلات العمل والتذاكر وتحويله إلى شكل موحد للتحليل."""
    if BUSINESS_TRIPS_PATH is None:
        return pd.DataFrame()

    xl = pd.ExcelFile(BUSINESS_TRIPS_PATH)
    sheet_name = "تفاصيل" if "تفاصيل" in xl.sheet_names else xl.sheet_names[0]
    raw = pd.read_excel(xl, sheet_name=sheet_name)

    raw = normalize_columns(raw)

    rename_map = {
        'Person ID': 'الرقم الوظيفي',
        'Personnel Number': 'الرقم الوظيفي',
        'معرف الشخص': 'الرقم الوظيفي',
        'معرّف الشخص': 'الرقم الوظيفي',
        'Pay Grade (Label)': 'الدرجة الوظيفية',
        'Employee Type': 'نوع الموظف',
        'employee type': 'نوع الموظف',
        'نوع الموظف ': 'نوع الموظف',
        'Status': 'حالة الموظف',
        'حالة الموظف ': 'حالة الموظف',
        'الإدارة ': 'الإدارة',
        'الإدارة العامة ': 'الإدارة العامة',
        'الموقع الفعلي ': 'الموقع الفعلي',
        'From Date': 'تاريخ البداية',
        'To': 'تاريخ النهاية',
        'month': 'الشهر',
        'Month': 'الشهر',
        'Numberofdays': 'عدد الأيام',
        'Number of days': 'عدد الأيام',
        'Trip Reason (Picklist Label)': 'سبب الرحلة',
        'Region (Picklist Label)': 'المنطقة',
        'Travel From (Picklist Label)': 'نقطة الانطلاق',
        'City (Picklist Label)': 'المدينة',
        'Class (Picklist Label)': 'درجة السفر',
        'Perdiem': 'بدل الانتداب',
        'BusinessTrip Ticket': 'قيمة التذكرة',
    }
    raw = raw.rename(columns=rename_map).dropna(how='all')

    if 'الرقم الوظيفي' not in raw.columns:
        return pd.DataFrame()

    raw['الرقم الوظيفي'] = pd.to_numeric(raw['الرقم الوظيفي'], errors='coerce')
    raw = raw[raw['الرقم الوظيفي'].notna()].copy()
    raw['الرقم الوظيفي'] = raw['الرقم الوظيفي'].astype('Int64')

    text_cols = [
        'نوع الموظف', 'حالة الموظف', 'القطاع', 'الإدارة العامة', 'الإدارة',
        'الموقع الفعلي', 'الشهر', 'سبب الرحلة', 'المنطقة',
        'نقطة الانطلاق', 'المدينة', 'درجة السفر', 'الدرجة الوظيفية'
    ]
    for col in text_cols:
        if col in raw.columns:
            raw[col] = clean_text_value(raw[col])

    if 'نوع الموظف' in raw.columns:
        raw['نوع الموظف'] = raw['نوع الموظف'].apply(normalize_employee_type_value)
    else:
        raw['نوع الموظف'] = 'غير محدد'

    if 'حالة الموظف' in raw.columns:
        raw['حالة الموظف'] = raw['حالة الموظف'].apply(normalize_employee_status_value)
    else:
        raw['حالة الموظف'] = 'غير محدد'

    for col in ['القطاع', 'الإدارة العامة', 'الإدارة', 'الموقع الفعلي', 'الشهر', 'سبب الرحلة', 'المنطقة', 'نقطة الانطلاق', 'المدينة', 'درجة السفر']:
        if col not in raw.columns:
            raw[col] = ''

    for col in ['بدل الانتداب', 'قيمة التذكرة', 'عدد الأيام']:
        if col in raw.columns:
            raw[col] = pd.to_numeric(raw[col], errors='coerce').fillna(0)
        else:
            raw[col] = 0

    if 'تاريخ البداية' in raw.columns:
        raw['تاريخ البداية'] = pd.to_datetime(raw['تاريخ البداية'], errors='coerce')
    if 'تاريخ النهاية' in raw.columns:
        raw['تاريخ النهاية'] = pd.to_datetime(raw['تاريخ النهاية'], errors='coerce')

    raw['إجمالي تكلفة الرحلة'] = raw['بدل الانتداب'] + raw['قيمة التذكرة']

    raw['_ترتيب_الشهر'] = raw['الشهر'].map(MONTH_ORDER).fillna(99)

    return raw


GLOBAL_FILTER_COLUMNS = {
    'sector': 'القطاع',
    'general_admin': 'الإدارة العامة',
    'admin': 'الإدارة',
    'location': 'الموقع الفعلي',
}

def apply_global_filters(dataframe: pd.DataFrame, employee_type_columns=('نوع الموظف', 'كادر الموظف')) -> pd.DataFrame:
    """محرك موحد لتطبيق فلاتر اللوحة على أي مصدر بيانات يدعم الأعمدة التنظيمية."""
    result = dataframe.copy()
    if result.empty:
        return result

    if type_choice != "الكل":
        selected_type = normalize_employee_type_value(type_choice)
        type_col = next((c for c in employee_type_columns if c in result.columns), None)
        if type_col:
            result = result[result[type_col].apply(normalize_employee_type_value).eq(selected_type)]

    filter_values = {
        GLOBAL_FILTER_COLUMNS['sector']: sector_choice,
        GLOBAL_FILTER_COLUMNS['general_admin']: general_admin_choice,
        GLOBAL_FILTER_COLUMNS['admin']: admin_choice,
        GLOBAL_FILTER_COLUMNS['location']: location_choice,
    }
    for col, selected_values in filter_values.items():
        if selected_values and col in result.columns:
            result = result[result[col].isin(selected_values)]

    return result

def apply_business_trip_global_filters(trips_df: pd.DataFrame) -> pd.DataFrame:
    """تطبيق المحرك الموحد على رحلات العمل."""
    return apply_global_filters(trips_df, employee_type_columns=('نوع الموظف',))

def get_cascading_filter_options(dataframe: pd.DataFrame, target_col: str, active_filters=None):
    """إرجاع خيارات فلتر مرتبطة بالاختيارات الأعلى منه مع تنظيف القيم غير الصالحة."""
    if target_col not in dataframe.columns:
        return []
    source = dataframe.copy()
    for col, selected_values in (active_filters or {}).items():
        if selected_values and col in source.columns:
            source = source[source[col].isin(selected_values)]
    values = clean_text_value(source[target_col])
    return sorted(values[valid_text_mask(values)].unique().tolist())

def valid_previous_choices(key: str, options):
    """الاحتفاظ فقط بالاختيارات السابقة التي ما زالت صالحة بعد تغيير الفلاتر الأعلى."""
    return [x for x in st.session_state.get(key, []) if x in options]


def prepare_workforce_cost_view(base_df: pd.DataFrame, work_extra_long_df: pd.DataFrame, business_trips_df: pd.DataFrame, company_cost_mode: str) -> pd.DataFrame:
    """تجهيز نسخة العمل للتقارير الرئيسية مع إضافة التكاليف الإضافية إلى تكلفة الشركة فقط في وضع التكلفة الشاملة."""
    result = base_df.copy()

    result['تكلفة الشركة الشهرية الأساسية'] = pd.to_numeric(result.get('تكلفة الشركة الشهرية', 0), errors='coerce').fillna(0)
    result['تكلفة الشركة السنوية الأساسية'] = pd.to_numeric(result.get('تكلفة الشركة السنوية', 0), errors='coerce').fillna(0)

    for col in [
        'تكاليف إضافية شهرية - عمل إضافي',
        'تكاليف إضافية سنوية - عمل إضافي',
        'تكاليف إضافية شهرية - رحلات العمل',
        'تكاليف إضافية سنوية - رحلات العمل',
        'تكاليف القوى العاملة الإضافية الشهرية',
        'تكاليف القوى العاملة الإضافية السنوية',
    ]:
        result[col] = 0.0

    if 'معرّف الشخص' in result.columns:
        result['_person_id_int'] = pd.to_numeric(result['معرّف الشخص'], errors='coerce')

    # العمل الإضافي
    if work_extra_long_df is not None and not work_extra_long_df.empty and '_person_id_int' in result.columns:
        ot = work_extra_long_df.copy()
        ot['الرقم الوظيفي'] = pd.to_numeric(ot.get('الرقم الوظيفي'), errors='coerce')
        ot['مبلغ العمل الإضافي'] = pd.to_numeric(ot.get('مبلغ العمل الإضافي'), errors='coerce').fillna(0)
        ot = ot[ot['الرقم الوظيفي'].notna()].copy()

        if not ot.empty:
            agg_map = {
                'إجمالي_الأوفر_تايم': ('مبلغ العمل الإضافي', 'sum'),
                'القطاع': ('القطاع', 'first'),
                'الإدارة_العامة_أوفر_تايم': ('الإدارة العامة', 'first'),
                'الإدارة_أوفر_تايم': ('الإدارة', 'first'),
            }
            if 'الموقع الفعلي' in ot.columns:
                agg_map['الموقع_الفعلي_أوفر_تايم'] = ('الموقع الفعلي', 'first')
            if 'كادر الموظف' in ot.columns:
                agg_map['نوع_الموظف_أوفر_تايم'] = ('كادر الموظف', 'first')
            elif 'نوع الموظف' in ot.columns:
                agg_map['نوع_الموظف_أوفر_تايم'] = ('نوع الموظف', 'first')
            if 'حالة الموظف' in ot.columns:
                agg_map['حالة_الموظف_أوفر_تايم'] = ('حالة الموظف', 'first')

            ot_by_emp = ot.groupby('الرقم الوظيفي', dropna=False).agg(**agg_map).reset_index()

            result = result.merge(
                ot_by_emp[['الرقم الوظيفي', 'إجمالي_الأوفر_تايم']],
                left_on='_person_id_int',
                right_on='الرقم الوظيفي',
                how='left'
            )

            result['تكاليف إضافية سنوية - عمل إضافي'] = pd.to_numeric(result['إجمالي_الأوفر_تايم'], errors='coerce').fillna(0)
            result['تكاليف إضافية شهرية - عمل إضافي'] = result['تكاليف إضافية سنوية - عمل إضافي'] / 12

            if company_cost_mode == "التكلفة الشاملة":
                # السجلات غير الموجودة في ملف الموظفين تبقى محسوبة من ملف العمل الإضافي،
                # لكن حالتها لا تُستنتج من غيابها عن الملف الرئيسي؛ مصدر الحالة هو ملف العمل الإضافي نفسه.
                existing_ids = set(result['_person_id_int'].dropna().astype(int).tolist())
                unmatched_ot = ot_by_emp[~ot_by_emp['الرقم الوظيفي'].dropna().astype(int).isin(existing_ids)].copy()

                if not unmatched_ot.empty:
                    extra_rows = pd.DataFrame(columns=result.columns)
                    extra_rows['معرّف الشخص'] = unmatched_ot['الرقم الوظيفي'].astype('Int64')
                    extra_rows['القطاع'] = clean_text_value(unmatched_ot['القطاع'])
                    extra_rows['الإدارة العامة'] = clean_text_value(unmatched_ot['الإدارة_العامة_أوفر_تايم'])
                    extra_rows['الإدارة'] = clean_text_value(unmatched_ot['الإدارة_أوفر_تايم'])
                    extra_rows['نوع الموظف'] = unmatched_ot['نوع_الموظف_أوفر_تايم'].apply(normalize_employee_type_value) if 'نوع_الموظف_أوفر_تايم' in unmatched_ot.columns else ''
                    extra_rows['حالة الموظف'] = unmatched_ot['حالة_الموظف_أوفر_تايم'].apply(normalize_employee_status_value) if 'حالة_الموظف_أوفر_تايم' in unmatched_ot.columns else 'غير محدد'
                    extra_rows['الدرجة الوظيفية'] = ''
                    extra_rows['مكان العمل'] = ''
                    extra_rows['الموقع الفعلي'] = clean_text_value(unmatched_ot['الموقع_الفعلي_أوفر_تايم']) if 'الموقع_الفعلي_أوفر_تايم' in unmatched_ot.columns else ''
                    extra_rows['تكلفة الشركة الشهرية الأساسية'] = 0.0
                    extra_rows['تكلفة الشركة السنوية الأساسية'] = 0.0
                    extra_rows['تكاليف إضافية سنوية - عمل إضافي'] = unmatched_ot['إجمالي_الأوفر_تايم'].fillna(0).values
                    extra_rows['تكاليف إضافية شهرية - عمل إضافي'] = extra_rows['تكاليف إضافية سنوية - عمل إضافي'] / 12
                    extra_rows['تكلفة الوزارة الشهرية'] = 0.0
                    extra_rows['تكلفة الوزارة السنوية'] = 0.0
                    result = pd.concat([result, extra_rows], ignore_index=True, sort=False)

            result = result.drop(columns=['الرقم الوظيفي', 'إجمالي_الأوفر_تايم'], errors='ignore')

    # رحلات العمل والتذاكر
    if business_trips_df is not None and not business_trips_df.empty and '_person_id_int' in result.columns:
        trips = business_trips_df.copy()
        trips['الرقم الوظيفي'] = pd.to_numeric(trips.get('الرقم الوظيفي'), errors='coerce')
        trips['إجمالي تكلفة الرحلة'] = pd.to_numeric(trips.get('إجمالي تكلفة الرحلة'), errors='coerce').fillna(0)
        trips = trips[trips['الرقم الوظيفي'].notna()].copy()

        if not trips.empty:
            trips_by_emp = trips.groupby('الرقم الوظيفي', dropna=False).agg(
                إجمالي_رحلات_العمل=('إجمالي تكلفة الرحلة', 'sum'),
                القطاع=('القطاع', 'first'),
                الإدارة_العامة_رحلات=('الإدارة العامة', 'first'),
                الإدارة_رحلات=('الإدارة', 'first'),
                الموقع_الفعلي_رحلات=('الموقع الفعلي', 'first'),
                نوع_الموظف_رحلات=('نوع الموظف', 'first'),
                حالة_الموظف_رحلات=('حالة الموظف', 'first')
            ).reset_index()

            result = result.merge(
                trips_by_emp[['الرقم الوظيفي', 'إجمالي_رحلات_العمل']],
                left_on='_person_id_int',
                right_on='الرقم الوظيفي',
                how='left'
            )

            result['تكاليف إضافية سنوية - رحلات العمل'] = pd.to_numeric(result['إجمالي_رحلات_العمل'], errors='coerce').fillna(0)
            result['تكاليف إضافية شهرية - رحلات العمل'] = result['تكاليف إضافية سنوية - رحلات العمل'] / 12

            if company_cost_mode == "التكلفة الشاملة":
                # السجلات غير الموجودة في ملف الموظفين تبقى محسوبة من ملف الرحلات،
                # وحالة الموظف تؤخذ من ملف رحلات العمل نفسه فقط.
                existing_ids = set(result['_person_id_int'].dropna().astype(int).tolist())
                unmatched_trips = trips_by_emp[~trips_by_emp['الرقم الوظيفي'].dropna().astype(int).isin(existing_ids)].copy()

                if not unmatched_trips.empty:
                    extra_rows = pd.DataFrame(columns=result.columns)
                    extra_rows['معرّف الشخص'] = unmatched_trips['الرقم الوظيفي'].astype('Int64')
                    extra_rows['القطاع'] = clean_text_value(unmatched_trips['القطاع'])
                    extra_rows['الإدارة العامة'] = clean_text_value(unmatched_trips['الإدارة_العامة_رحلات'])
                    extra_rows['الإدارة'] = clean_text_value(unmatched_trips['الإدارة_رحلات'])
                    extra_rows['نوع الموظف'] = unmatched_trips['نوع_الموظف_رحلات'].apply(normalize_employee_type_value)
                    extra_rows['حالة الموظف'] = unmatched_trips['حالة_الموظف_رحلات'].apply(normalize_employee_status_value)
                    extra_rows['الدرجة الوظيفية'] = ''
                    extra_rows['مكان العمل'] = ''
                    extra_rows['الموقع الفعلي'] = clean_text_value(unmatched_trips['الموقع_الفعلي_رحلات'])
                    extra_rows['تكلفة الشركة الشهرية الأساسية'] = 0.0
                    extra_rows['تكلفة الشركة السنوية الأساسية'] = 0.0
                    extra_rows['تكاليف إضافية سنوية - رحلات العمل'] = unmatched_trips['إجمالي_رحلات_العمل'].fillna(0).values
                    extra_rows['تكاليف إضافية شهرية - رحلات العمل'] = extra_rows['تكاليف إضافية سنوية - رحلات العمل'] / 12
                    extra_rows['تكلفة الوزارة الشهرية'] = 0.0
                    extra_rows['تكلفة الوزارة السنوية'] = 0.0
                    result = pd.concat([result, extra_rows], ignore_index=True, sort=False)

            result = result.drop(columns=['الرقم الوظيفي', 'إجمالي_رحلات_العمل'], errors='ignore')

    for col in [
        'تكاليف إضافية شهرية - عمل إضافي',
        'تكاليف إضافية سنوية - عمل إضافي',
        'تكاليف إضافية شهرية - رحلات العمل',
        'تكاليف إضافية سنوية - رحلات العمل',
    ]:
        result[col] = pd.to_numeric(result.get(col, 0), errors='coerce').fillna(0)

    result['تكاليف القوى العاملة الإضافية الشهرية'] = result['تكاليف إضافية شهرية - عمل إضافي'] + result['تكاليف إضافية شهرية - رحلات العمل']
    result['تكاليف القوى العاملة الإضافية السنوية'] = result['تكاليف إضافية سنوية - عمل إضافي'] + result['تكاليف إضافية سنوية - رحلات العمل']

    if company_cost_mode == "التكلفة الشاملة":
        result['تكلفة الشركة الشهرية'] = result['تكلفة الشركة الشهرية الأساسية'] + result['تكاليف القوى العاملة الإضافية الشهرية']
        result['تكلفة الشركة السنوية'] = result['تكلفة الشركة السنوية الأساسية'] + result['تكاليف القوى العاملة الإضافية السنوية']
    else:
        result['تكلفة الشركة الشهرية'] = result['تكلفة الشركة الشهرية الأساسية']
        result['تكلفة الشركة السنوية'] = result['تكلفة الشركة السنوية الأساسية']

    result['تكلفة الوزارة الشهرية'] = pd.to_numeric(result.get('تكلفة الوزارة الشهرية', 0), errors='coerce').fillna(0)
    result['تكلفة الوزارة السنوية'] = pd.to_numeric(result.get('تكلفة الوزارة السنوية', 0), errors='coerce').fillna(0)
    result['التكلفة الشهرية الإجمالية'] = result['تكلفة الشركة الشهرية'] + result['تكلفة الوزارة الشهرية']
    result['التكلفة السنوية الإجمالية'] = result['تكلفة الشركة السنوية'] + result['تكلفة الوزارة السنوية']

    return result


def apply_work_extra_filters(work_extra_long_df: pd.DataFrame) -> pd.DataFrame:
    """تطبيق المحرك الموحد على بيانات العمل الإضافي."""
    return apply_global_filters(work_extra_long_df, employee_type_columns=('كادر الموظف', 'نوع الموظف'))


def render_work_extra_tab(work_extra_raw_df: pd.DataFrame, work_extra_long_df: pd.DataFrame, current_employee_df: pd.DataFrame):
    st.subheader("العمل الإضافي")
    if work_extra_raw_df.empty or work_extra_long_df.empty:
        st.info("لم يتم العثور على ملف العمل الإضافي أو لا توجد مبالغ عمل إضافي صالحة للعرض.")
        st.caption("ضع ملف العمل الإضافي داخل مجلد data أو بجانب pay.py.")
        return

    ot_base = apply_work_extra_filters(work_extra_long_df)

    if ot_base.empty:
        st.warning("لا توجد بيانات عمل إضافي مطابقة للفلاتر الحالية.")
        return

    # حالة الموظف مصدرها ملف العمل الإضافي نفسه، ولا تُشتق من ملف الموظفين الرئيسي.
    ot_base = ot_base.copy()
    if 'حالة الموظف' not in ot_base.columns:
        ot_base['حالة الموظف'] = 'غير محدد'
    else:
        ot_base['حالة الموظف'] = ot_base['حالة الموظف'].apply(normalize_employee_status_value)

    if 'كادر الموظف' in ot_base.columns:
        ot_base['كادر الموظف'] = ot_base['كادر الموظف'].apply(normalize_employee_type_value)
    elif 'نوع الموظف' in ot_base.columns:
        ot_base['كادر الموظف'] = ot_base['نوع الموظف'].apply(normalize_employee_type_value)
    else:
        ot_base['كادر الموظف'] = 'غير محدد'

    # بناء عمود الجهة حتى يمكن الفلترة بمستوى تنفيذي واحد
    ot_base['الجهة'] = build_org_unit(ot_base)

    # إجماليات قبل فلاتر تبويب العمل الإضافي الداخلية، مع احترام فلاتر اللوحة العامة
    base_total_ot = float(ot_base['مبلغ العمل الإضافي'].sum())
    base_employee_count = int(ot_base['الرقم الوظيفي'].nunique())

    filter_cols = st.columns(3)

    with filter_cols[0]:
        month_options_df = ot_base[['الشهر / المناسبة', '_ترتيب_الشهر']].drop_duplicates().sort_values('_ترتيب_الشهر')
        month_options = month_options_df['الشهر / المناسبة'].tolist()
        month_filter = st.multiselect(
            "الشهر / المناسبة",
            options=month_options,
            default=[],
            key="work_extra_month_filter"
        )

    with filter_cols[1]:
        entity_options = sorted([
            x for x in ot_base['الجهة'].dropna().unique().tolist()
            if str(x).strip() and str(x).strip() not in ["0", "nan", "غير محدد"]
        ])
        entity_filter = st.multiselect(
            "الجهة",
            options=entity_options,
            default=[],
            key="work_extra_entity_filter"
        )

    with filter_cols[2]:
        status_filter = st.radio(
            "حالة الموظف",
            ["الكل", "نشط", "غير نشط"],
            horizontal=True,
            key="work_extra_employee_status_filter"
        )

    ot_filtered = ot_base.copy()

    if month_filter:
        ot_filtered = ot_filtered[ot_filtered['الشهر / المناسبة'].isin(month_filter)].copy()

    if entity_filter:
        ot_filtered = ot_filtered[ot_filtered['الجهة'].isin(entity_filter)].copy()

    if status_filter != "الكل":
        ot_filtered = ot_filtered[ot_filtered['حالة الموظف'].eq(status_filter)].copy()

    if ot_filtered.empty:
        st.warning("لا توجد بيانات عمل إضافي مطابقة للفلاتر المختارة داخل التبويب.")
        st.markdown(
            f"""
            <div class='alert-note'>
                إجمالي العمل الإضافي قبل فلاتر هذا التبويب: <b>{fmt_money_full(base_total_ot)}</b>،
                وعدد المستفيدين: <b>{fmt_int(base_employee_count)}</b>.
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    total_ot = float(ot_filtered['مبلغ العمل الإضافي'].sum())
    benefited_employees = int(ot_filtered['الرقم الوظيفي'].nunique())
    avg_per_employee = total_ot / benefited_employees if benefited_employees else 0
    active_count = int(ot_filtered.loc[ot_filtered['حالة الموظف'].eq('نشط'), 'الرقم الوظيفي'].nunique())
    inactive_count = int(ot_filtered.loc[ot_filtered['حالة الموظف'].eq('غير نشط'), 'الرقم الوظيفي'].nunique())

    kpi_cols = st.columns(5)
    kpis = [
        ("إجمالي العمل الإضافي", fmt_money(total_ot)),
        ("عدد المستفيدين", fmt_int(benefited_employees)),
        ("متوسط الصرف للموظف", fmt_money(avg_per_employee)),
        ("عدد النشطين", fmt_int(active_count)),
        ("عدد غير النشطين", fmt_int(inactive_count)),
    ]

    for col, (label, value) in zip(kpi_cols, kpis):
        col.markdown(
            f"""
            <div class='smart-card' style='min-height:110px; text-align:center; padding:16px 12px;'>
                <div class='smart-card-title'>{label}</div>
                <div class='smart-card-value' style='font-size:24px;'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    status_summary = ot_filtered.groupby('حالة الموظف', dropna=False).agg(
        عدد_الموظفين=('الرقم الوظيفي', 'nunique'),
        إجمالي_الأوفر_تايم=('مبلغ العمل الإضافي', 'sum')
    ).reset_index()

    month_summary = ot_filtered.groupby(['الشهر / المناسبة', '_ترتيب_الشهر'], dropna=False).agg(
        إجمالي_الأوفر_تايم=('مبلغ العمل الإضافي', 'sum'),
        عدد_الموظفين=('الرقم الوظيفي', 'nunique')
    ).reset_index().sort_values('_ترتيب_الشهر')

    entity_ot = ot_filtered.groupby('الجهة', dropna=False).agg(
        عدد_الموظفين=('الرقم الوظيفي', 'nunique'),
        إجمالي_الأوفر_تايم=('مبلغ العمل الإضافي', 'sum')
    ).reset_index().sort_values('إجمالي_الأوفر_تايم', ascending=False)

    sector_ot = ot_filtered.groupby('القطاع', dropna=False).agg(
        عدد_الموظفين=('الرقم الوظيفي', 'nunique'),
        إجمالي_الأوفر_تايم=('مبلغ العمل الإضافي', 'sum')
    ).reset_index().sort_values('إجمالي_الأوفر_تايم', ascending=False)

    general_admin_ot = ot_filtered.groupby('الإدارة العامة', dropna=False).agg(
        عدد_الموظفين=('الرقم الوظيفي', 'nunique'),
        إجمالي_الأوفر_تايم=('مبلغ العمل الإضافي', 'sum')
    ).reset_index().sort_values('إجمالي_الأوفر_تايم', ascending=False)

    admin_ot = ot_filtered.groupby('الإدارة', dropna=False).agg(
        عدد_الموظفين=('الرقم الوظيفي', 'nunique'),
        إجمالي_الأوفر_تايم=('مبلغ العمل الإضافي', 'sum')
    ).reset_index().sort_values('إجمالي_الأوفر_تايم', ascending=False)

    employee_ot = ot_filtered.groupby(['الرقم الوظيفي', 'كادر الموظف', 'الجهة', 'القطاع', 'الإدارة العامة', 'الإدارة', 'حالة الموظف'], dropna=False).agg(
        إجمالي_الأوفر_تايم=('مبلغ العمل الإضافي', 'sum'),
        عدد_الأشهر_والمناسبات=('الشهر / المناسبة', 'nunique')
    ).reset_index().sort_values('إجمالي_الأوفر_تايم', ascending=False)

    chart_cols = st.columns(2)

    with chart_cols[0]:
        render_bar_chart(month_summary, 'الشهر / المناسبة', 'إجمالي_الأوفر_تايم', "توزيع العمل الإضافي حسب الشهر / المناسبة", text='عدد_الموظفين', y_title="إجمالي العمل الإضافي")

    with chart_cols[1]:
        render_bar_chart(entity_ot.head(15), 'الجهة', 'إجمالي_الأوفر_تايم', "أعلى الجهات حسب العمل الإضافي", text='عدد_الموظفين', y_title="إجمالي العمل الإضافي")

    st.markdown("### أعلى الإدارات صرفاً")
    render_bar_chart(admin_ot.head(15), 'الإدارة', 'إجمالي_الأوفر_تايم', "أعلى 15 إدارة حسب العمل الإضافي", text='عدد_الموظفين', y_title="إجمالي العمل الإضافي", height=460)

    detail_cols = ['الرقم الوظيفي', 'كادر الموظف', 'حالة الموظف', 'الجهة', 'القطاع', 'الإدارة العامة', 'الإدارة', 'الموقع الفعلي', 'الشهر / المناسبة', 'مبلغ العمل الإضافي']
    detail_cols = [c for c in detail_cols if c in ot_filtered.columns]
    sort_cols = [c for c in ['_ترتيب_الشهر', 'مبلغ العمل الإضافي'] if c in ot_filtered.columns]
    details_source = ot_filtered.sort_values(sort_cols, ascending=[True, False][:len(sort_cols)]).copy() if sort_cols else ot_filtered.copy()
    details = details_source[detail_cols].copy()
    render_tabbed_financial_tables([
        ("حسب الجهة", entity_ot), ("حسب القطاع", sector_ot),
        ("حسب الإدارة العامة", general_admin_ot), ("حسب الإدارة", admin_ot),
        ("أعلى الموظفين", employee_ot.head(50)), ("التفاصيل الشهرية", details),
    ])

    st.download_button(
        "تحميل بيانات العمل الإضافي CSV",
        ot_filtered.drop(columns=['_ترتيب_الشهر'], errors='ignore').to_csv(index=False).encode("utf-8-sig"),
        "work_extra_analysis.csv",
        "text/csv"
    )


def build_business_trip_monthly_excel(month_summary: pd.DataFrame, details_df: pd.DataFrame) -> bytes:
    """إنشاء تقرير Excel لمقارنة أشهر رحلات العمل من نفس البيانات المفلترة المعروضة في التبويب."""
    output = BytesIO()
    summary_export = month_summary.drop(columns=['_ترتيب_الشهر'], errors='ignore').copy()
    details_export = details_df.drop(columns=['_ترتيب_الشهر'], errors='ignore').copy()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        summary_export.to_excel(writer, index=False, sheet_name='ملخص الأشهر')
        details_export.to_excel(writer, index=False, sheet_name='تفاصيل الرحلات')

        for sheet_name in ['ملخص الأشهر', 'تفاصيل الرحلات']:
            ws = writer.book[sheet_name]
            ws.sheet_view.rightToLeft = True
            ws.freeze_panes = 'A2'
            for column_cells in ws.columns:
                max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
                ws.column_dimensions[column_cells[0].column_letter].width = min(max(max_length + 2, 12), 35)

    output.seek(0)
    return output.getvalue()


def render_business_trips_tab(trips_df: pd.DataFrame, current_employee_df: pd.DataFrame):
    st.subheader("رحلات العمل")
    if trips_df.empty:
        st.info("لم يتم العثور على ملف رحلات العمل والتذاكر أو لا توجد بيانات صالحة للعرض.")
        return

    base = apply_business_trip_global_filters(trips_df)

    if base.empty:
        st.warning("لا توجد بيانات رحلات عمل مطابقة للفلاتر العامة الحالية.")
        return

    # حالة الموظف مصدرها ملف رحلات العمل نفسه، ولا تُشتق من ملف الموظفين الرئيسي.
    base = base.copy()
    if 'حالة الموظف' not in base.columns:
        base['حالة الموظف'] = 'غير محدد'
    else:
        base['حالة الموظف'] = base['حالة الموظف'].apply(normalize_employee_status_value)
    base['الجهة'] = build_org_unit(base)

    filter_row_1 = st.columns(3)
    with filter_row_1[0]:
        month_options_df = base[['الشهر', '_ترتيب_الشهر']].drop_duplicates().sort_values('_ترتيب_الشهر')
        month_options = [x for x in month_options_df['الشهر'].tolist() if str(x).strip()]
        month_filter = st.multiselect("الشهر", options=month_options, default=[], key="business_trip_month_filter")

    with filter_row_1[1]:
        entity_options = sorted([
            x for x in base['الجهة'].dropna().unique().tolist()
            if str(x).strip() and str(x).strip() not in ["0", "nan", "غير محدد"]
        ])
        entity_filter = st.multiselect("الجهة", options=entity_options, default=[], key="business_trip_entity_filter")

    with filter_row_1[2]:
        reason_options = sorted([x for x in base['سبب الرحلة'].dropna().unique().tolist() if str(x).strip() and str(x).strip() not in ["0", "nan"]])
        reason_filter = st.multiselect("سبب الرحلة", options=reason_options, default=[], key="business_trip_reason_filter")

    filter_row_2 = st.columns(3)
    with filter_row_2[0]:
        region_options = sorted([x for x in base['المنطقة'].dropna().unique().tolist() if str(x).strip() and str(x).strip() not in ["0", "nan"]])
        region_filter = st.multiselect("المنطقة", options=region_options, default=[], key="business_trip_region_filter")

    with filter_row_2[1]:
        city_options = sorted([x for x in base['المدينة'].dropna().unique().tolist() if str(x).strip() and str(x).strip() not in ["0", "nan"]])
        city_filter = st.multiselect("المدينة", options=city_options, default=[], key="business_trip_city_filter")

    with filter_row_2[2]:
        class_options = sorted([x for x in base['درجة السفر'].dropna().unique().tolist() if str(x).strip() and str(x).strip() not in ["0", "nan"]])
        class_filter = st.multiselect("درجة السفر", options=class_options, default=[], key="business_trip_class_filter")

    trips_filtered = base.copy()
    if month_filter:
        trips_filtered = trips_filtered[trips_filtered['الشهر'].isin(month_filter)].copy()
    if entity_filter:
        trips_filtered = trips_filtered[trips_filtered['الجهة'].isin(entity_filter)].copy()
    if reason_filter:
        trips_filtered = trips_filtered[trips_filtered['سبب الرحلة'].isin(reason_filter)].copy()
    if region_filter:
        trips_filtered = trips_filtered[trips_filtered['المنطقة'].isin(region_filter)].copy()
    if city_filter:
        trips_filtered = trips_filtered[trips_filtered['المدينة'].isin(city_filter)].copy()
    if class_filter:
        trips_filtered = trips_filtered[trips_filtered['درجة السفر'].isin(class_filter)].copy()

    if trips_filtered.empty:
        st.warning("لا توجد بيانات رحلات عمل مطابقة للفلاتر المختارة داخل التبويب.")
        return

    total_cost = float(trips_filtered['إجمالي تكلفة الرحلة'].sum())
    total_perdiem = float(trips_filtered['بدل الانتداب'].sum())
    total_tickets = float(trips_filtered['قيمة التذكرة'].sum())
    trip_count = int(len(trips_filtered))
    employee_count = int(trips_filtered['الرقم الوظيفي'].nunique())
    avg_trip = total_cost / trip_count if trip_count else 0

    kpi_cols = st.columns(6)
    kpis = [
        ("إجمالي رحلات العمل", fmt_money(total_cost)),
        ("بدل الانتداب", fmt_money(total_perdiem)),
        ("التذاكر", fmt_money(total_tickets)),
        ("عدد الرحلات", fmt_int(trip_count)),
        ("عدد الموظفين", fmt_int(employee_count)),
        ("متوسط تكلفة الرحلة", fmt_money(avg_trip)),
    ]
    for col, (label, value) in zip(kpi_cols, kpis):
        col.markdown(
            f"""
            <div class='smart-card' style='min-height:110px; text-align:center; padding:16px 12px;'>
                <div class='smart-card-title'>{label}</div>
                <div class='smart-card-value' style='font-size:24px;'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    month_summary = trips_filtered.groupby(['الشهر', '_ترتيب_الشهر'], dropna=False).agg(
        إجمالي_رحلات_العمل=('إجمالي تكلفة الرحلة', 'sum'),
        بدل_الانتداب=('بدل الانتداب', 'sum'),
        التذاكر=('قيمة التذكرة', 'sum'),
        عدد_الرحلات=('الرقم الوظيفي', 'count'),
        عدد_الموظفين=('الرقم الوظيفي', 'nunique')
    ).reset_index().sort_values('_ترتيب_الشهر')

    entity_summary = trips_filtered.groupby('الجهة', dropna=False).agg(
        إجمالي_رحلات_العمل=('إجمالي تكلفة الرحلة', 'sum'),
        عدد_الرحلات=('الرقم الوظيفي', 'count'),
        عدد_الموظفين=('الرقم الوظيفي', 'nunique')
    ).reset_index().sort_values('إجمالي_رحلات_العمل', ascending=False)

    sector_summary = trips_filtered.groupby('القطاع', dropna=False).agg(
        إجمالي_رحلات_العمل=('إجمالي تكلفة الرحلة', 'sum'),
        عدد_الرحلات=('الرقم الوظيفي', 'count'),
        عدد_الموظفين=('الرقم الوظيفي', 'nunique')
    ).reset_index().sort_values('إجمالي_رحلات_العمل', ascending=False)

    general_admin_summary = trips_filtered.groupby('الإدارة العامة', dropna=False).agg(
        إجمالي_رحلات_العمل=('إجمالي تكلفة الرحلة', 'sum'),
        عدد_الرحلات=('الرقم الوظيفي', 'count'),
        عدد_الموظفين=('الرقم الوظيفي', 'nunique')
    ).reset_index().sort_values('إجمالي_رحلات_العمل', ascending=False)

    admin_summary = trips_filtered.groupby('الإدارة', dropna=False).agg(
        إجمالي_رحلات_العمل=('إجمالي تكلفة الرحلة', 'sum'),
        عدد_الرحلات=('الرقم الوظيفي', 'count'),
        عدد_الموظفين=('الرقم الوظيفي', 'nunique')
    ).reset_index().sort_values('إجمالي_رحلات_العمل', ascending=False)

    location_summary = trips_filtered.groupby('الموقع الفعلي', dropna=False).agg(
        إجمالي_رحلات_العمل=('إجمالي تكلفة الرحلة', 'sum'),
        عدد_الرحلات=('الرقم الوظيفي', 'count'),
        عدد_الموظفين=('الرقم الوظيفي', 'nunique')
    ).reset_index().sort_values('إجمالي_رحلات_العمل', ascending=False)

    city_summary = trips_filtered.groupby('المدينة', dropna=False).agg(
        إجمالي_رحلات_العمل=('إجمالي تكلفة الرحلة', 'sum'),
        عدد_الرحلات=('الرقم الوظيفي', 'count'),
        عدد_الموظفين=('الرقم الوظيفي', 'nunique')
    ).reset_index().sort_values('إجمالي_رحلات_العمل', ascending=False)

    reason_summary = trips_filtered.groupby('سبب الرحلة', dropna=False).agg(
        إجمالي_رحلات_العمل=('إجمالي تكلفة الرحلة', 'sum'),
        عدد_الرحلات=('الرقم الوظيفي', 'count'),
        عدد_الموظفين=('الرقم الوظيفي', 'nunique')
    ).reset_index().sort_values('إجمالي_رحلات_العمل', ascending=False)

    employee_summary = trips_filtered.groupby(['الرقم الوظيفي', 'نوع الموظف', 'حالة الموظف', 'الجهة', 'القطاع', 'الإدارة العامة', 'الإدارة', 'الموقع الفعلي'], dropna=False).agg(
        إجمالي_رحلات_العمل=('إجمالي تكلفة الرحلة', 'sum'),
        بدل_الانتداب=('بدل الانتداب', 'sum'),
        التذاكر=('قيمة التذكرة', 'sum'),
        عدد_الرحلات=('الرقم الوظيفي', 'count'),
        إجمالي_الأيام=('عدد الأيام', 'sum')
    ).reset_index().sort_values('إجمالي_رحلات_العمل', ascending=False)

    st.markdown("### مقارنة الأشهر")
    fig_month = px.bar(
        month_summary,
        x='الشهر',
        y='إجمالي_رحلات_العمل',
        text='عدد_الرحلات',
        title="تكلفة رحلات العمل حسب الشهر"
    )
    fig_month.update_layout(xaxis_title="", yaxis_title="إجمالي رحلات العمل", height=420)
    fig_month.update_yaxes(tickformat=',.0f')
    render_chart(fig_month)

    month_report_details = trips_filtered.sort_values(
        ['_ترتيب_الشهر', 'إجمالي تكلفة الرحلة'],
        ascending=[True, False]
    ).copy()
    month_excel = build_business_trip_monthly_excel(month_summary, month_report_details)
    st.download_button(
        "تحميل تقرير مقارنة الأشهر Excel",
        data=month_excel,
        file_name="business_trips_monthly_comparison.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_business_trip_monthly_excel"
    )

    render_bar_chart(entity_summary.head(15), 'الجهة', 'إجمالي_رحلات_العمل', "أعلى الجهات حسب تكلفة رحلات العمل", text='عدد_الرحلات', y_title="إجمالي رحلات العمل", height=460)

    detail_cols = [
        'الرقم الوظيفي', 'نوع الموظف', 'حالة الموظف', 'الجهة', 'القطاع', 'الإدارة العامة', 'الإدارة',
        'الموقع الفعلي', 'الشهر', 'عدد الأيام', 'سبب الرحلة', 'المنطقة', 'نقطة الانطلاق',
        'المدينة', 'درجة السفر', 'بدل الانتداب', 'قيمة التذكرة', 'إجمالي تكلفة الرحلة'
    ]
    detail_cols = [c for c in detail_cols if c in trips_filtered.columns]
    details = trips_filtered.sort_values(['_ترتيب_الشهر', 'إجمالي تكلفة الرحلة'], ascending=[True, False]).copy()
    render_tabbed_financial_tables([
        ("حسب الجهة", entity_summary), ("حسب القطاع", sector_summary),
        ("حسب الإدارة العامة", general_admin_summary), ("حسب الإدارة", admin_summary),
        ("حسب الموقع", location_summary), ("حسب المدينة", city_summary),
        ("حسب سبب الرحلة", reason_summary), ("أعلى الموظفين", employee_summary.head(50)),
        ("التفاصيل", details[detail_cols]),
    ])

    st.download_button(
        "تحميل بيانات رحلات العمل CSV",
        trips_filtered.drop(columns=['_ترتيب_الشهر'], errors='ignore').to_csv(index=False).encode("utf-8-sig"),
        "business_trips_analysis.csv",
        "text/csv"
    )

def build_summary(dataframe, group_cols):
    return dataframe.groupby(group_cols, dropna=False).agg(
        عدد_الموظفين=('معرّف الشخص', 'count'),
        تكلفة_الشركة_شهرياً=('تكلفة الشركة الشهرية', 'sum'),
        تكلفة_الوزارة_شهرياً=('تكلفة الوزارة الشهرية', 'sum'),
        التكلفة_الإجمالية_شهرياً=('التكلفة الشهرية الإجمالية', 'sum'),
        تكلفة_الشركة_سنوياً=('تكلفة الشركة السنوية', 'sum'),
        تكلفة_الوزارة_سنوياً=('تكلفة الوزارة السنوية', 'sum'),
        التكلفة_الإجمالية_سنوياً=('التكلفة السنوية الإجمالية', 'sum'),
    ).reset_index()


def adjust_summary_count_for_selected_cost(summary_df, source_df, group_cols, selected_monthly_col):
    """تعديل عدد الموظفين في الملخصات ليعكس أصحاب التكلفة المختارة فقط."""
    temp = source_df.copy()
    temp[selected_monthly_col] = pd.to_numeric(temp[selected_monthly_col], errors='coerce').fillna(0)
    temp = temp[temp[selected_monthly_col] > 0].copy()

    if temp.empty:
        summary_df = summary_df.copy()
        summary_df['عدد_الموظفين'] = 0
        return summary_df

    selected_counts = temp.groupby(group_cols, dropna=False).agg(
        عدد_الموظفين_حسب_التكلفة=('معرّف الشخص', 'count')
    ).reset_index()

    result = summary_df.drop(columns=['عدد_الموظفين'], errors='ignore').merge(
        selected_counts,
        on=group_cols,
        how='left'
    )
    result['عدد_الموظفين'] = result['عدد_الموظفين_حسب_التكلفة'].fillna(0).astype(int)
    result = result.drop(columns=['عدد_الموظفين_حسب_التكلفة'])

    # إخفاء الصفوف التي لا يوجد فيها موظفون حسب التكلفة المختارة
    result = result[result['عدد_الموظفين'] > 0].copy()

    # ترتيب عدد الموظفين مباشرة بعد أعمدة التجميع
    metric_cols = [c for c in result.columns if c not in group_cols + ['عدد_الموظفين']]
    result = result[group_cols + ['عدد_الموظفين'] + metric_cols]

    return result


def clean_summary_view(dataframe: pd.DataFrame, display_cols: list[str]) -> pd.DataFrame:
    """عرض الأعمدة المناسبة فقط لكل مستوى ملخص للحفاظ على شكل تنفيذي نظيف."""
    existing_cols = [col for col in display_cols if col in dataframe.columns]
    return dataframe[existing_cols].copy()


def clean_admin_for_charts(dataframe: pd.DataFrame) -> pd.DataFrame:
    """إخفاء الإدارة الفارغة أو 0 من رسوم/ملخصات الإدارات فقط مع إبقائها محسوبة ضمن القطاع."""
    result = dataframe.copy()
    if 'الإدارة' not in result.columns:
        return result.iloc[0:0].copy()
    result['الإدارة'] = clean_text_value(result['الإدارة'])
    return result[
        (result['الإدارة'] != "") &
        (result['الإدارة'] != "0") &
        (result['الإدارة'].str.lower() != "nan")
    ]


def clean_general_admin_for_charts(dataframe: pd.DataFrame) -> pd.DataFrame:
    """إخفاء الإدارة العامة الفارغة أو 0 من ملخصات الإدارات العامة فقط مع إبقائها محسوبة ضمن القطاع."""
    result = dataframe.copy()

    if 'الإدارة العامة' not in result.columns:
        return result.iloc[0:0].copy()

    result['الإدارة العامة'] = clean_text_value(result['الإدارة العامة'])

    result = result[
        (result['الإدارة العامة'] != "") &
        (result['الإدارة العامة'] != "0") &
        (result['الإدارة العامة'].str.lower() != "nan")
    ]

    return result


def clean_sector_for_charts(dataframe: pd.DataFrame) -> pd.DataFrame:
    """إخفاء القطاع الفارغ أو 0 من ملخصات القطاعات فقط مع إبقائه محسوباً في الإجماليات العامة."""
    result = dataframe.copy()

    if 'القطاع' not in result.columns:
        return result.iloc[0:0].copy()

    result['القطاع'] = clean_text_value(result['القطاع'])

    result = result[
        (result['القطاع'] != "") &
        (result['القطاع'] != "0") &
        (result['القطاع'].str.lower() != "nan")
    ]

    return result


def build_drill_level(dataframe, group_col, value_col):
    """ملخص سريع لمستوى واحد في مسار التحليل المتدرج.
    عدد الموظفين هنا يتبع نوع التكلفة المختارة:
    - عند اختيار تكلفة الوزارة: يحسب فقط من لديهم تكلفة وزارة.
    - عند اختيار تكلفة الشركة: يحسب فقط من لديهم تكلفة شركة.
    - عند اختيار الإجمالي: يحسب فقط من لديهم تكلفة إجمالية.
    """
    if group_col not in dataframe.columns:
        return pd.DataFrame(columns=[group_col, 'عدد_الموظفين', 'التكلفة_الشهرية', 'متوسط_تكلفة_الموظف'])

    temp = dataframe.copy()
    temp[group_col] = clean_text_value(temp[group_col])
    temp[value_col] = pd.to_numeric(temp[value_col], errors='coerce').fillna(0)

    temp = temp[
        (temp[group_col] != "") &
        (temp[group_col] != "0") &
        (temp[group_col].str.lower() != "nan")
    ]

    if temp.empty:
        return pd.DataFrame(columns=[group_col, 'عدد_الموظفين', 'التكلفة_الشهرية', 'متوسط_تكلفة_الموظف'])

    # نستخدم عدد أصحاب التكلفة المختارة فقط حتى لا يتشوه المتوسط
    temp['_has_selected_cost'] = temp[value_col] > 0

    result = temp.groupby(group_col, dropna=False).agg(
        عدد_الموظفين=('_has_selected_cost', 'sum'),
        التكلفة_الشهرية=(value_col, 'sum')
    ).reset_index()

    result['عدد_الموظفين'] = result['عدد_الموظفين'].astype(int)

    result = result[result['عدد_الموظفين'] > 0].copy()

    result['متوسط_تكلفة_الموظف'] = (
        result['التكلفة_الشهرية'] / result['عدد_الموظفين']
    ).fillna(0)

    return result.sort_values('التكلفة_الشهرية', ascending=False)


def render_chart(fig):
    """عرض الرسم مع تطبيق خط SST Arabic وتقليل عناصر Plotly غير الضرورية."""
    fig.update_layout(
        font=dict(
            family="SST Arabic, SSTArabic, SST Arabic Roman, SST Arabic Medium, IBM Plex Sans Arabic, Tahoma, Arial, sans-serif",
            size=14
        ),
        title_font=dict(
            family="SST Arabic, SSTArabic, SST Arabic Roman, SST Arabic Medium, IBM Plex Sans Arabic, Tahoma, Arial, sans-serif",
            size=18
        ),
        legend=dict(
            font=dict(family="SST Arabic, SSTArabic, SST Arabic Roman, SST Arabic Medium, IBM Plex Sans Arabic, Tahoma, Arial, sans-serif", size=13)
        ),
        xaxis=dict(
            tickfont=dict(family="SST Arabic, SSTArabic, SST Arabic Roman, SST Arabic Medium, IBM Plex Sans Arabic, Tahoma, Arial, sans-serif", size=12),
            title_font=dict(family="SST Arabic, SSTArabic, SST Arabic Roman, SST Arabic Medium, IBM Plex Sans Arabic, Tahoma, Arial, sans-serif", size=13)
        ),
        yaxis=dict(
            tickfont=dict(family="SST Arabic, SSTArabic, SST Arabic Roman, SST Arabic Medium, IBM Plex Sans Arabic, Tahoma, Arial, sans-serif", size=12),
            title_font=dict(family="SST Arabic, SSTArabic, SST Arabic Roman, SST Arabic Medium, IBM Plex Sans Arabic, Tahoma, Arial, sans-serif", size=13)
        ),
        margin=dict(l=20, r=20, t=55, b=35),
        hovermode="x unified"
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )


def render_bar_chart(dataframe, x, y, title, text=None, y_title="القيمة", height=420, barmode=None, orientation="v"):
    """رسم أعمدة موحد بإعدادات اللوحة القياسية، ويدعم العرض العمودي أو الأفقي."""
    fig = px.bar(dataframe, x=x, y=y, text=text, title=title, barmode=barmode, orientation=orientation)
    if orientation == "h":
        fig.update_layout(xaxis_title=y_title, yaxis_title="", height=height, hovermode="y unified")
        fig.update_xaxes(tickformat=',.0f')
        fig.update_yaxes(categoryorder='total ascending', automargin=True)
        fig.update_traces(textposition='outside', cliponaxis=False)
    else:
        fig.update_layout(xaxis_title="", yaxis_title=y_title, height=height)
        fig.update_yaxes(tickformat=',.0f')
    render_chart(fig)


def render_drill_insight(dataframe, group_col, value_col):
    """خلاصة مختصرة لكل مستوى من التحليل المتدرج بدون حشو."""
    if dataframe.empty or group_col not in dataframe.columns or value_col not in dataframe.columns:
        return

    temp = dataframe.copy()
    temp[value_col] = pd.to_numeric(temp[value_col], errors='coerce').fillna(0)
    total_value = float(temp[value_col].sum())

    if total_value <= 0:
        return

    top_row = temp.sort_values(value_col, ascending=False).iloc[0]
    top_name = top_row[group_col]
    top_value = float(top_row[value_col])
    top_count = int(top_row.get('عدد_الموظفين', 0))
    top_avg = float(top_row.get('متوسط_تكلفة_الموظف', 0))
    share = (top_value / total_value * 100) if total_value else 0

    insight_label_map = {
        'الجهة': 'أعلى الجهات',
        'القطاع': 'أعلى القطاعات',
        'الإدارة العامة': 'أعلى الإدارات العامة',
        'الإدارة': 'أعلى الإدارات',
        'الموقع الفعلي': 'أعلى موقع',
    }
    insight_label = insight_label_map.get(group_col, f"أعلى {group_col}")

    if share >= 40:
        status = "🔴 تركّز عالي"
    elif share >= 25:
        status = "🟠 تركّز متوسط"
    else:
        status = "🟢 توزيع طبيعي"

    st.markdown(f"""
    <div style="
        background:#FFFFFF;
        border-right:5px solid #0C8A73;
        border-radius:12px;
        padding:11px 15px;
        margin:8px 0 14px 0;
        color:#0B3C5D;
        font-weight:700;
        direction:rtl;
        text-align:right;
        box-shadow:0 4px 12px rgba(15,23,42,0.06);
    ">
        🔎 <b>الخلاصة:</b> {insight_label}: <b>{top_name}</b> بعدد <b>{top_count}</b> موظف،
        ويمثل <b>{share:.1f}%</b> من إجمالي التكلفة الشهرية المختارة،
        بمتوسط تكلفة <b>{fmt_money(top_avg)}</b> للموظف — {status}.
    </div>
    """, unsafe_allow_html=True)


def render_drill_card(title, dataframe, group_col, value_col, chart_title, key_suffix=None, default_limit=5, expanded_limit=20):
    """عرض جدول ورسم مختصر لكل مستوى في التحليل المتدرج مع زر عرض المزيد."""
    st.markdown(f"<div class='drill-box'><div class='drill-title'>{title}</div></div>", unsafe_allow_html=True)
    if dataframe.empty:
        st.info("لا توجد بيانات لهذا المستوى حسب الفلاتر الحالية.")
        return

    render_drill_insight(dataframe, group_col, value_col)

    safe_key = key_suffix or str(group_col).replace(' ', '_')
    show_more = st.toggle("عرض المزيد", value=False, key=f"show_more_drill_{safe_key}")
    limit = expanded_limit if show_more else default_limit
    view_df = dataframe.head(limit).copy()

    render_financial_table(view_df)

    if group_col == 'الموقع الفعلي':
        location_chart_df = view_df.sort_values(value_col, ascending=True).copy()
        render_bar_chart(
            location_chart_df,
            value_col,
            group_col,
            chart_title,
            text=None,
            y_title="التكلفة الشهرية",
            height=max(360, 58 * len(location_chart_df)),
            orientation="h"
        )
    else:
        render_bar_chart(view_df, group_col, value_col, chart_title, text='عدد_الموظفين', y_title="القيمة الشهرية", height=340)


# =========================
# تحميل البيانات
# =========================
# =========================
# زر رفع ملف Excel عبر نافذة Modal
# تظهر النافذة فقط عند الضغط على زر الرفع، وليس عند تغيير الفلاتر
# =========================
if "uploaded_excel_file" not in st.session_state:
    st.session_state["uploaded_excel_file"] = None

uploaded = st.session_state.get("uploaded_excel_file")

def _upload_modal_body():
    st.markdown("### رفع ملف Excel")
    st.caption("اختر ملف البيانات بصيغة xlsx لتحديث اللوحة مؤقتاً.")
    uploaded_file = st.file_uploader(
        "اختر ملف Excel",
        type=["xlsx"],
        key="excel_uploader_modal"
    )

    if uploaded_file is not None:
        st.session_state["uploaded_excel_file"] = uploaded_file
        st.cache_data.clear()
        st.success("تم تحميل الملف بنجاح. سيتم استخدامه في اللوحة.")
        st.caption("يمكنك إغلاق النافذة من علامة × بالأعلى.")
        st.rerun()

if hasattr(st, "dialog"):
    @st.dialog("تحديث بيانات التكاليف")
    def upload_dialog():
        _upload_modal_body()

with st.sidebar:
    open_upload_modal = st.button("⬆️ رفع ملف Excel", use_container_width=True, key="open_upload_modal")

if open_upload_modal:
    if hasattr(st, "dialog"):
        upload_dialog()
    else:
        with st.expander("تحديث بيانات التكاليف", expanded=True):
            _upload_modal_body()


if uploaded is not None:
    df = load_data(uploaded)
else:
    df = load_data()

# بناء تنبيهات الاستحقاق السنوي من تاريخ التعيين لجميع أنواع الموظفين
df = build_anniversary_alerts(df)

# تحميل بيانات العمل الإضافي المستقلة
work_extra_raw_all, work_extra_long_all = load_work_extra_data()

# تحميل بيانات رحلات العمل والتذاكر المستقلة
business_trips_all = load_business_trips_data()

# =========================
# الفلاتر
# =========================
with st.sidebar:
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.25); margin:6px 0 10px 0;'>", unsafe_allow_html=True)
    st.header("خيارات التصفية")

    emp_type_values = []
    if 'نوع الموظف' in df.columns:
        emp_type_values += df['نوع الموظف'].dropna().unique().tolist()
    if isinstance(work_extra_long_all, pd.DataFrame) and not work_extra_long_all.empty:
        if 'كادر الموظف' in work_extra_long_all.columns:
            emp_type_values += work_extra_long_all['كادر الموظف'].dropna().unique().tolist()
        elif 'نوع الموظف' in work_extra_long_all.columns:
            emp_type_values += work_extra_long_all['نوع الموظف'].dropna().unique().tolist()
    if isinstance(business_trips_all, pd.DataFrame) and not business_trips_all.empty and 'نوع الموظف' in business_trips_all.columns:
        emp_type_values += business_trips_all['نوع الموظف'].dropna().unique().tolist()

    emp_types = sorted([
        v for v in {normalize_employee_type_value(x) for x in emp_type_values}
        if v and v not in ["غير محدد"]
    ])
    type_choice = st.radio("نوع الموظف / الكادر", ["الكل"] + emp_types)

    sectors = get_cascading_filter_options(df, 'القطاع')
    sector_choice = st.multiselect("القطاع", options=sectors, default=[], key="sector_choice")

    general_admins = get_cascading_filter_options(
        df, 'الإدارة العامة', {'القطاع': sector_choice}
    )
    general_admin_choice = st.multiselect(
        "الإدارة العامة",
        options=general_admins,
        default=valid_previous_choices("general_admin_choice", general_admins),
        key="general_admin_choice"
    )

    admins = get_cascading_filter_options(
        df, 'الإدارة',
        {'القطاع': sector_choice, 'الإدارة العامة': general_admin_choice}
    )
    admin_choice = st.multiselect(
        "الإدارة",
        options=admins,
        default=valid_previous_choices("admin_choice", admins),
        key="admin_choice"
    )

    location_choice = []
    if 'الموقع الفعلي' in df.columns:
        locations = get_cascading_filter_options(
            df, 'الموقع الفعلي',
            {
                'القطاع': sector_choice,
                'الإدارة العامة': general_admin_choice,
                'الإدارة': admin_choice,
            }
        )
        location_choice = st.multiselect(
            "الموقع الفعلي",
            options=locations,
            default=valid_previous_choices("location_choice", locations),
            key="location_choice"
        )
    else:
        st.caption("عمود الموقع الفعلي غير موجود في ملف البيانات.")

    view_mode = st.radio(
        "عرض التكاليف",
        ["تكلفة الشركة فقط", "تكلفة الوزارة فقط", "التكلفة الإجمالية"],
        horizontal=False
    )

    company_cost_mode = st.radio(
        "طريقة احتساب تكلفة الشركة",
        ["التكلفة الأساسية", "التكلفة الشاملة"],
        horizontal=False
    )

    st.markdown(
        "<div class='footer-signature'>by <b>Hussain Almalki</b></div>",
        unsafe_allow_html=True
    )

# =========================
# تطبيق نمط احتساب تكلفة الشركة
# =========================
df = prepare_workforce_cost_view(df, work_extra_long_all, business_trips_all, company_cost_mode)


# =========================
# تطبيق الفلاتر عبر المحرك الموحد
# =========================
filtered = apply_global_filters(df, employee_type_columns=('نوع الموظف',))

if filtered.empty:
    st.warning("لا توجد بيانات مطابقة للفلاتر المختارة.")
    st.stop()

# =========================
# خرائط العرض
# =========================
monthly_map = {
    "تكلفة الشركة فقط": "تكلفة الشركة الشهرية",
    "تكلفة الوزارة فقط": "تكلفة الوزارة الشهرية",
    "التكلفة الإجمالية": "التكلفة الشهرية الإجمالية",
}

annual_map = {
    "تكلفة الشركة فقط": "تكلفة الشركة السنوية",
    "تكلفة الوزارة فقط": "تكلفة الوزارة السنوية",
    "التكلفة الإجمالية": "التكلفة السنوية الإجمالية",
}

monthly_summary_map = {
    "تكلفة الشركة فقط": "تكلفة_الشركة_شهرياً",
    "تكلفة الوزارة فقط": "تكلفة_الوزارة_شهرياً",
    "التكلفة الإجمالية": "التكلفة_الإجمالية_شهرياً",
}

annual_summary_map = {
    "تكلفة الشركة فقط": "تكلفة_الشركة_سنوياً",
    "تكلفة الوزارة فقط": "تكلفة_الوزارة_سنوياً",
    "التكلفة الإجمالية": "التكلفة_الإجمالية_سنوياً",
}

monthly_col = monthly_map[view_mode]
annual_col = annual_map[view_mode]
monthly_summary_col = monthly_summary_map[view_mode]
annual_summary_col = annual_summary_map[view_mode]

# أعمدة عرض ديناميكية تتغير حسب اختيار "عرض التكاليف"
display_monthly_label = "القيمة الشهرية المختارة"
display_annual_label = "القيمة السنوية المختارة"
df[display_monthly_label] = df[monthly_col]
df[display_annual_label] = df[annual_col]
filtered[display_monthly_label] = filtered[monthly_col]
filtered[display_annual_label] = filtered[annual_col]

# =========================
# مؤشرات رئيسية
# =========================
total_emp = int(filtered['معرّف الشخص'].count())
company_month = float(filtered['تكلفة الشركة الشهرية'].sum())
mewa_month = float(filtered['تكلفة الوزارة الشهرية'].sum())
total_month = float(filtered['التكلفة الشهرية الإجمالية'].sum())
company_year = float(filtered['تكلفة الشركة السنوية'].sum())
mewa_year = float(filtered['تكلفة الوزارة السنوية'].sum())
total_year = float(filtered['التكلفة السنوية الإجمالية'].sum())

# =========================
# مؤشرات رئيسية (KPI)
# =========================

# الصف الأول: الشركة
row1 = st.columns([1, 1.5, 1.5, 1.5, 1], gap="medium")

row1_metrics = [
    ("عدد الموظفين", fmt_int(total_emp), "metric-card"),
    ("تكلفة الشركة شهرياً", fmt_money(company_month), "metric-card"),
    ("تكلفة الشركة سنوياً", fmt_money(company_year), "metric-card"),
]

for col, (label, value, cls) in zip(row1[1:4], row1_metrics):
    col.markdown(f"""
    <div class='{cls}'>
        <div class='metric-label'>{label}</div>
        <div class='metric-value'>{value}</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# الصف الثاني: الوزارة + الإجمالي
row2 = st.columns(4, gap="medium")

row2_metrics = [
    ("تكلفة الوزارة شهرياً", fmt_money(mewa_month), "metric-card light"),
    ("تكلفة الوزارة سنوياً", fmt_money(mewa_year), "metric-card light"),
    ("إجمالي التكلفة الشهرية", fmt_money(total_month), "metric-card total"),
    ("إجمالي التكلفة السنوية", fmt_money(total_year), "metric-card total"),
]

for col, (label, value, cls) in zip(row2, row2_metrics):
    col.markdown(f"""
    <div class='{cls}'>
        <div class='metric-label'>{label}</div>
        <div class='metric-value'>{value}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# وصف وضع العرض الحالي
# =========================
if type_choice == "الكل":
    st.markdown(f"**عرض البيانات الحالي:** {view_mode}")
else:
    st.markdown(f"**عرض البيانات الحالي:** {view_mode} — **نوع الموظف المختار:** {type_choice}")

# =========================
# مسار التحليل المتدرج
# =========================
path_items = []
if sector_choice:
    path_items.append("القطاع: " + "، ".join(sector_choice))
else:
    path_items.append("كل القطاعات")

if general_admin_choice:
    path_items.append("الإدارة العامة: " + "، ".join(general_admin_choice))
else:
    path_items.append("كل الإدارات العامة")

if admin_choice:
    path_items.append("الإدارة: " + "، ".join(admin_choice))
else:
    path_items.append("كل الإدارات")

if location_choice:
    path_items.append("الموقع الفعلي: " + "، ".join(location_choice))
else:
    path_items.append("كل المواقع الفعلية")

if type_choice != "الكل":
    path_items.append("نوع الموظف: " + type_choice)


# =========================
# لوحة مختصرة خاصة بنوع الموظف المختار
# =========================
if type_choice != "الكل":
    st.markdown(f"## تحليل نوع الموظف: {type_choice}")

    selected_count = int(filtered['معرّف الشخص'].count())
    selected_company_month = float(filtered['تكلفة الشركة الشهرية'].sum())
    selected_mewa_month = float(filtered['تكلفة الوزارة الشهرية'].sum())
    selected_total_month = float(filtered['التكلفة الشهرية الإجمالية'].sum())

    selected_cols = st.columns(4)
    selected_metrics = [
        (f"عدد {type_choice}", fmt_int(selected_count)),
        ("تكلفة الشركة شهرياً", fmt_money(selected_company_month)),
        ("تكلفة الوزارة شهرياً", fmt_money(selected_mewa_month)),
        ("إجمالي التكلفة شهرياً", fmt_money(selected_total_month)),
    ]

    for col, (label, value) in zip(selected_cols, selected_metrics):
        col.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-label'>{label}</div>
                <div class='metric-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================
# ملخصات
# =========================
sector_summary_df = clean_sector_for_charts(filtered)
sector_summary = build_summary(sector_summary_df, ['القطاع'])
sector_summary = adjust_summary_count_for_selected_cost(
    sector_summary, sector_summary_df, ['القطاع'], monthly_col
).sort_values(monthly_summary_col, ascending=False)

general_admin_summary_df = clean_general_admin_for_charts(filtered)
general_admin_summary = build_summary(general_admin_summary_df, ['القطاع', 'الإدارة العامة'])
general_admin_summary = adjust_summary_count_for_selected_cost(
    general_admin_summary, general_admin_summary_df, ['القطاع', 'الإدارة العامة'], monthly_col
).sort_values(monthly_summary_col, ascending=False)

admin_summary_df = clean_admin_for_charts(filtered)
admin_summary = build_summary(admin_summary_df, ['القطاع', 'الإدارة العامة', 'الإدارة'])
admin_summary = adjust_summary_count_for_selected_cost(
    admin_summary, admin_summary_df, ['القطاع', 'الإدارة العامة', 'الإدارة'], monthly_col
).sort_values(monthly_summary_col, ascending=False)

# أعمدة عرض مختصرة ونظيفة لكل مستوى من الملخصات
summary_metric_cols = [
    'عدد_الموظفين',
    'تكلفة_الشركة_شهرياً',
    'تكلفة_الوزارة_شهرياً',
    'التكلفة_الإجمالية_شهرياً',
    'تكلفة_الشركة_سنوياً',
    'تكلفة_الوزارة_سنوياً',
    'التكلفة_الإجمالية_سنوياً'
]

sector_summary_view = clean_summary_view(
    sector_summary,
    ['القطاع'] + summary_metric_cols
)

general_admin_summary_view = clean_summary_view(
    general_admin_summary,
    ['الإدارة العامة'] + summary_metric_cols
)

admin_summary_view = clean_summary_view(
    admin_summary,
    ['الإدارة'] + summary_metric_cols
)

if 'الموقع الفعلي' in filtered.columns:
    location_group_cols = ['الموقع الفعلي']
    if 'الإدارة العامة' in filtered.columns:
        location_group_cols.append('الإدارة العامة')
    if 'الإدارة' in filtered.columns:
        location_group_cols.append('الإدارة')

    location_summary = build_summary(filtered, location_group_cols)
    location_summary = adjust_summary_count_for_selected_cost(
        location_summary, filtered, location_group_cols, monthly_col
    ).sort_values(monthly_summary_col, ascending=False)
else:
    location_summary = pd.DataFrame()

location_summary_view = clean_summary_view(
    location_summary,
    ['الموقع الفعلي', 'الإدارة العامة', 'الإدارة'] + summary_metric_cols
)

type_summary = filtered.groupby(['نوع الموظف'], dropna=False).agg(
    عدد_الموظفين=('معرّف الشخص', 'count'),
    قيمة_شهرية=(monthly_col, 'sum'),
    قيمة_سنوية=(annual_col, 'sum'),
).reset_index()

# تجهيز مستويات التحليل المتدرج حسب الفلاتر الحالية
drill_unit_source = filtered.copy()
drill_unit_source['الجهة'] = build_org_unit(drill_unit_source)
drill_unit_source = drill_unit_source[drill_unit_source['الجهة'] != 'غير محدد'].copy()
drill_unit_df = build_drill_level(drill_unit_source, 'الجهة', monthly_col)
drill_sector_df = build_drill_level(clean_sector_for_charts(filtered), 'القطاع', monthly_col)
drill_general_admin_df = build_drill_level(filtered, 'الإدارة العامة', monthly_col)
drill_admin_df = build_drill_level(filtered, 'الإدارة', monthly_col)
drill_location_df = build_drill_level(filtered, 'الموقع الفعلي', monthly_col)
drill_employee_df = filtered.copy().sort_values(monthly_col, ascending=False)


# =========================
# تجهيز تحليلات الأعمار
# =========================
# البحث الذكي عن عمود العمر
age_col = next((c for c in AGE_COLUMNS if c in filtered.columns), None)

if age_col:
    filtered['العمر'] = pd.to_numeric(filtered[age_col], errors='coerce')

    filtered['الفئة العمرية'] = pd.cut(
        filtered['العمر'],
        bins=[0, 24, 30, 40, 50, 100],
        labels=['أقل من 25', '25-30', '31-40', '41-50', '50+']
    )

    avg_age = round(filtered['العمر'].mean(), 1)
    min_age = int(filtered['العمر'].min()) if filtered['العمر'].notna().any() else 0
    max_age = int(filtered['العمر'].max()) if filtered['العمر'].notna().any() else 0

    age_group_summary = filtered.groupby('الفئة العمرية', dropna=False).agg(
        عدد_الموظفين=('معرّف الشخص', 'count'),
        متوسط_التكلفة=(monthly_col, 'mean')
    ).reset_index()
else:
    avg_age = 0
    min_age = 0
    max_age = 0
    age_group_summary = pd.DataFrame()


# =========================
# التبويبات
# =========================
executive_tab, workforce_tab, employee_details_tab, alerts_tab, work_extra_tab, trips_tab = st.tabs([
    "الملخص التنفيذي",
    "تحليل القوى العاملة والتكلفة",
    "تفاصيل الموظفين",
    "مؤشرات العقود والإعارة",
    "العمل الإضافي",
    "رحلات العمل"
])

with executive_tab:
    st.subheader("الملخص التنفيذي")

    # مؤشرات تنفيذية مختصرة من نفس مصادر البيانات الحالية، دون تغيير أي منطق حسابي.
    executive_work_extra_df = apply_work_extra_filters(work_extra_long_all) if 'work_extra_long_all' in globals() else pd.DataFrame()
    executive_trips_df = apply_business_trip_global_filters(business_trips_all) if 'business_trips_all' in globals() else pd.DataFrame()

    work_extra_total = 0.0
    if executive_work_extra_df is not None and not executive_work_extra_df.empty and 'مبلغ العمل الإضافي' in executive_work_extra_df.columns:
        work_extra_total = float(pd.to_numeric(executive_work_extra_df['مبلغ العمل الإضافي'], errors='coerce').fillna(0).sum())

    trips_total = 0.0
    if executive_trips_df is not None and not executive_trips_df.empty and 'إجمالي تكلفة الرحلة' in executive_trips_df.columns:
        trips_total = float(pd.to_numeric(executive_trips_df['إجمالي تكلفة الرحلة'], errors='coerce').fillna(0).sum())

    variable_cost_total = work_extra_total + trips_total
    avg_cost_per_employee = float(filtered[monthly_col].sum() / total_emp) if total_emp else 0.0
    general_admin_count = int(clean_text_value(filtered['الإدارة العامة']).replace('', pd.NA).dropna().nunique()) if 'الإدارة العامة' in filtered.columns else 0
    location_count = int(clean_text_value(filtered['الموقع الفعلي']).replace('', pd.NA).dropna().nunique()) if 'الموقع الفعلي' in filtered.columns else 0

    # المؤشرات العليا تعرض بالفعل عدد الموظفين والتكاليف الأساسية؛
    # لذلك يعرض الملخص التنفيذي مؤشرات مكملة فقط لتجنب تكرار نفس الأرقام.
    sector_count_exec = int(clean_sector_for_charts(filtered)['القطاع'].nunique()) if 'القطاع' in filtered.columns else 0
    admin_count_exec = int(clean_text_value(filtered['الإدارة']).replace('', pd.NA).dropna().nunique()) if 'الإدارة' in filtered.columns else 0

    exec_rows = [
        [
            ("عدد القطاعات", fmt_int(sector_count_exec)),
            ("عدد الإدارات العامة", fmt_int(general_admin_count)),
            ("عدد الإدارات", fmt_int(admin_count_exec)),
            ("عدد المواقع التشغيلية", fmt_int(location_count)),
        ],
        [
            ("متوسط تكلفة الموظف", fmt_money(avg_cost_per_employee)),
            ("العمل الإضافي", fmt_money(work_extra_total)),
            ("رحلات العمل", fmt_money(trips_total)),
            ("إجمالي التكاليف المتغيرة", fmt_money(variable_cost_total)),
        ],
    ]

    for metrics_row in exec_rows:
        exec_cols = st.columns(4)
        for col, (label, value) in zip(exec_cols, metrics_row):
            col.markdown(
                f"""
                <div class='smart-card' style='min-height:110px; text-align:center; padding:16px 12px;'>
                    <div class='smart-card-title'>{label}</div>
                    <div class='smart-card-value' style='font-size:24px;'>{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    chart_col_a, chart_col_b = st.columns(2)
    with chart_col_a:
        if not sector_summary.empty:
            render_bar_chart(sector_summary.head(8), 'القطاع', monthly_summary_col, 'توزيع التكلفة حسب القطاع', text='عدد_الموظفين', height=390)
        else:
            st.info("لا توجد بيانات كافية لعرض توزيع التكلفة حسب القطاع.")

    with chart_col_b:
        if not type_summary.empty:
            fig_exec_type = px.pie(
                type_summary,
                names='نوع الموظف',
                values='عدد_الموظفين',
                title='تحليل القوى العاملة حسب النوع'
            )
            fig_exec_type.update_layout(height=390)
            fig_exec_type.update_traces(textinfo='label+percent+value')
            render_chart(fig_exec_type)
        else:
            st.info("لا توجد بيانات كافية لعرض تحليل القوى العاملة حسب النوع.")

    chart_col_c, chart_col_d = st.columns(2)
    with chart_col_c:
        if not general_admin_summary.empty:
            render_bar_chart(general_admin_summary.head(5), 'الإدارة العامة', monthly_summary_col, 'أعلى 5 إدارات عامة تكلفة', text='عدد_الموظفين', height=390)
        else:
            st.info("لا توجد بيانات كافية لعرض أعلى الإدارات العامة تكلفة.")

    with chart_col_d:
        if not location_summary.empty and 'الموقع الفعلي' in location_summary.columns:
            location_exec = location_summary.groupby('الموقع الفعلي', dropna=False).agg(
                عدد_الموظفين=('عدد_الموظفين', 'sum')
            ).reset_index().sort_values('عدد_الموظفين', ascending=False).head(8)
            render_bar_chart(location_exec, 'الموقع الفعلي', 'عدد_الموظفين', 'توزيع الموظفين حسب الموقع', text='عدد_الموظفين', y_title='عدد الموظفين', height=390)
        else:
            st.info("لا توجد بيانات كافية لعرض توزيع الموظفين حسب الموقع.")

    st.markdown("### ملخص التكاليف المتغيرة")
    variable_summary = pd.DataFrame([
        {'البند': 'العمل الإضافي', 'القيمة': work_extra_total},
        {'البند': 'رحلات العمل', 'القيمة': trips_total},
        {'البند': 'الإجمالي', 'القيمة': variable_cost_total},
    ])
    render_financial_table(variable_summary)

with workforce_tab:

    drill_kpi_cols = st.columns(5)
    sector_count = clean_sector_for_charts(filtered)['القطاع'].nunique() if 'القطاع' in filtered.columns else 0
    drill_kpi_cols[0].metric("عدد القطاعات", fmt_int(sector_count))
    drill_kpi_cols[1].metric("عدد الإدارات العامة", fmt_int(drill_general_admin_df['الإدارة العامة'].nunique() if not drill_general_admin_df.empty else 0))
    drill_kpi_cols[2].metric("عدد الإدارات", fmt_int(drill_admin_df['الإدارة'].nunique() if not drill_admin_df.empty else 0))
    drill_kpi_cols[3].metric("عدد المواقع الفعلية", fmt_int(drill_location_df['الموقع الفعلي'].nunique() if not drill_location_df.empty else 0))
    drill_kpi_cols[4].metric("عدد الموظفين", fmt_int(total_emp))

    st.markdown("### التحليل التنظيمي والتكلفة")

    show_employee_level = False

    # التحليل المتدرج: نعرض المستوى التالي فقط لتجنب تكرار نفس التحليل عبر عدة رسوم
    if not sector_choice and not general_admin_choice and not admin_choice and not location_choice:
        st.markdown("#### الجهات حسب التكلفة")
        render_drill_card(
            "الجهات حسب التكلفة الشهرية المختارة",
            drill_unit_df,
            'الجهة',
            'التكلفة_الشهرية',
            "أعلى الجهات حسب التكلفة الشهرية",
            key_suffix="unit_overview"
        )

    elif sector_choice and not general_admin_choice and not admin_choice and not location_choice:
        st.markdown("#### الإدارات العامة التابعة للقطاع المختار")
        render_drill_card(
            "الإدارات العامة التابعة للقطاع المختار",
            drill_general_admin_df,
            'الإدارة العامة',
            'التكلفة_الشهرية',
            "الإدارات العامة حسب التكلفة الشهرية",
            key_suffix="general_admin_after_sector"
        )

    elif general_admin_choice and not admin_choice and not location_choice:
        st.markdown("#### الإدارات التابعة للإدارة العامة المختارة")
        render_drill_card(
            "الإدارات التابعة للإدارة العامة المختارة",
            drill_admin_df,
            'الإدارة',
            'التكلفة_الشهرية',
            "الإدارات حسب التكلفة الشهرية",
            key_suffix="admin_after_general_admin"
        )

    elif admin_choice and not location_choice:
        st.markdown("#### المواقع الفعلية التابعة للإدارة المختارة")
        render_drill_card(
            "المواقع الفعلية حسب الإدارة المختارة",
            drill_location_df,
            'الموقع الفعلي',
            'التكلفة_الشهرية',
            "المواقع الفعلية حسب التكلفة الشهرية",
            key_suffix="location_after_admin"
        )

    elif location_choice:
        st.markdown("#### الموظفون في الموقع الفعلي المختار")
        show_employee_level = True

    if show_employee_level:
        employee_drill_cols = [
            'معرّف الشخص', 'القطاع', 'الإدارة العامة', 'الإدارة', 'نوع الموظف',
            'الدرجة الوظيفية', 'مكان العمل', 'الموقع الفعلي',
            display_monthly_label, display_annual_label
        ]

        employee_drill_cols = list(dict.fromkeys(employee_drill_cols))
        drill_employee_display = drill_employee_df.loc[:, ~drill_employee_df.columns.duplicated()].copy()
        employee_drill_cols = [c for c in employee_drill_cols if c in drill_employee_display.columns]

        st.dataframe(
            format_financial_dataframe(drill_employee_display[employee_drill_cols].head(100)),
            use_container_width=True,
            hide_index=True
        )

    st.download_button(
        "تحميل نتائج التحليل CSV",
        drill_employee_df.to_csv(index=False).encode("utf-8-sig"),
        "drill_down_results.csv",
        "text/csv"
    )

with workforce_tab:
    st.markdown("---")
    st.subheader("الملخصات التنظيمية")

    org_tabs = st.tabs(["القطاع", "الإدارة العامة", "الإدارة", "الموقع الفعلي"])
    org_summaries = [
        (org_tabs[0], sector_summary_view, "تحميل ملخص القطاعات CSV", "sector_summary.csv"),
        (org_tabs[1], general_admin_summary_view, "تحميل ملخص الإدارات العامة CSV", "general_admin_summary.csv"),
        (org_tabs[2], admin_summary_view, "تحميل ملخص الإدارات CSV", "admin_summary.csv"),
        (org_tabs[3], location_summary_view, "تحميل ملخص المواقع الفعلية CSV", "location_summary.csv"),
    ]

    for idx, (org_tab, summary_df, download_label, download_name) in enumerate(org_summaries):
        with org_tab:
            # الموقع الفعلي يحتفظ بتحليل تكلفة واحد فقط، لتجنب تكراره في بقية التبويب.
            if idx == 3 and not location_summary.empty and 'الموقع الفعلي' in location_summary.columns:
                location_cost_chart = (
                    location_summary.groupby('الموقع الفعلي', dropna=False)
                    .agg(التكلفة_الشهرية=(monthly_summary_col, 'sum'))
                    .reset_index()
                    .sort_values('التكلفة_الشهرية', ascending=False)
                    .head(10)
                )
                fig_location_cost = px.bar(
                    location_cost_chart.sort_values('التكلفة_الشهرية'),
                    x='التكلفة_الشهرية',
                    y='الموقع الفعلي',
                    orientation='h',
                    text='التكلفة_الشهرية',
                    title='أعلى المواقع الفعلية حسب التكلفة الشهرية'
                )
                fig_location_cost.update_layout(xaxis_title='التكلفة الشهرية', yaxis_title='', height=max(380, 42 * len(location_cost_chart) + 120))
                fig_location_cost.update_xaxes(tickformat=',.0f')
                fig_location_cost.update_traces(texttemplate='%{text:,.0f}', textposition='outside', cliponaxis=False)
                render_chart(fig_location_cost)

            render_financial_table(summary_df)
            st.download_button(
                download_label,
                summary_df.to_csv(index=False).encode("utf-8-sig"),
                download_name,
                "text/csv",
                key=f"download_{download_name}"
            )


with employee_details_tab:
    st.subheader("تفاصيل الموظفين بعد التصفية")
    display_cols = [
        'معرّف الشخص', 'القطاع', 'الإدارة العامة', 'الإدارة', 'نوع الموظف',
        'الدرجة الوظيفية', 'مكان العمل', 'الموقع الفعلي',
        'العمر',
        'تاريخ التعيين', 'تاريخ الاستحقاق القادم', 'الأيام المتبقية', 'مؤشر الاستحقاق',
        display_monthly_label, display_annual_label
    ]
    display_cols = [c for c in display_cols if c in filtered.columns]

    # الفرز بناءً على اختيار عرض التكاليف الحالي
    details_display = filtered.sort_values(monthly_col, ascending=False)[display_cols].copy()

    st.dataframe(
        format_financial_dataframe(details_display),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "تحميل البيانات المفلترة CSV",
        filtered.to_csv(index=False).encode("utf-8-sig"),
        "filtered_employee_costs.csv",
        "text/csv"
    )

with alerts_tab:
    st.subheader("مؤشرات العقود والإعارة")

    # الشاشة تعرض فقط الاستحقاقات القادمة التي تحتاج متابعة (70 يوماً فأقل).
    # الحالات التي تمت معالجتها أو مضى استحقاقها تحفظ في السجل السابق.
    alerts_df = filtered.copy()
    today_ts = pd.Timestamp(datetime.now().date()).normalize()

    # إعادة تسمية الحالات لتكون تشغيلية بدلاً من وصفها بالحرجة/المستقرة.
    def _operational_status(days):
        if pd.isna(days):
            return ""
        days = int(days)
        if days > 85:
            # تستمر الحسبة، لكن بدون تصنيف حتى يدخل الاستحقاق نطاق المتابعة.
            return ""
        if 80 <= days <= 85:
            return "قريب الاستحقاق"
        if 0 <= days <= 79:
            return "يتطلب إجراء"
        return ""

    alerts_df["حالة المتابعة"] = alerts_df["الأيام المتبقية"].apply(_operational_status)
    alerts_df["مؤشر المتابعة"] = alerts_df["حالة المتابعة"].map({
        "يتطلب إجراء": "🔴 يتطلب إجراء",
        "قريب الاستحقاق": "🟠 قريب الاستحقاق",
    }).fillna("")

    alerts_status_data = load_alerts_status()
    alerts_df["_alert_key"] = alerts_df.apply(build_alert_key, axis=1)
    alerts_df["تمت المعالجة"] = alerts_df["_alert_key"].isin(alerts_status_data.keys())
    alerts_df["إجراء المعالجة"] = alerts_df["_alert_key"].map(
        lambda key: alerts_status_data.get(key, {}).get("status", "")
        if isinstance(alerts_status_data.get(key, {}), dict) else ""
    )
    alerts_df["تاريخ المعالجة"] = alerts_df["_alert_key"].map(
        lambda key: alerts_status_data.get(key, {}).get("updated_at", "")
        if isinstance(alerts_status_data.get(key, {}), dict) else ""
    )

    # نطاق المتابعة النشط يبدأ عند 85 يوماً ويستمر حتى تاريخ الاستحقاق.
    current_mask = (
        alerts_df["الأيام المتبقية"].notna()
        & alerts_df["الأيام المتبقية"].between(0, 85, inclusive="both")
        & (~alerts_df["تمت المعالجة"])
    )
    current_alerts_df = alerts_df[current_mask].copy()

    # العقود: نعرض جميع الاستحقاقات القادمة من تاريخ اليوم.
    # إذا كان الاستحقاق أبعد من 70 يوماً يبقى بلا تصنيف حتى يدخل نطاق المتابعة.
    employee_type_series = alerts_df["نوع الموظف"].apply(normalize_employee_type_value)
    all_upcoming_mask = (
        alerts_df["الأيام المتبقية"].notna()
        & alerts_df["الأيام المتبقية"].ge(0)
        & (~alerts_df["تمت المعالجة"])
        & (~employee_type_series.eq("إعارة"))
    )
    contracts_df = alerts_df[all_upcoming_mask].copy()

    # الإعارة تظهر ضمن نطاق المتابعة حتى 85 يوماً.
    current_type_series = current_alerts_df["نوع الموظف"].apply(normalize_employee_type_value)
    secondment_df = current_alerts_df[current_type_series.eq("إعارة")].copy()

    # السجل السابق = الحالات المعالجة + الاستحقاقات السنوية التي مضت خلال السنة الحالية.
    processed_history_df = alerts_df[alerts_df["تمت المعالجة"]].copy()
    if not processed_history_df.empty:
        processed_history_df["نوع السجل"] = "مكتمل"

    past_history_df = alerts_df[~alerts_df["تمت المعالجة"]].copy()
    if "تاريخ التعيين" in past_history_df.columns:
        hire_dates = pd.to_datetime(past_history_df["تاريخ التعيين"], errors="coerce")
        previous_dates = hire_dates.apply(lambda x: _safe_anniversary_date(x, today_ts.year))
        passed_mask = previous_dates.notna() & (previous_dates < today_ts)
        past_history_df = past_history_df[passed_mask].copy()
        past_history_df["تاريخ الاستحقاق السابق"] = previous_dates.loc[passed_mask].dt.strftime("%Y-%m-%d")
        past_history_df["نوع السجل"] = "استحقاق سابق"
    else:
        past_history_df = pd.DataFrame()

    history_df = pd.concat([processed_history_df, past_history_df], ignore_index=True, sort=False)
    if not history_df.empty:
        history_df = history_df.drop_duplicates(subset=["معرّف الشخص", "نوع السجل"], keep="last")

    def _render_followup_section(section_df, section_key, section_title):
        st.markdown(f"### {section_title}")

        action_required = section_df[section_df["حالة المتابعة"].eq("يتطلب إجراء")].copy()
        upcoming = section_df[section_df["حالة المتابعة"].eq("قريب الاستحقاق")].copy()
        nearest_days = section_df["الأيام المتبقية"].dropna().min() if not section_df.empty else pd.NA
        nearest_display = "-" if pd.isna(nearest_days) else f"{int(nearest_days)} يوم"

        metric_cols = st.columns(3)
        metrics = [
            ("يتطلب إجراء", fmt_int(len(action_required)), "alert-card red"),
            ("قريب الاستحقاق", fmt_int(len(upcoming)), "alert-card orange"),
            ("أقرب استحقاق", nearest_display, "alert-card blue"),
        ]
        for col, (label, value, cls) in zip(metric_cols, metrics):
            col.markdown(
                f"""<div class='{cls}'>
                    <div class='alert-card-title'>{label}</div>
                    <div class='alert-card-value'>{value}</div>
                </div>""",
                unsafe_allow_html=True
            )

        if section_df.empty:
            if section_key == "contracts":
                st.info("لا توجد عقود قادمة حسب الفلاتر الحالية.")
            else:
                st.info("لا توجد استحقاقات إعارة ضمن نطاق المتابعة حتى 85 يوماً حسب الفلاتر الحالية.")
            return

        section_df = section_df.copy()
        section_df["_ترتيب_المتابعة"] = section_df["حالة المتابعة"].map(
            {"يتطلب إجراء": 1, "قريب الاستحقاق": 2}
        ).fillna(3)
        section_df = section_df.sort_values(
            ["_ترتيب_المتابعة", "الأيام المتبقية"], ascending=[True, True]
        )

        display_cols = [
            "معرّف الشخص", "نوع الموظف", "الإدارة العامة", "الإدارة",
            "الموقع الفعلي", "تاريخ الاستحقاق القادم", "الأيام المتبقية",
            "مؤشر المتابعة"
        ]
        display_cols = [c for c in display_cols if c in section_df.columns]

        select_all = st.checkbox(
            "تحديد الكل للمعروض",
            value=False,
            key=f"select_all_{section_key}"
        )
        editor_df = section_df[display_cols + ["_alert_key"]].copy()
        editor_df.insert(0, "تحديد", bool(select_all))
        editor_df = format_financial_dataframe(editor_df)

        edited_df = st.data_editor(
            editor_df,
            use_container_width=True,
            hide_index=True,
            disabled=[c for c in editor_df.columns if c != "تحديد"],
            column_config={
                "_alert_key": None,
                "تحديد": st.column_config.CheckboxColumn(
                    "تحديد", help="حدد الحالات ثم سجل الإجراء"
                )
            },
            key=f"{section_key}_editor"
        )

        selected_keys = edited_df.loc[
            edited_df["تحديد"].eq(True), "_alert_key"
        ].dropna().astype(str).tolist()

        action_cols = st.columns([1, 1, 4])
        with action_cols[0]:
            if st.button(
                "تم التجديد",
                use_container_width=True,
                disabled=not selected_keys,
                key=f"renew_{section_key}"
            ):
                current_status = load_alerts_status()
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for key_value in selected_keys:
                    current_status[key_value] = {
                        "status": "تم التجديد",
                        "updated_at": now_str
                    }
                save_alerts_status(current_status)
                st.success("تم تسجيل الحالات المحددة كـ تم التجديد.")
                st.rerun()

        with action_cols[1]:
            if st.button(
                "تم الإنهاء",
                use_container_width=True,
                disabled=not selected_keys,
                key=f"end_{section_key}"
            ):
                current_status = load_alerts_status()
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for key_value in selected_keys:
                    current_status[key_value] = {
                        "status": "تم الإنهاء",
                        "updated_at": now_str
                    }
                save_alerts_status(current_status)
                st.success("تم تسجيل الحالات المحددة كـ تم الإنهاء.")
                st.rerun()

        export_df = section_df[display_cols].copy()
        st.download_button(
            "تحميل Excel",
            data=dataframe_to_excel_bytes(export_df, sheet_name=section_title[:31]),
            file_name=f"{section_key}_followup.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"download_{section_key}"
        )

    contracts_tab, secondment_tab, history_tab = st.tabs([
        "العقود", "الإعارة", "السجل السابق"
    ])

    with contracts_tab:
        _render_followup_section(contracts_df, "contracts", "العقود")

    with secondment_tab:
        _render_followup_section(secondment_df, "secondment", "الإعارة")

    with history_tab:
        st.markdown("### السجل السابق")

        if history_df.empty:
            st.info("لا توجد حالات سابقة أو مكتملة حسب الفلاتر الحالية.")
        else:
            history_df = history_df.copy()
            history_df["نوع الاستحقاق"] = history_df["نوع الموظف"].apply(
                lambda x: "إعارة" if normalize_employee_type_value(x) == "إعارة" else "عقد"
            )

            history_type = st.radio(
                "نوع الاستحقاق",
                ["الكل", "عقد", "إعارة"],
                horizontal=True,
                key="history_type_filter"
            )
            if history_type != "الكل":
                history_df = history_df[history_df["نوع الاستحقاق"].eq(history_type)]

            history_display_cols = [
                "معرّف الشخص", "نوع الاستحقاق", "نوع الموظف",
                "الإدارة العامة", "الإدارة", "الموقع الفعلي",
                "تاريخ الاستحقاق السابق", "تاريخ الاستحقاق القادم",
                "نوع السجل", "إجراء المعالجة", "تاريخ المعالجة"
            ]
            history_display_cols = [c for c in history_display_cols if c in history_df.columns]

            render_financial_table(history_df[history_display_cols])

            processed_only = history_df[history_df["تمت المعالجة"].fillna(False)].copy()
            if not processed_only.empty:
                cancel_df = processed_only[history_display_cols + ["_alert_key"]].copy()
                cancel_df.insert(0, "إلغاء الإجراء", False)
                cancel_df = format_financial_dataframe(cancel_df)

                edited_history = st.data_editor(
                    cancel_df,
                    use_container_width=True,
                    hide_index=True,
                    disabled=[c for c in cancel_df.columns if c != "إلغاء الإجراء"],
                    column_config={
                        "_alert_key": None,
                        "إلغاء الإجراء": st.column_config.CheckboxColumn(
                            "إلغاء الإجراء",
                            help="إعادة الحالة المكتملة إلى المتابعة عند الحاجة"
                        )
                    },
                    key="history_cancel_editor"
                )
                cancel_keys = edited_history.loc[
                    edited_history["إلغاء الإجراء"].eq(True), "_alert_key"
                ].dropna().astype(str).tolist()

                if st.button(
                    "↩ إلغاء الإجراء",
                    disabled=not cancel_keys,
                    key="cancel_history_actions"
                ):
                    current_status = load_alerts_status()
                    for key_value in cancel_keys:
                        current_status.pop(key_value, None)
                    save_alerts_status(current_status)
                    st.success("تم إلغاء الإجراء للحالات المحددة.")
                    st.rerun()

            st.download_button(
                "تحميل السجل السابق Excel",
                data=dataframe_to_excel_bytes(history_df[history_display_cols], sheet_name="السجل السابق"),
                file_name="contracts_secondment_history.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_contracts_secondment_history"
            )


with workforce_tab:
    st.markdown("---")
    st.subheader("تحليل الهيكل والقوى العاملة")

    mix_df = filtered.copy()

    # حل الجهة: يمنع ظهور صفوف أو أعمدة فارغة في الجداول والرسوم
    mix_df['الجهة'] = build_org_unit(mix_df)

    # لا نعرض غير محدد في تحليل القوى العاملة حتى لا تظهر أعمدة/صفوف فارغة
    mix_df = mix_df[mix_df['الجهة'] != 'غير محدد'].copy()

    # توحيد نص نوع الموظف لضمان احتساب المعارين بشكل صحيح
    mix_df['نوع الموظف'] = clean_text_value(mix_df['نوع الموظف'])

    mix_summary = mix_df.groupby(['الجهة', 'نوع الموظف'], dropna=False).agg(
        عدد_الموظفين=('معرّف الشخص', 'count'),
        القيمة_الشهرية_المختارة=(monthly_col, 'sum'),
        تكلفة_الشركة_شهرياً=('تكلفة الشركة الشهرية', 'sum'),
        تكلفة_الوزارة_شهرياً=('تكلفة الوزارة الشهرية', 'sum'),
        التكلفة_الإجمالية_شهرياً=('التكلفة الشهرية الإجمالية', 'sum'),
    ).reset_index()

    if mix_summary.empty:
        st.info("لا توجد بيانات كافية لعرض تحليل القوى العاملة.")
    else:
        total_workforce = int(mix_df['معرّف الشخص'].count())

        assignees_only = mix_df[mix_df['نوع الموظف'].isin(['إعارة', 'معار'])].copy()
        employees_only = mix_df[mix_df['نوع الموظف'].eq('موظف')].copy()
        temporary_only = mix_df[mix_df['نوع الموظف'].astype(str).str.contains('عقد', na=False)].copy()

        total_assignees = int(assignees_only['معرّف الشخص'].count())
        total_employees = int(employees_only['معرّف الشخص'].count())
        total_temporary = int(temporary_only['معرّف الشخص'].count())

        assignee_ratio = (total_assignees / total_workforce * 100) if total_workforce else 0

        employee_selected_cost = float(employees_only[monthly_col].sum()) if not employees_only.empty else 0
        assignee_selected_cost = float(assignees_only[monthly_col].sum()) if not assignees_only.empty else 0
        temporary_selected_cost = float(temporary_only[monthly_col].sum()) if not temporary_only.empty else 0

        assignee_company_cost = float(assignees_only['تكلفة الشركة الشهرية'].sum()) if not assignees_only.empty else 0
        assignee_mewa_cost = float(assignees_only['تكلفة الوزارة الشهرية'].sum()) if not assignees_only.empty else 0

        mix_cols = st.columns(5)
        mix_cols[0].metric("إجمالي القوى العاملة", fmt_int(total_workforce))
        mix_cols[1].metric("عدد الموظفين", fmt_int(total_employees))
        mix_cols[2].metric("عدد المعارين", fmt_int(total_assignees))
        mix_cols[3].metric("عدد العقود المؤقتة", fmt_int(total_temporary))
        mix_cols[4].metric("نسبة المعارين", f"{assignee_ratio:.1f}%")

        mix_cols2 = st.columns(4)
        mix_cols2[0].metric("تكلفة الموظفين شهرياً", fmt_money(employee_selected_cost))
        mix_cols2[1].metric("تكلفة المعارين شهرياً", fmt_money(assignee_selected_cost))
        mix_cols2[2].metric("تكلفة العقود المؤقتة شهرياً", fmt_money(temporary_selected_cost))
        if (assignee_company_cost + assignee_mewa_cost) > 0:
            company_share = assignee_company_cost / (assignee_company_cost + assignee_mewa_cost) * 100
            mix_cols2[3].metric("نسبة تحمل الشركة للمعارين", f"{company_share:.1f}%")
        else:
            mix_cols2[3].metric("نسبة تحمل الشركة للمعارين", "0.0%")

        mix_cols3 = st.columns(2)
        mix_cols3[0].metric("تكلفة الشركة للمعارين شهرياً", fmt_money(assignee_company_cost))
        mix_cols3[1].metric("تكلفة الوزارة للمعارين شهرياً", fmt_money(assignee_mewa_cost))

        st.markdown("### ملخص الجهة حسب نوع الموظف")
        render_financial_table(mix_summary)

        headcount_pivot = mix_summary.pivot_table(
            index='الجهة',
            columns='نوع الموظف',
            values='عدد_الموظفين',
            aggfunc='sum',
            fill_value=0
        ).reset_index()

        type_cols = [c for c in headcount_pivot.columns if c != 'الجهة']
        headcount_pivot['الإجمالي'] = headcount_pivot[type_cols].sum(axis=1) if type_cols else 0

        assignee_col = 'إعارة' if 'إعارة' in headcount_pivot.columns else ('معار' if 'معار' in headcount_pivot.columns else None)
        if assignee_col:
            headcount_pivot['نسبة المعارين %'] = (
                headcount_pivot[assignee_col] / headcount_pivot['الإجمالي'] * 100
            ).replace([float('inf'), -float('inf')], 0).fillna(0).round(1)
        else:
            headcount_pivot['نسبة المعارين %'] = 0

        st.markdown("### عدد الموظفين والمعارين حسب الجهة")
        st.dataframe(
            headcount_pivot.sort_values('نسبة المعارين %', ascending=False),
            use_container_width=True,
            hide_index=True
        )

        # تحسين الأداء: جعل الرسوم اختيارية داخل هذا التبويب الثقيل
        show_mix_charts = st.toggle("عرض رسوم تحليل القوى العاملة", value=False)

        if show_mix_charts:
            fig_mix_count = px.bar(
                mix_summary,
                x='الجهة',
                y='عدد_الموظفين',
                color='نوع الموظف',
                barmode='group',
                text='عدد_الموظفين',
                title="عدد الموظفين والمعارين حسب الجهة"
            )
            fig_mix_count.update_layout(xaxis_title="", yaxis_title="عدد الموظفين", height=420)
            render_chart(fig_mix_count)

            fig_mix_cost = px.bar(
                mix_summary,
                x='الجهة',
                y='القيمة_الشهرية_المختارة',
                color='نوع الموظف',
                barmode='group',
                text='عدد_الموظفين',
                title=f"{view_mode} شهرياً حسب الجهة ونوع الموظف"
            )
            fig_mix_cost.update_layout(xaxis_title="", yaxis_title="القيمة", height=420)
            render_chart(fig_mix_cost)

        if not assignees_only.empty:
            assignee_by_unit = assignees_only.groupby('الجهة', dropna=False).agg(
                عدد_المعارين=('معرّف الشخص', 'count'),
                تكلفة_الشركة_شهرياً=('تكلفة الشركة الشهرية', 'sum'),
                تكلفة_الوزارة_شهرياً=('تكلفة الوزارة الشهرية', 'sum'),
                التكلفة_الإجمالية_شهرياً=('التكلفة الشهرية الإجمالية', 'sum')
            ).reset_index()

            assignee_by_unit['نسبة_تحمل_الشركة %'] = (
                assignee_by_unit['تكلفة_الشركة_شهرياً'] /
                assignee_by_unit['التكلفة_الإجمالية_شهرياً'] * 100
            ).replace([float('inf'), -float('inf')], 0).fillna(0).round(1)

            st.markdown("### تحليل المعارين حسب الجهة")
            st.dataframe(
                format_financial_dataframe(assignee_by_unit.sort_values('عدد_المعارين', ascending=False)),
                use_container_width=True,
                hide_index=True
            )

            top_unit = assignee_by_unit.sort_values('عدد_المعارين', ascending=False).iloc[0]
            st.warning(
                f"🔴 أعلى جهة من حيث الاعتماد على المعارين: "
                f"{top_unit['الجهة']} ({int(top_unit['عدد_المعارين'])} معار)"
            )

            if show_mix_charts:
                fig_assignee_burden = px.bar(
                    assignee_by_unit,
                    x='الجهة',
                    y=['تكلفة_الشركة_شهرياً', 'تكلفة_الوزارة_شهرياً'],
                    barmode='group',
                    title="تكلفة المعارين: الشركة مقابل الوزارة حسب الجهة"
                )
                fig_assignee_burden.update_layout(xaxis_title="", yaxis_title="القيمة الشهرية", height=420)
                render_chart(fig_assignee_burden)

        st.download_button(
            "تحميل تحليل القوى العاملة CSV",
            mix_summary.to_csv(index=False).encode("utf-8-sig"),
            "workforce_mix.csv",
            "text/csv"
        )


# =========================
# حل نهائي لصندوق رفع الملف وفراغات السايدبار
# =========================


# =========================


# =========================
# تصميم زر الرفع والنافذة
# =========================


with workforce_tab:
    st.markdown("---")
    st.subheader("تحليل الأعمار")

    age_col = next((c for c in AGE_COLUMNS if c in filtered.columns), None)

    if age_col is None:
        st.warning("عمود العمر غير موجود.")
    else:
        age_df = filtered.copy()
        age_df['العمر'] = pd.to_numeric(age_df[age_col], errors='coerce')
        age_df = age_df[age_df['العمر'].notna()].copy()

        if age_df.empty:
            st.info("لا توجد بيانات أعمار صالحة حسب الفلاتر الحالية.")
        else:
            age_df['الفئة العمرية'] = pd.cut(
                age_df['العمر'],
                bins=[0, 24, 30, 40, 50, 100],
                labels=['أقل من 25', '25-30', '31-40', '41-50', '50+']
            )

            age_group_summary = age_df.groupby('الفئة العمرية', dropna=False).agg(
                عدد_الموظفين=('معرّف الشخص', 'count'),
                متوسط_التكلفة=(monthly_col, 'mean')
            ).reset_index()

            age_group_summary['متوسط_التكلفة'] = (
                age_group_summary['متوسط_التكلفة']
                .fillna(0)
                .round(0)
                .astype(int)
            )

            age_cols = st.columns(3)
            age_cols[0].metric("متوسط العمر", round(age_df['العمر'].mean(), 1))
            age_cols[1].metric("أصغر عمر", int(age_df['العمر'].min()))
            age_cols[2].metric("أكبر عمر", int(age_df['العمر'].max()))

            st.markdown("### توزيع الأعمار حسب الفئة العمرية")
            st.dataframe(
                format_financial_dataframe(age_group_summary),
                use_container_width=True,
                hide_index=True
            )

            chart_type = st.radio(
                "نوع رسم توزيع الأعمار",
                ["أعمدة", "خطي", "دائري"],
                horizontal=True,
                key="age_distribution_chart_type"
            )

            if chart_type == "أعمدة":
                fig_age = px.bar(
                    age_group_summary,
                    x='الفئة العمرية',
                    y='عدد_الموظفين',
                    text='عدد_الموظفين',
                    title='توزيع القوى العاملة حسب الفئات العمرية'
                )
                fig_age.update_traces(texttemplate='%{text:,.0f}', textposition='inside')

            elif chart_type == "خطي":
                fig_age = px.line(
                    age_group_summary,
                    x='الفئة العمرية',
                    y='عدد_الموظفين',
                    markers=True,
                    title='توزيع القوى العاملة حسب الفئات العمرية'
                )
                fig_age.update_traces(texttemplate='%{y:,.0f}', textposition='top center')

            else:
                fig_age = px.pie(
                    age_group_summary,
                    names='الفئة العمرية',
                    values='عدد_الموظفين',
                    title='توزيع القوى العاملة حسب الفئات العمرية'
                )
                fig_age.update_traces(textinfo='label+percent+value')

            fig_age.update_layout(
                xaxis_title='',
                yaxis_title='عدد الموظفين',
                height=420
            )
            fig_age.update_yaxes(tickformat=',.0f')
            render_chart(fig_age)

            cost_chart_type = st.radio(
                "نوع رسم متوسط التكلفة",
                ["أعمدة", "خطي", "مساحة"],
                horizontal=True,
                key="age_cost_chart_type"
            )

            age_group_summary['متوسط_التكلفة_منسق'] = age_group_summary['متوسط_التكلفة'].map(lambda x: f'{x:,.0f}')

            if cost_chart_type == "أعمدة":
                fig_cost = px.bar(
                    age_group_summary,
                    x='الفئة العمرية',
                    y='متوسط_التكلفة',
                    text='متوسط_التكلفة_منسق',
                    title='متوسط التكلفة حسب الفئة العمرية'
                )
                fig_cost.update_traces(texttemplate='%{text}', textposition='inside')

            elif cost_chart_type == "خطي":
                fig_cost = px.line(
                    age_group_summary,
                    x='الفئة العمرية',
                    y='متوسط_التكلفة',
                    markers=True,
                    text='متوسط_التكلفة_منسق',
                    title='متوسط التكلفة حسب الفئة العمرية'
                )
                fig_cost.update_traces(texttemplate='%{text}', textposition='top center')

            else:
                fig_cost = px.area(
                    age_group_summary,
                    x='الفئة العمرية',
                    y='متوسط_التكلفة',
                    text='متوسط_التكلفة_منسق',
                    title='متوسط التكلفة حسب الفئة العمرية'
                )
                fig_cost.update_traces(texttemplate='%{text}', textposition='top center')

            fig_cost.update_layout(
                xaxis_title='',
                yaxis_title='متوسط التكلفة',
                height=420
            )
            fig_cost.update_yaxes(tickformat=',.0f')
            render_chart(fig_cost)


with work_extra_tab:
    render_work_extra_tab(work_extra_raw_all, work_extra_long_all, df)

with trips_tab:
    render_business_trips_tab(business_trips_all, df)
