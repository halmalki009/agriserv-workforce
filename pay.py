import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime
import re

# =========================
# إعدادات الصفحة
# =========================
st.set_page_config(
    page_title="داشبورد تكاليف الموظفين",
    page_icon="📊",
    layout="wide"
)

# =========================
# Executive Clean Mode
# =========================
st.markdown("""
<style>

/* إخفاء قائمة Streamlit */
#MainMenu {
    visibility: hidden;
}



/* إخفاء الفوتر */
footer {
    visibility: hidden;
}

/* إخفاء أدوات Streamlit العلوية */
[data-testid="stToolbar"] {
    display: none !important;
}

/* تقليل المسافة العلوية */
.block-container {
    padding-top: 1rem !important;
}



/* =========================
   Mobile Responsive Design
========================= */
@media (max-width: 768px) {

    /* Main container */
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 0.5rem !important;
    }

    /* Dashboard title */
    h1 {
        font-size: 2.4rem !important;
        line-height: 1.4 !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
    }

    /* KPI cards */
    .metric-card {
        padding: 18px !important;
        border-radius: 18px !important;
        margin-bottom: 14px !important;
    }

    .metric-card h3 {
        font-size: 1rem !important;
    }

    .metric-card h2 {
        font-size: 2rem !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        width: 260px !important;
    }

    /* Tables */
    .stDataFrame, .dataframe {
        overflow-x: auto !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        min-width: max-content !important;
        padding: 10px 14px !important;
        font-size: 0.9rem !important;
    }

    div[role="tablist"] {
        overflow-x: auto !important;
        white-space: nowrap !important;
    }

    /* Logo */
    img {
        max-width: 140px !important;
        height: auto !important;
    }
}


/* =========================
   Sidebar Mobile Fix
========================= */



/* تحسين ظهور السايدبار في الجوال */
@media (max-width: 768px) {

    section[data-testid="stSidebar"] {
        min-width: 280px !important;
        max-width: 280px !important;
    }

    /* منع اختفاء السايدبار */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: 0px !important;
    }
}



/* =========================
   Safe Executive Mode
========================= */

/* إخفاء Main Menu فقط */
#MainMenu {
    visibility: hidden !important;
}

/* إخفاء Footer فقط */
footer {
    visibility: hidden !important;
}

/* إخفاء شريط أدوات Streamlit بدون التأثير على Sidebar */
[data-testid="stToolbar"] {
    visibility: hidden !important;
    height: 0px !important;
    position: fixed !important;
}

/* الحفاظ على زر الفلاتر والسايدبار */
[data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    z-index: 999999 !important;
}

/* تحسين الجوال */
@media (max-width: 768px) {

    section[data-testid="stSidebar"] {
        min-width: 280px !important;
        max-width: 280px !important;
    }

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ===== CSS هنا =====
st.markdown("""
<style>
.smart-card {
    background: linear-gradient(135deg, #ffffff 0%, #f7f9fc 100%);
    border-radius: 22px;
    padding: 22px 20px;
    min-height: 140px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.05);
    direction: rtl;
    text-align: right;
}

.smart-card-title {
    font-size: 14px;
    font-weight: 700;
    color: #344054;
    margin-bottom: 12px;
}

.smart-card-value {
    font-size: clamp(22px, 3vw, 38px);
    font-weight: 900;
    color: #101828;
    line-height: 1.2;
    word-break: break-word;
}



/* نصوص صندوق الرفع */
section[data-testid="stFileUploader"] div,
section[data-testid="stFileUploader"] span,
section[data-testid="stFileUploader"] p,
section[data-testid="stFileUploader"] small {
    color: #334155 !important;
}

/* أيقونات منطقة الرفع فقط */
section[data-testid="stFileUploader"] svg {
    color: #0B3C5D !important;
    fill: #0B3C5D !important;
    opacity: 0.95 !important;
}



/* تحسين صندوق رفع الملف بدون التأثير على أيقونات Streamlit */
section[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    padding: 12px !important;
    border: 1px solid rgba(255,255,255,0.35) !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.12) !important;
}

section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] {
    min-height: 58px !important;
    border-radius: 12px !important;
    background: #FFFFFF !important;
    border: 1px dashed #CBD5E1 !important;
}

/* زر الرفع واضح بدون تكرار النص */
section[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"],
section[data-testid="stFileUploader"] button[kind="secondary"] {
    background-color: #0B3C5D !important;
    border: 1px solid #0B3C5D !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    opacity: 1 !important;
    font-weight: 800 !important;
    box-shadow: none !important;
}

section[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"] *,
section[data-testid="stFileUploader"] button[kind="secondary"] * {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

section[data-testid="stFileUploader"] button[data-testid="stBaseButton-secondary"]:hover,
section[data-testid="stFileUploader"] button[kind="secondary"]:hover {
    background-color: #0C8A73 !important;
    border-color: #0C8A73 !important;
}

/* نصوص داخل صندوق الرفع */
section[data-testid="stFileUploader"] div,
section[data-testid="stFileUploader"] span,
section[data-testid="stFileUploader"] small {
    color: #0B3C5D !important;
}

/* لا تغيّر خط أيقونات Streamlit */
.material-icons,
.material-icons-outlined,
.material-symbols-outlined,
.material-symbols-rounded,
span[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
}


/* =========================
   تطبيق خط SST Arabic على كامل اللوحة
   ========================= */
:root {
    --app-font: "SST Arabic", "SSTArabic", "SST Arabic Roman", "SST Arabic Medium",
                "IBM Plex Sans Arabic", "Tahoma", "Arial", sans-serif;
}

html, body, .stApp, .block-container,
.stMarkdown, .stDataFrame, .stMetric,
p, div, span, label,
h1, h2, h3, h4, h5, h6,
button, input, textarea,
[data-testid="stSidebar"],
[data-testid="stTable"],
[data-testid="stDataFrame"],
[data-baseweb="tab"],
[data-baseweb="select"],
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="option"],
[data-testid="stWidgetLabel"] {
    font-family: var(--app-font) !important;
}

/* الجداول */
div[data-testid="stDataFrame"] *,
div[data-testid="stTable"] * {
    font-family: var(--app-font) !important;
}

/* الفلاتر والقوائم */
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] div[data-baseweb="select"] *,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    font-family: var(--app-font) !important;
}

/* مهم: استثناء أيقونات Streamlit حتى لا تظهر كنص */
.material-icons,
.material-icons-outlined,
.material-symbols-outlined,
.material-symbols-rounded,
.material-symbols-sharp,
span[class*="material"],
span[data-testid="stIconMaterial"],
[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    font-weight: normal !important;
    font-style: normal !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    -webkit-font-feature-settings: "liga" !important;
    -webkit-font-smoothing: antialiased !important;
}


/* =========================
   تنبيهات الاستحقاقات - ألوان ناعمة لا تؤثر على جمالية اللوحة
   ========================= */
.alert-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 15px 14px;
    min-height: 104px;
    box-shadow: 0 8px 18px rgba(15,23,42,0.07);
    border: 1px solid #E6EAF0;
    direction: rtl;
    text-align: center;
}
.alert-card.red { border-top: 4px solid #F04438; }
.alert-card.orange { border-top: 4px solid #F79009; }
.alert-card.green { border-top: 4px solid #12B76A; }
.alert-card.blue { border-top: 4px solid #0B3C5D; }
.alert-card-title {
    font-size: 13px;
    font-weight: 800;
    color: #475467;
    margin-bottom: 8px;
}
.alert-card-value {
    font-size: clamp(20px, 2.4vw, 30px);
    font-weight: 900;
    color: #101828;
    line-height: 1.15;
}
.alert-note {
    background: #FFFFFF;
    border-right: 5px solid #0B3C5D;
    border-radius: 14px;
    padding: 12px 16px;
    margin: 8px 0 16px 0;
    color: #0B3C5D;
    font-weight: 700;
    direction: rtl;
    text-align: right;
    box-shadow: 0 6px 14px rgba(15,23,42,0.06);
}

/* تحسين الجداول التنفيذية */
div[data-testid="stDataFrame"] table {
    font-family: "SST Arabic", "SSTArabic", "IBM Plex Sans Arabic", Tahoma, Arial, sans-serif !important;
}

div[data-testid="stDataFrame"] th {
    text-align: center !important;
    vertical-align: middle !important;
    font-weight: 800 !important;
    font-size: 13px !important;
}

div[data-testid="stDataFrame"] td {
    text-align: center !important;
    vertical-align: middle !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding-top: 8px !important;
    padding-bottom: 8px !important;
}

/* تحسين الجداول الداخلية */
[data-testid="stDataFrameResizable"] * {
    font-family: "SST Arabic", "SSTArabic", "IBM Plex Sans Arabic", Tahoma, Arial, sans-serif !important;
}

/* توسيط عناصر المؤشرات */
.metric-label,
.metric-value {
    text-align: center !important;
    width: 100%;
}

/* تحسين التبويبات */
.stTabs [data-baseweb="tab"] {
    justify-content: center !important;
    align-items: center !important;
}

/* تحسين Plotly */
.js-plotly-plot .plotly * {
    font-family: "SST Arabic", "SSTArabic", "IBM Plex Sans Arabic", Tahoma, Arial, sans-serif !important;
}


/* ===== Executive DataFrame Styling ===== */

[data-testid="stDataFrame"] {
    direction: rtl !important;
}

[data-testid="stDataFrame"] * {
    font-family: "SST Arabic", "SSTArabic", "IBM Plex Sans Arabic", Tahoma, Arial, sans-serif !important;
}

/* Glide Data Grid cells */
[data-testid="stDataFrame"] div[role="gridcell"] {
    text-align: center !important;
    justify-content: center !important;
    align-items: center !important;
    display: flex !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* Column headers */
[data-testid="stDataFrame"] div[role="columnheader"] {
    text-align: center !important;
    justify-content: center !important;
    align-items: center !important;
    display: flex !important;
    font-size: 13px !important;
    font-weight: 800 !important;
}

/* Header text */
[data-testid="stDataFrame"] div[role="columnheader"] * {
    text-align: center !important;
    justify-content: center !important;
}

/* Cell inner content */
[data-testid="stDataFrame"] div[role="gridcell"] * {
    text-align: center !important;
    justify-content: center !important;
}

/* Metrics */
.metric-label,
.metric-value {
    text-align: center !important;
    width: 100% !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    justify-content: center !important;
    align-items: center !important;
    font-family: "SST Arabic", "SSTArabic", "IBM Plex Sans Arabic", Tahoma, Arial, sans-serif !important;
}

/* Plotly */
.js-plotly-plot .plotly * {
    font-family: "SST Arabic", "SSTArabic", "IBM Plex Sans Arabic", Tahoma, Arial, sans-serif !important;
}


/* ===== تحسين التقارير والجداول ===== */

/* استهداف الجداول داخل التقارير */
[data-testid="stDataFrame"] div[role="grid"] {
    direction: rtl !important;
}

/* توسيط رؤوس الأعمدة */
[data-testid="stDataFrame"] [role="columnheader"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    font-family: "SST Arabic", "SSTArabic", Tahoma, Arial, sans-serif !important;
    font-weight: 800 !important;
}

/* توسيط بيانات التقارير */
[data-testid="stDataFrame"] [role="gridcell"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    font-family: "SST Arabic", "SSTArabic", Tahoma, Arial, sans-serif !important;
    font-weight: 600 !important;
}

/* تحسين ارتفاع الصفوف */
[data-testid="stDataFrame"] [role="row"] {
    min-height: 42px !important;
}

/* منع اختلاف الخط داخل التقارير */
[data-testid="stDataFrame"] canvas {
    font-family: "SST Arabic", "SSTArabic", Tahoma, Arial, sans-serif !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# تنسيق الواجهة
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #F4F7F9;
}


html, body, .stApp, .block-container,
.stMarkdown, .stDataFrame, .stMetric,
p, h1, h2, h3, h4, h5, h6, label,
input, textarea, [data-testid="stSidebar"],
[data-testid="stTable"], [data-testid="stDataFrame"],
[data-baseweb="tab"], [data-baseweb="select"] {
    font-family: "SST Arabic", "SSTArabic", "SST Arabic Roman", "SST Arabic Medium",
                 "IBM Plex Sans Arabic", "Tahoma", "Arial", sans-serif !important;
}

html, body, [class*="css"], .stApp, .block-container, .stMarkdown, .stDataFrame, .stMetric {
    font-size: 15px;
}

/* مهم: عدم تغيير خط الأيقونات حتى لا تظهر نصوص مثل keyboard_double_arrow_right */
.material-icons,
.material-icons-outlined,
.material-symbols-outlined,
.material-symbols-rounded,
.material-symbols-sharp,
span[class*="material"],
span[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    font-weight: normal !important;
    font-style: normal !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    -webkit-font-feature-settings: "liga" !important;
    -webkit-font-smoothing: antialiased !important;
}

.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 1rem !important;
}

h1, h2, h3 {
    margin-top: 0 !important;
    padding-top: 0 !important;
    line-height: 1.4 !important;
    color: #0B3C5D;
}

.metric-card {
    background: linear-gradient(135deg, #0B3C5D 0%, #0C8A73 100%);
    border-radius: 16px;
    padding: 12px 16px;

    width: 100%;
    max-width: 260px;
    margin: 0 auto 8px auto;

    box-shadow: 0 6px 14px rgba(0,0,0,0.10);

    display: flex;
    flex-direction: column;
    justify-content: center;   /* عمودي */
    align-items: center;       /* أفقي */
    text-align: center;        /* النص */
}

.metric-card.total {
    background: linear-gradient(135deg, #1B5E20 0%, #008000 100%);
}

.metric-card.light {
    background: #FFFFFF;
    box-shadow: 0 8px 18px rgba(15,23,42,0.08);
}

.metric-card.light .metric-label {
    color: #25324D !important;
}

.metric-card.light .metric-value {
    color: #101124 !important;
}

.metric-label {
    font-size: 12px;
    color: rgba(255,255,255,0.88) !important;
    font-weight: 700;
    margin-bottom: 5px;
}

.metric-value {
    font-size: clamp(16px, 1.45vw, 22px);
    font-weight: 900;
    color: #FFFFFF !important;
    line-height: 1.1;
    white-space: nowrap;
}

section[data-testid="stSidebar"] {
    background-color: #173A70;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #0B3C5D !important;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: white !important;
}


/* تنسيق احترافي لمنطقة رفع الملف بدون التأثير على نص زر الرفع */
section[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.96) !important;
    border-radius: 14px !important;
    padding: 12px !important;
    border: 1px solid rgba(255,255,255,0.35) !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.12) !important;
}

section[data-testid="stFileUploader"] label {
    color: #FFFFFF !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}

section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] {
    min-height: 54px !important;
    padding: 8px !important;
    border-radius: 12px !important;
    background-color: #FFFFFF !important;
    border: 1px dashed #CBD5E1 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    border-bottom: 2px solid #D9E2EC;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding: 0 18px;
    background-color: #EAF1F6;
    border-radius: 12px 12px 0 0;
    color: #0B3C5D !important;
    font-weight: 700;
}

.stTabs [data-baseweb="tab"] p {
    color: #0B3C5D !important;
    font-weight: 700 !important;
}

.stTabs [aria-selected="true"] {
    background-color: #0B3C5D !important;
    color: white !important;
}

.stTabs [aria-selected="true"] p {
    color: white !important;
}

div[data-testid="stDataFrame"] div[role="grid"] {
    direction: rtl;
}

.drill-box {
    background: #FFFFFF;
    border: 1px solid #D9E2EC;
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: 0 6px 14px rgba(15,23,42,0.06);
    direction: rtl;
    text-align: right;
}

.drill-title {
    font-size: 15px;
    font-weight: 800;
    color: #0B3C5D;
    margin-bottom: 6px;
}

.drill-path {
    background: #EAF1F6;
    border-right: 5px solid #0C8A73;
    border-radius: 12px;
    padding: 12px 16px;
    margin: 8px 0 18px 0;
    color: #0B3C5D;
    font-weight: 800;
    direction: rtl;
    text-align: right;
}

/* توقيع بسيط بدون خلفية وبدون تداخل مع الفلاتر */
.footer-signature {
    margin-top: 18px;
    padding-top: 10px;
    font-size: 12px;
    color: #FFFFFF !important;
    opacity: 0.75;
    background: transparent !important;
    pointer-events: none;
    text-align: left;
}

</style>
""", unsafe_allow_html=True)

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
                لوحة تحليل تكاليف الموظفين
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
DATA_PATH = Path(__file__).parent / "employee_cost_data.xlsx"
ARABIC_NUM_FORMAT = "{:,.0f}"

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


def build_org_unit(dataframe: pd.DataFrame) -> pd.Series:
    """بناء الجهة للـ Workforce Mix بدون ترك أي جهة فارغة."""
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
        if not DATA_PATH.exists():
            st.error(f"لم يتم العثور على ملف البيانات: {DATA_PATH.name}. تأكد من رفع employee_cost_data.xlsx في نفس مجلد pay.py داخل GitHub.")
            st.stop()
        xl = pd.ExcelFile(DATA_PATH)
    else:
        xl = pd.ExcelFile(file_bytes)

    raw = pd.read_excel(xl, sheet_name='ناتج ملف Excel', header=2)
    raw.columns = [re.sub(r'\s+', ' ', str(c).replace('\u200f', '').replace('\u200e', '').replace('\xa0', ' ')).strip() for c in raw.columns]
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

    st.dataframe(format_financial_dataframe(view_df), use_container_width=True, hide_index=True)

    fig = px.bar(
        view_df,
        x=group_col,
        y=value_col,
        text='عدد_الموظفين',
        title=chart_title
    )
    fig.update_layout(xaxis_title="", yaxis_title="القيمة الشهرية", height=340)
    render_chart(fig)


# =========================
# تحميل البيانات
# =========================

# =========================
# Executive Version - Fixed Data Source
# =========================
df = load_data()

# بناء تنبيهات الاستحقاق السنوي
df = build_anniversary_alerts(df)

# =========================
# الفلاتر
# =========================
with st.sidebar:
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.25); margin:6px 0 10px 0;'>", unsafe_allow_html=True)
    st.header("خيارات التصفية")

    emp_types = sorted([x for x in df['نوع الموظف'].dropna().unique().tolist() if str(x).strip()])
    type_choice = st.radio("نوع الموظف", ["الكل"] + emp_types)

    sectors = sorted([x for x in df['القطاع'].dropna().unique().tolist() if str(x).strip()])
    sector_choice = st.multiselect("القطاع", options=sectors, default=[], key="sector_choice")

    # فلتر الإدارة العامة مرتبط بالقطاع
    if sector_choice:
        general_admins = sorted([
            x for x in df.loc[df['القطاع'].isin(sector_choice), 'الإدارة العامة'].dropna().unique().tolist()
            if str(x).strip() and str(x).strip() not in ["0", "nan"]
        ])
    else:
        general_admins = sorted([
            x for x in df['الإدارة العامة'].dropna().unique().tolist()
            if str(x).strip() and str(x).strip() not in ["0", "nan"]
        ])

    previous_general_admins = st.session_state.get("general_admin_choice", [])
    valid_general_admins = [x for x in previous_general_admins if x in general_admins]

    general_admin_choice = st.multiselect(
        "الإدارة العامة",
        options=general_admins,
        default=valid_general_admins,
        key="general_admin_choice"
    )

    # فلتر الإدارة مرتبط بالقطاع والإدارة العامة
    admin_source = df.copy()
    if sector_choice:
        admin_source = admin_source[admin_source['القطاع'].isin(sector_choice)]
    if general_admin_choice:
        admin_source = admin_source[admin_source['الإدارة العامة'].isin(general_admin_choice)]

    admins = sorted([
        x for x in admin_source['الإدارة'].dropna().unique().tolist()
        if str(x).strip() and str(x).strip() not in ["0", "nan"]
    ])

    previous_admins = st.session_state.get("admin_choice", [])
    valid_admins = [x for x in previous_admins if x in admins]

    admin_choice = st.multiselect(
        "الإدارة",
        options=admins,
        default=valid_admins,
        key="admin_choice"
    )

    # فلتر الموقع الفعلي مرتبط بالقطاع والإدارة العامة والإدارة
    location_choice = []
    if 'الموقع الفعلي' in df.columns:
        location_source = df.copy()
        if sector_choice:
            location_source = location_source[location_source['القطاع'].isin(sector_choice)]
        if general_admin_choice:
            location_source = location_source[location_source['الإدارة العامة'].isin(general_admin_choice)]
        if admin_choice:
            location_source = location_source[location_source['الإدارة'].isin(admin_choice)]

        location_source['الموقع الفعلي'] = clean_text_value(location_source['الموقع الفعلي'])
        locations = sorted([
            x for x in location_source['الموقع الفعلي'].dropna().unique().tolist()
            if str(x).strip() and str(x).strip() not in ["0", "nan"]
        ])

        previous_locations = st.session_state.get("location_choice", [])
        valid_locations = [x for x in previous_locations if x in locations]

        location_choice = st.multiselect(
            "الموقع الفعلي",
            options=locations,
            default=valid_locations,
            key="location_choice"
        )
    else:
        st.caption("عمود الموقع الفعلي غير موجود في ملف البيانات.")

    view_mode = st.radio(
        "عرض التكاليف",
        ["تكلفة الشركة فقط", "تكلفة الوزارة فقط", "التكلفة الإجمالية"],
        horizontal=False
    )

    st.markdown(
        "<div class='footer-signature'>by <b>Hussain Almalki</b></div>",
        unsafe_allow_html=True
    )

# =========================
# تطبيق الفلاتر
# =========================
filtered = df.copy()

if sector_choice:
    filtered = filtered[filtered['القطاع'].isin(sector_choice)]

if general_admin_choice:
    filtered = filtered[filtered['الإدارة العامة'].isin(general_admin_choice)]

if admin_choice:
    filtered = filtered[filtered['الإدارة'].isin(admin_choice)]

if 'الموقع الفعلي' in filtered.columns and location_choice:
    filtered = filtered[filtered['الموقع الفعلي'].isin(location_choice)]

if type_choice != "الكل":
    filtered = filtered[filtered['نوع الموظف'] == type_choice]

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

st.markdown("""
<div style="
    font-size:13px;
    color:#98A2B3;
    margin-top:-10px;
    margin-bottom:15px;
    text-align:right;
">
📍 مسار التحليل: القطاع ← الإدارة العامة ← الإدارة ← الموقع الفعلي ← الموظف
</div>
""", unsafe_allow_html=True)

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

    st.caption("للتفصيل حسب الجهات والإدارات والمواقع والموظفين استخدم تبويب التحليل المتدرج.")

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
possible_age_cols = [
    'العمر الحالي',
    'أعمار الموظفين',
    'Age',
    'AGE'
]

age_col = None
for c in possible_age_cols:
    if c in filtered.columns:
        age_col = c
        break

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
tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "التحليل المتدرج",
    "ملخص القطاعات",
    "ملخص الإدارات العامة",
    "ملخص الإدارات",
    "ملخص المواقع الفعلية",
    "تفاصيل الموظفين",
    "التنبيهات والاستحقاقات",
    "رسوم بيانية",
    "مقارنة الأنواع",
    "Workforce Mix"
])

with tab0:

    drill_kpi_cols = st.columns(5)
    sector_count = clean_sector_for_charts(filtered)['القطاع'].nunique() if 'القطاع' in filtered.columns else 0
    drill_kpi_cols[0].metric("عدد القطاعات", fmt_int(sector_count))
    drill_kpi_cols[1].metric("عدد الإدارات العامة", fmt_int(drill_general_admin_df['الإدارة العامة'].nunique() if not drill_general_admin_df.empty else 0))
    drill_kpi_cols[2].metric("عدد الإدارات", fmt_int(drill_admin_df['الإدارة'].nunique() if not drill_admin_df.empty else 0))
    drill_kpi_cols[3].metric("عدد المواقع الفعلية", fmt_int(drill_location_df['الموقع الفعلي'].nunique() if not drill_location_df.empty else 0))
    drill_kpi_cols[4].metric("عدد الموظفين", fmt_int(total_emp))

    st.markdown("### التحليل المتدرج حسب الاختيار الحالي")
    st.caption("يعرض هذا التبويب صورة عامة لكل المستويات، ثم يتقلص تدريجياً عند استخدام الفلاتر للوصول إلى المستوى التالي المناسب.")

    show_employee_level = False

    # بدون فلترة: Overview شامل لكل المستويات الأساسية
    if not sector_choice and not general_admin_choice and not admin_choice and not location_choice:
        st.markdown("#### نظرة عامة حسب المستويات")
        render_drill_card(
            "الجهات حسب التكلفة الشهرية المختارة",
            drill_unit_df,
            'الجهة',
            'التكلفة_الشهرية',
            "أعلى الجهات حسب التكلفة الشهرية",
            key_suffix="unit_overview"
        )
        render_drill_card(
            "الإدارات العامة حسب التكلفة الشهرية المختارة",
            drill_general_admin_df,
            'الإدارة العامة',
            'التكلفة_الشهرية',
            "أعلى الإدارات العامة حسب التكلفة الشهرية",
            key_suffix="general_admin_overview"
        )
        render_drill_card(
            "الإدارات حسب التكلفة الشهرية المختارة",
            drill_admin_df,
            'الإدارة',
            'التكلفة_الشهرية',
            "أعلى الإدارات حسب التكلفة الشهرية",
            key_suffix="admin_overview"
        )
        render_drill_card(
            "المواقع الفعلية حسب التكلفة الشهرية المختارة",
            drill_location_df,
            'الموقع الفعلي',
            'التكلفة_الشهرية',
            "أعلى المواقع الفعلية حسب التكلفة الشهرية",
            key_suffix="location_overview"
        )

    # عند اختيار قطاع: نبدأ من المستويات التابعة له
    elif sector_choice and not general_admin_choice and not admin_choice and not location_choice:
        st.markdown("#### المستويات التابعة للقطاع المختار")
        render_drill_card(
            "الإدارات العامة التابعة للقطاع المختار",
            drill_general_admin_df,
            'الإدارة العامة',
            'التكلفة_الشهرية',
            "الإدارات العامة حسب التكلفة الشهرية",
            key_suffix="general_admin_after_sector"
        )
        render_drill_card(
            "الإدارات التابعة للقطاع المختار",
            drill_admin_df,
            'الإدارة',
            'التكلفة_الشهرية',
            "الإدارات حسب التكلفة الشهرية",
            key_suffix="admin_after_sector"
        )
        render_drill_card(
            "المواقع الفعلية التابعة للقطاع المختار",
            drill_location_df,
            'الموقع الفعلي',
            'التكلفة_الشهرية',
            "المواقع الفعلية حسب التكلفة الشهرية",
            key_suffix="location_after_sector"
        )

    # عند اختيار إدارة عامة: نبدأ من الإدارات والمواقع
    elif general_admin_choice and not admin_choice and not location_choice:
        st.markdown("#### المستويات التابعة للإدارة العامة المختارة")
        render_drill_card(
            "الإدارات التابعة للإدارة العامة المختارة",
            drill_admin_df,
            'الإدارة',
            'التكلفة_الشهرية',
            "الإدارات حسب التكلفة الشهرية",
            key_suffix="admin_after_general_admin"
        )
        render_drill_card(
            "المواقع الفعلية التابعة للإدارة العامة المختارة",
            drill_location_df,
            'الموقع الفعلي',
            'التكلفة_الشهرية',
            "المواقع الفعلية حسب التكلفة الشهرية",
            key_suffix="location_after_general_admin"
        )

    # عند اختيار إدارة: نعرض المواقع فقط
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

    # عند اختيار موقع: نصل لتفاصيل الموظفين
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
        "تحميل نتائج التحليل المتدرج CSV",
        drill_employee_df.to_csv(index=False).encode("utf-8-sig"),
        "drill_down_results.csv",
        "text/csv"
    )

with tab1:
    st.subheader("ملخص حسب القطاع")
    st.caption(f"العرض الحالي: {view_mode}")
    st.dataframe(format_financial_dataframe(sector_summary_view), use_container_width=True, hide_index=True)
    st.download_button(
        "تحميل ملخص القطاعات CSV",
        sector_summary_view.to_csv(index=False).encode("utf-8-sig"),
        "sector_summary.csv",
        "text/csv"
    )

with tab2:
    st.subheader("ملخص حسب الإدارة العامة")
    st.caption(f"العرض الحالي: {view_mode}")
    st.dataframe(format_financial_dataframe(general_admin_summary_view), use_container_width=True, hide_index=True)
    st.download_button(
        "تحميل ملخص الإدارات العامة CSV",
        general_admin_summary_view.to_csv(index=False).encode("utf-8-sig"),
        "general_admin_summary.csv",
        "text/csv"
    )

with tab3:
    st.subheader("ملخص حسب الإدارة")
    st.caption(f"العرض الحالي: {view_mode}")
    st.dataframe(format_financial_dataframe(admin_summary_view), use_container_width=True, hide_index=True)
    st.download_button(
        "تحميل ملخص الإدارات CSV",
        admin_summary_view.to_csv(index=False).encode("utf-8-sig"),
        "admin_summary.csv",
        "text/csv"
    )

with tab4:
    st.subheader("ملخص حسب الموقع الفعلي")
    st.caption(f"العرض الحالي: {view_mode}")

    if type_choice == "إعارة" and not location_summary_view.empty and monthly_summary_col in location_summary_view.columns:
        top_locations = location_summary_view.sort_values(
            monthly_summary_col,
            ascending=False
        ).head(5)

        st.markdown(f"### 🔎 أعلى 5 مواقع حسب {view_mode}")

        top_cols = st.columns(len(top_locations))
        for idx, (col, (_, row)) in enumerate(zip(top_cols, top_locations.iterrows()), start=1):
            location_name = row.get('الموقع الفعلي', 'غير محدد')
            cost_value = row.get(monthly_summary_col, 0)
            count_value = row.get('عدد_الموظفين', 0)
            col.markdown(
                f"""
                <div class='smart-card' style='min-height:115px; padding:14px 12px; text-align:center;'>
                    <div class='smart-card-title'>#{idx} {location_name}</div>
                    <div class='smart-card-value' style='font-size:22px;'>{fmt_money(cost_value)}</div>
                    <div style='font-size:12px; color:#667085; font-weight:700;'>عدد الموظفين: {fmt_int(int(count_value))}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    st.dataframe(format_financial_dataframe(location_summary_view), use_container_width=True, hide_index=True)
    st.download_button(
        "تحميل ملخص المواقع الفعلية CSV",
        location_summary_view.to_csv(index=False).encode("utf-8-sig"),
        "location_summary.csv",
        "text/csv"
    )

with tab5:
    st.subheader("تفاصيل الموظفين بعد التصفية")
    st.caption(f"العرض الحالي: {view_mode}")
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

with tab6:
    st.subheader("التنبيهات والاستحقاقات")
    st.caption("يتم احتساب الاستحقاق القادم سنوياً من تاريخ التعيين لجميع أنواع الموظفين، بغض النظر عن سنة التعيين.")

    alerts_df = filtered.copy()
    alerts_df['_ترتيب_الحالة'] = alert_status_order(alerts_df['حالة الاستحقاق'])
    alerts_df = alerts_df.sort_values(['_ترتيب_الحالة', 'الأيام المتبقية', monthly_col], ascending=[True, True, False])

    critical_df = alerts_df[alerts_df['حالة الاستحقاق'].eq('حرج')].copy()
    warning_df = alerts_df[alerts_df['حالة الاستحقاق'].eq('تنبيه')].copy()
    stable_df = alerts_df[alerts_df['حالة الاستحقاق'].eq('مستقر')].copy()

    affected_df = alerts_df[alerts_df['حالة الاستحقاق'].isin(['حرج', 'تنبيه'])].copy()
    affected_cost = float(affected_df[monthly_col].sum()) if not affected_df.empty else 0

    nearest_days = alerts_df['الأيام المتبقية'].dropna().min()
    nearest_days_display = "-" if pd.isna(nearest_days) else f"{int(nearest_days)} يوم"

    alert_cols = st.columns(4)
    alert_metrics = [
        ("🔴 حالات حرجة أقل من 60 يوم", fmt_int(len(critical_df)), "alert-card red"),
        ("🟠 حالات تنبيه من 60 إلى 70 يوم", fmt_int(len(warning_df)), "alert-card orange"),
        ("🟢 حالات مستقرة أكثر من 70 يوم", fmt_int(len(stable_df)), "alert-card green"),
        ("التكلفة الشهرية المتأثرة", fmt_money(affected_cost), "alert-card blue"),
    ]

    for col, (label, value, cls) in zip(alert_cols, alert_metrics):
        col.markdown(
            f"""
            <div class='{cls}'>
                <div class='alert-card-title'>{label}</div>
                <div class='alert-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class='alert-note'>
            أقرب استحقاق قادم بعد <b>{nearest_days_display}</b>.
            يعتمد التصنيف على تاريخ التعيين السنوي: أحمر أقل من 60 يوم، برتقالي من 60 إلى 70 يوم، أخضر أكثر من 70 يوم.
        </div>
        """,
        unsafe_allow_html=True
    )

    status_choice = st.radio(
        "تصفية حالات الاستحقاق",
        ["الكل", "🔴 حرج", "🟠 تنبيه", "🟢 مستقر"],
        horizontal=True,
        key="alert_status_filter"
    )

    alert_view_df = alerts_df.copy()
    if status_choice == "🔴 حرج":
        alert_view_df = alert_view_df[alert_view_df['حالة الاستحقاق'].eq('حرج')]
    elif status_choice == "🟠 تنبيه":
        alert_view_df = alert_view_df[alert_view_df['حالة الاستحقاق'].eq('تنبيه')]
    elif status_choice == "🟢 مستقر":
        alert_view_df = alert_view_df[alert_view_df['حالة الاستحقاق'].eq('مستقر')]

    alert_display_cols = [
        'معرّف الشخص', 'نوع الموظف', 'القطاع', 'الإدارة العامة', 'الإدارة',
        'الموقع الفعلي', 'العمر', 'تاريخ التعيين', 'تاريخ الاستحقاق القادم',
        'الأيام المتبقية', 'مؤشر الاستحقاق', 'الإجراء المقترح',
        display_monthly_label, display_annual_label
    ]
    alert_display_cols = [c for c in alert_display_cols if c in alert_view_df.columns]

    st.dataframe(
        format_financial_dataframe(alert_view_df[alert_display_cols]),
        use_container_width=True,
        hide_index=True
    )

    status_summary = alerts_df.groupby('مؤشر الاستحقاق', dropna=False).agg(
        عدد_الموظفين=('معرّف الشخص', 'count'),
        القيمة_الشهرية_المختارة=(monthly_col, 'sum'),
        متوسط_الأيام_المتبقية=('الأيام المتبقية', 'mean')
    ).reset_index()
    status_summary['متوسط_الأيام_المتبقية'] = status_summary['متوسط_الأيام_المتبقية'].round(0).astype('Int64')

    st.markdown("### ملخص الحالات حسب التصنيف")
    st.dataframe(format_financial_dataframe(status_summary), use_container_width=True, hide_index=True)

    show_alert_chart = st.toggle("عرض رسم التنبيهات", value=False, key="show_alert_chart")
    if show_alert_chart and not status_summary.empty:
        fig_alerts = px.bar(
            status_summary,
            x='مؤشر الاستحقاق',
            y='عدد_الموظفين',
            text='عدد_الموظفين',
            title="توزيع حالات الاستحقاق حسب عدد الموظفين"
        )
        fig_alerts.update_layout(xaxis_title="", yaxis_title="عدد الموظفين", height=380)
        render_chart(fig_alerts)

    st.download_button(
        "تحميل تنبيهات الاستحقاقات CSV",
        alert_view_df[alert_display_cols].to_csv(index=False).encode("utf-8-sig"),
        "employee_anniversary_alerts.csv",
        "text/csv"
    )


with tab7:
    st.subheader("الرسوم البيانية")
    st.caption(f"العرض الحالي: {view_mode}")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig1 = px.bar(
            sector_summary.head(10),
            x='القطاع',
            y=monthly_summary_col,
            text='عدد_الموظفين',
            title="أعلى القطاعات حسب التكلفة الشهرية"
        )
        fig1.update_layout(xaxis_title="", yaxis_title="القيمة", height=450)
        render_chart(fig1)

    with chart_col2:
        fig2 = px.pie(
            type_summary,
            names='نوع الموظف',
            values='عدد_الموظفين',
            title="توزيع الموظفين حسب النوع"
        )
        fig2.update_layout(height=450)
        render_chart(fig2)

    fig3 = px.bar(
        general_admin_summary.head(15),
        x='الإدارة العامة',
        y=monthly_summary_col,
        color='القطاع',
        title="أعلى الإدارات العامة حسب التكلفة الشهرية",
        text='عدد_الموظفين'
    )
    fig3.update_layout(xaxis_title="", yaxis_title="القيمة", height=520)
    render_chart(fig3)

    if not admin_summary.empty:
        fig4 = px.bar(
            admin_summary.head(15),
            x='الإدارة',
            y=monthly_summary_col,
            color='الإدارة العامة',
            title="أعلى الإدارات حسب التكلفة الشهرية",
            text='عدد_الموظفين'
        )
        fig4.update_layout(xaxis_title="", yaxis_title="القيمة", height=520)
        render_chart(fig4)

    if not location_summary.empty:
        fig5 = px.bar(
            location_summary.head(15),
            x='الموقع الفعلي',
            y=monthly_summary_col,
            title="أعلى المواقع الفعلية حسب التكلفة الشهرية",
            text='عدد_الموظفين'
        )
        fig5.update_layout(xaxis_title="", yaxis_title="القيمة", height=520)
        render_chart(fig5)

with tab8:
    st.subheader("مقارنة بين أنواع الموظفين")
    st.caption(f"العرض الحالي: {view_mode}")

    comparison_df = filtered.copy()

    types_comparison = comparison_df.groupby('نوع الموظف', dropna=False).agg(
        عدد_الموظفين=('معرّف الشخص', 'count'),
        القيمة_الشهرية_المختارة=(monthly_col, 'sum'),
        القيمة_السنوية_المختارة=(annual_col, 'sum'),
    ).reset_index()

    types_comparison['متوسط_القيمة_الشهرية_للموظف'] = (
        types_comparison['القيمة_الشهرية_المختارة'] / types_comparison['عدد_الموظفين']
    ).fillna(0)

    comparison_cols = st.columns(3)
    comparison_cols[0].metric("عدد الأنواع", fmt_int(types_comparison['نوع الموظف'].nunique()))
    comparison_cols[1].metric("إجمالي الموظفين", fmt_int(types_comparison['عدد_الموظفين'].sum()))
    comparison_cols[2].metric(f"إجمالي {view_mode} شهرياً", fmt_money(types_comparison['القيمة_الشهرية_المختارة'].sum()))

    st.dataframe(format_financial_dataframe(types_comparison), use_container_width=True, hide_index=True)

    fig_types_count = px.bar(
        types_comparison,
        x='نوع الموظف',
        y='عدد_الموظفين',
        text='عدد_الموظفين',
        title="عدد الموظفين حسب النوع"
    )
    fig_types_count.update_layout(xaxis_title="", yaxis_title="عدد الموظفين", height=400)
    render_chart(fig_types_count)

    fig_types_cost = px.bar(
        types_comparison,
        x='نوع الموظف',
        y='القيمة_الشهرية_المختارة',
        text='عدد_الموظفين',
        title=f"{view_mode} شهرياً حسب نوع الموظف"
    )
    fig_types_cost.update_layout(xaxis_title="", yaxis_title="القيمة", height=400)
    render_chart(fig_types_cost)


with tab9:
    st.subheader("Workforce Mix - مزيج القوى العاملة")
    st.caption("تحليل الموظفين والمعارين حسب الجهة. يتم بناء الجهة تلقائيًا من القطاع ثم الإدارة العامة ثم الإدارة، مع اعتبار الفروع كجهة مستقلة.")

    mix_df = filtered.copy()

    # حل الجهة: يمنع ظهور صفوف أو أعمدة فارغة في الجداول والرسوم
    mix_df['الجهة'] = build_org_unit(mix_df)

    # لا نعرض غير محدد في Workforce Mix حتى لا تظهر أعمدة/صفوف فارغة
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
        st.info("لا توجد بيانات كافية لعرض مزيج القوى العاملة.")
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
        st.dataframe(format_financial_dataframe(mix_summary), use_container_width=True, hide_index=True)

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
        show_mix_charts = st.toggle("عرض رسوم Workforce Mix", value=False)

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
            "تحميل Workforce Mix CSV",
            mix_summary.to_csv(index=False).encode("utf-8-sig"),
            "workforce_mix.csv",
            "text/csv"
        )


# =========================
# حل نهائي لصندوق رفع الملف وفراغات السايدبار
# =========================
st.markdown("""
<style>

/* صندوق رفع الملف: واضح وخفيف */
section[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    padding: 10px !important;
    margin-bottom: 10px !important;
    box-shadow: 0 6px 14px rgba(0,0,0,0.14) !important;
}

/* منطقة الرفع الداخلية */
section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] {
    min-height: 52px !important;
    height: 52px !important;
    padding: 8px 10px !important;
    background: #FFFFFF !important;
    border: 1px dashed #94A3B8 !important;
    border-radius: 12px !important;
}

/* زر Upload: نتركه بخلفية فاتحة لكن نجعل النص والأيقونة بلون واضح */
section[data-testid="stFileUploader"] button,
section[data-testid="stFileUploader"] button:disabled,
section[data-testid="stFileUploader"] button[kind="secondary"],
section[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] {
    background: #F8FAFC !important;
    background-color: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    color: #0B3C5D !important;
    -webkit-text-fill-color: #0B3C5D !important;
    opacity: 1 !important;
    filter: none !important;
    min-height: 34px !important;
    height: 34px !important;
    min-width: 96px !important;
    padding: 0 12px !important;
    box-shadow: none !important;
    font-weight: 800 !important;
}

/* نص وأيقونة Upload داخل الزر */
section[data-testid="stFileUploader"] button *,
section[data-testid="stFileUploader"] button:disabled *,
section[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] * {
    color: #0B3C5D !important;
    -webkit-text-fill-color: #0B3C5D !important;
    fill: #0B3C5D !important;
    opacity: 1 !important;
    filter: none !important;
    font-weight: 800 !important;
}

/* نصوص الصندوق */
section[data-testid="stFileUploader"] div,
section[data-testid="stFileUploader"] span,
section[data-testid="stFileUploader"] small,
section[data-testid="stFileUploader"] p {
    color: #0B3C5D !important;
    -webkit-text-fill-color: #0B3C5D !important;
    opacity: 1 !important;
}

/* منع أي فراغات كبيرة بين عناصر الفلاتر */
section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
}

section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stRadio {
    margin-bottom: 4px !important;
}

section[data-testid="stSidebar"] label {
    margin-bottom: 2px !important;
}

/* الحفاظ على خط الأيقونات وعدم تحويلها إلى نص */
.material-icons,
.material-icons-outlined,
.material-symbols-outlined,
.material-symbols-rounded,
span[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
st.markdown("""
<style>
/* ===== File uploader: زر واضح ومقروء ===== */
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    padding: 10px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 6px 14px rgba(0,0,0,0.14) !important;
}

section[data-testid="stSidebar"] section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF !important;
    border: 1px dashed #94A3B8 !important;
    border-radius: 12px !important;
    min-height: 54px !important;
    height: 54px !important;
    padding: 8px !important;
}

/* استهداف شامل لزر Upload حتى لو كان disabled */
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button,
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button:disabled,
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button[disabled],
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button[kind="secondary"],
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] {
    background: #0B3C5D !important;
    background-color: #0B3C5D !important;
    border: 1px solid #0B3C5D !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
    filter: none !important;
    box-shadow: 0 5px 12px rgba(11,60,93,0.24) !important;
    min-width: 112px !important;
    min-height: 38px !important;
    height: 38px !important;
    padding: 0 14px !important;
    font-weight: 800 !important;
}

/* النص والأيقونة داخل الزر */
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button *,
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button:disabled *,
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button[disabled] *,
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    fill: #FFFFFF !important;
    opacity: 1 !important;
    filter: none !important;
    font-weight: 800 !important;
}

/* نصوص صندوق الرفع خارج الزر */
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] div,
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] span:not([class*="material"]),
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] small,
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] p {
    color: #0B3C5D !important;
    -webkit-text-fill-color: #0B3C5D !important;
    opacity: 1 !important;
}

/* Hover */
section[data-testid="stSidebar"] section[data-testid="stFileUploader"] button:hover {
    background: #0C8A73 !important;
    background-color: #0C8A73 !important;
    border-color: #0C8A73 !important;
}

/* ===== توسيط مؤشرات st.metric ===== */
div[data-testid="stMetric"] {
    text-align: center !important;
}

div[data-testid="stMetric"] > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricValue"] {
    width: 100% !important;
    text-align: center !important;
    justify-content: center !important;
}

div[data-testid="stMetricLabel"] label,
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] > div {
    text-align: center !important;
    justify-content: center !important;
}

/* الحفاظ على أيقونات Streamlit */
.material-icons,
.material-icons-outlined,
.material-symbols-outlined,
.material-symbols-rounded,
.material-symbols-sharp,
span[class*="material"],
span[data-testid="stIconMaterial"],
[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# تصميم زر الرفع والنافذة
# =========================
st.markdown("""
<style>
/* زر الرفع في السايدبار */
section[data-testid="stSidebar"] .stButton button {
    background: #0B3C5D !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 12px !important;
    height: 42px !important;
    font-weight: 900 !important;
    box-shadow: 0 6px 14px rgba(0,0,0,0.16) !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #0C8A73 !important;
    color: #FFFFFF !important;
    border-color: #0C8A73 !important;
}

/* خط وواجهة النافذة */
div[role="dialog"] * {
    font-family: "SST Arabic", "SSTArabic", "SST Arabic Roman", "IBM Plex Sans Arabic", "Tahoma", "Arial", sans-serif !important;
}

/* زر النافذة */
div[role="dialog"] button {
    border-radius: 10px !important;
    font-weight: 800 !important;
}

/* صندوق رفع الملف داخل النافذة فقط */
div[role="dialog"] section[data-testid="stFileUploader"] {
    background: #F8FAFC !important;
    border-radius: 16px !important;
    padding: 14px !important;
    border: 1px solid #E2E8F0 !important;
}

div[role="dialog"] section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] {
    border-radius: 14px !important;
    border: 1.5px dashed #94A3B8 !important;
    background: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)


with tab9:
    st.markdown("---")
    st.subheader("تحليل الأعمار")
    st.caption("مرتبطة تلقائياً بالفلاتر الحالية ونوع الموظف.")

    possible_age_cols = ['العمر', 'العمر الحالي', 'أعمار الموظفين', 'Age', 'AGE']
    age_col = next((c for c in possible_age_cols if c in filtered.columns), None)

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
