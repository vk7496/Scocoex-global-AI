"""
SCOCOEX AI Core — دموی ترکیبی (نسخه Streamlit)
اجرا: streamlit run app.py
"""

import base64
import os
import time
import datetime as dt

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="SCOCOEX AI Core — دمو",
    page_icon="🟡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

NAVY = "#0b1f2e"
NAVY_800 = "#122b3e"
NAVY_700 = "#1a3a52"
GOLD = "#c9a24b"
GOLD_LIGHT = "#dab86a"
TEAL = "#3f8f9e"
INK = "#e9e4d6"
INK_DIM = "#a9b6c2"
GREEN = "#5ea87a"
RED = "#c85c5c"

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "scocoex_logo.png")
LOCAL_CSV_FALLBACK = os.path.join(os.path.dirname(__file__), "registrations_local.csv")

# ============================================================
# ۱۰ صنعت رسمی اسکوکواکس — این تفکیک در همه‌جای اپ (ثبت‌نام، تطبیق،
# جست‌وجوی پنل مدیریت) استفاده می‌شود تا سرچ/فیلتر سریع باشد.
# ============================================================
SECTORS = [
    "فولاد و زنجیره ارزش",
    "معادن: سنگ‌آهن، آلومینیوم و صنایع معدنی",
    "صنعت مس و فلزات",
    "صنعت نفت، گاز و پتروشیمی",
    "پالایشگاه‌ها، فرآورده‌های نفتی و تجارت انرژی",
    "مهندسی، ساخت، فناوری‌های انرژی و نیروگاه‌ها",
    "بانک‌ها، صندوق‌های ثروت ملی و سرمایه‌گذاری",
    "فناوری‌های نوین، هوش مصنوعی و بلاک‌چین",
    "صنایع غذایی، کشاورزی و امنیت غذایی",
    "صنایع دارویی، پزشکی و سلامت",
]

REG_COLUMNS = ["زمان ثبت", "نام شرکت", "کشور", "صنعت", "نام رابط", "ایمیل", "تلفن", "توضیحات"]

# ============================================================
# GLOBAL STYLE — RTL + brand look
# ============================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;900&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Vazirmatn', sans-serif !important;
}}

.stApp {{
    background:
        radial-gradient(1200px 600px at 15% -10%, rgba(201,162,75,0.08), transparent 60%),
        radial-gradient(900px 500px at 100% 0%, rgba(63,143,158,0.12), transparent 55%),
        {NAVY};
    color: {INK};
}}

.main .block-container {{
    direction: rtl;
    text-align: right;
    max-width: 1100px;
}}

h1, h2, h3, h4, h5, p, span, div, label {{
    direction: rtl;
    text-align: right;
}}

.scx-header {{
    display:flex; align-items:center; justify-content:space-between; gap:16px;
    padding: 14px 24px; border-radius: 14px;
    background: linear-gradient(135deg, {NAVY_800}, {NAVY_700});
    border: 1px solid rgba(201,162,75,0.25);
    margin-bottom: 18px;
}}
.scx-header img {{ height: 54px; }}
.scx-header .scx-sub {{ font-size: 12.5px; color:{INK_DIM}; margin-top:4px; }}
.scx-badge {{
    background:{GOLD}; color:{NAVY}; padding:5px 14px; border-radius:100px;
    font-size:11.5px; font-weight:700; white-space:nowrap;
}}

.scx-card {{
    background: linear-gradient(180deg, rgba(233,228,214,0.035), rgba(233,228,214,0.015));
    border:1px solid rgba(233,228,214,0.10);
    border-radius:14px;
    padding:18px 20px;
    margin-bottom:14px;
}}
.scx-tag {{ font-size:11px; color:{TEAL}; font-weight:700; }}
.scx-reason {{ font-size:12.8px; color:{INK_DIM}; line-height:1.85; margin-top:6px; }}
.scx-name {{ font-size:16px; font-weight:700; color:{INK}; margin:4px 0; }}

.stTabs [data-baseweb="tab-list"] {{ gap: 6px; direction: rtl; }}
.stTabs [data-baseweb="tab"] {{
    background: rgba(233,228,214,0.05);
    border-radius: 100px; padding: 8px 16px; color:{INK_DIM};
    border:1px solid rgba(233,228,214,0.12);
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {GOLD}, {GOLD_LIGHT}) !important;
    color:{NAVY} !important; font-weight:700;
}}

.stButton>button {{
    background: linear-gradient(135deg, {TEAL}, #2f6f7c);
    color:#eafcff; border:none; border-radius:10px; font-weight:700;
    padding:10px 18px; width:100%;
}}
.stButton>button:hover {{ filter:brightness(1.12); color:#eafcff; }}

[data-testid="stMetric"] {{
    background: linear-gradient(180deg, rgba(233,228,214,0.035), rgba(233,228,214,0.015));
    border:1px solid rgba(233,228,214,0.10); border-radius:14px; padding:14px 18px;
}}
[data-testid="stMetricLabel"] {{ color:{INK_DIM} !important; }}
[data-testid="stMetricValue"] {{ color:{GOLD_LIGHT} !important; direction:ltr; }}

.stChatMessage {{ direction: rtl; }}

.scx-conn-ok {{ color:{GREEN}; font-size:12px; font-weight:700; }}
.scx-conn-off {{ color:{GOLD_LIGHT}; font-size:12px; font-weight:700; }}

hr {{ border-color: rgba(233,228,214,0.12); }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER (با لوگوی رسمی SCOCOEX Global Week)
# ============================================================
def _logo_b64():
    try:
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

_logo = _logo_b64()
_logo_html = f'<img src="data:image/png;base64,{_logo}">' if _logo else "<h1 style='margin:0;'>SCOCOEX</h1>"

st.markdown(f"""
<div class="scx-header">
    <div>
        {_logo_html}
        <div class="scx-sub">دموی مفهومی — موتور تطبیق، دستیار هوشمند، ثبت‌نام و داشبورد مدیریتی</div>
    </div>
    <div class="scx-badge">نسخه دمو · Streamlit</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# DATA — matching engine mock data
# ============================================================
COMPANIES = {
    "شرکت فولاد مبارکه اصفهان": {
        "sector": "فولاد و زنجیره ارزش",
        "meta": ["بزرگ‌ترین صادرکننده فولاد ایران", "ظرفیت تولید: ~۱۰ میلیون تن/سال", "محصولات: ورق گرم و سرد، اسلب"],
        "matches": [
            {"name": "Ma'aden", "country": "عربستان سعودی", "tag": "معدن و فولاد", "score": 94,
             "reason": "هر دو در زنجیره فولاد و مواد اولیه معدنی فعال هستند؛ ظرفیت صادراتی مبارکه دقیقاً با نیاز واردات فولادی معادن هدف همخوانی دارد."},
            {"name": "Oman Steel Company", "country": "عمان", "tag": "فولاد", "score": 88,
             "reason": "نزدیکی جغرافیایی و نیاز عمان به واردات محصولات فولادی برای پروژه‌های زیرساختی بندری."},
            {"name": "Emirates Steel Arkan", "country": "امارات متحده عربی", "tag": "فولاد", "score": 81,
             "reason": "بازار در حال رشد ساخت‌وساز امارات؛ فرصت همکاری در محصولات پایین‌دستی فولاد."},
        ],
    },
    "شرکت ملی صنایع مس ایران": {
        "sector": "صنعت مس و فلزات",
        "meta": ["بزرگ‌ترین تولیدکننده مس ایران", "محصولات: کاتد مس، مفتول مس، کنسانتره", "هدف: توسعه صادرات به GCC"],
        "matches": [
            {"name": "Vale Oman", "country": "عمان", "tag": "معدن و فلزات", "score": 91,
             "reason": "حضور فعال در منطقه صنعتی صحار؛ نیاز به تأمین مواد اولیه مسی برای صنایع پایین‌دستی."},
            {"name": "MDO (Minerals Development Oman)", "country": "عمان", "tag": "سرمایه‌گذاری معدنی", "score": 86,
             "reason": "سیاست توسعه معدن عمان با هدف تنوع اقتصادی؛ فرصت مشارکت در پروژه‌های اکتشاف مشترک."},
            {"name": "Jindal Shadeed", "country": "عمان", "tag": "فولاد و فلزات", "score": 77,
             "reason": "زنجیره تأمین مشترک در صنایع فلزی منطقه صحار."},
        ],
    },
    "صنایع پتروشیمی خلیج فارس": {
        "sector": "صنعت نفت، گاز و پتروشیمی",
        "meta": ["بزرگ‌ترین هلدینگ پتروشیمی ایران", "محصولات: پلیمر، مواد اولیه شیمیایی", "بازار هدف: صادرات به آسیا و آفریقا"],
        "matches": [
            {"name": "OQ", "country": "عمان", "tag": "نفت، گاز و پتروشیمی", "score": 92,
             "reason": "عمان در حال توسعه زیرساخت LNG و پتروپالایشگاهی؛ فرصت تأمین خوراک و همکاری فنی."},
            {"name": "QatarEnergy", "country": "قطر", "tag": "انرژی", "score": 83,
             "reason": "بازیگر اصلی منطقه در پروژه‌های جدید پتروشیمی با نیاز به شرکای فناوری."},
            {"name": "SABIC", "country": "عربستان سعودی", "tag": "پتروشیمی", "score": 79,
             "reason": "همپوشانی در محصولات پلیمری و پایین‌دستی شیمیایی."},
        ],
    },
    "گروه مپنا": {
        "sector": "مهندسی، ساخت، فناوری‌های انرژی و نیروگاه‌ها",
        "meta": ["سازنده توربین، ژنراتور و تجهیزات نیروگاهی", "تجربه اجرای پروژه‌های EPC بزرگ", "هدف: صادرات خدمات فنی و مهندسی"],
        "matches": [
            {"name": "ACWA Power", "country": "عربستان سعودی", "tag": "توسعه‌دهنده نیروگاه", "score": 90,
             "reason": "در حال اجرای پروژه‌های بزرگ نیروگاهی منطقه؛ نیاز به شرکای EPC و تجهیزات دوار."},
            {"name": "Nama Group / Hydrom", "country": "عمان", "tag": "برق و انرژی", "score": 85,
             "reason": "مسئول توسعه شبکه انتقال برق و پروژه‌های هیدروژن سبز عمان."},
            {"name": "Masdar", "country": "امارات متحده عربی", "tag": "انرژی تجدیدپذیر", "score": 74,
             "reason": "فرصت همکاری در پروژه‌های انرژی خورشیدی و بادی مشترک."},
        ],
    },
}

ANSWERS_FA = {
    "جلسات b2b صنعت فولاد کی برگزار می‌شود؟": "بر اساس برنامه فعلی، جلسات B2B صنعت فولاد و زنجیره ارزش در روز اول اجلاس (۱۳ می) با حدود ۲۰ تا ۳۰ شرکت هدف از جمله فولاد مبارکه، Ma'aden و Oman Steel برنامه‌ریزی شده است.",
    "کدام شرکت‌های عمانی در حوزه معدن حضور دارند؟": "شرکت‌های اصلی عمانی حاضر در حوزه معدن: Minerals Development Oman (MDO)، Oman Mining Company، Gulf Mining Group، Vale Oman و Sohar Aluminium.",
    "برای ثبت‌نام غرفه باید چه کار کنم؟": "برای رزرو غرفه لازم است فرم «ثبت‌نام شرکت‌ها» را در همین اپ تکمیل کنید؛ تیم مدیر نمایشگاه و فروش غرفه ظرف ۴۸ ساعت با شما تماس خواهد گرفت.",
}
ANSWERS_EN = {
    "which sectors have the most b2b sessions?": "Based on the current schedule, Steel & Mining and Oil, Gas & Petrochemicals have the highest number of pre-arranged B2B sessions, followed by Engineering & Energy.",
    "who are the main saudi steel companies attending?": "The main Saudi steel companies confirmed are Ma'aden and Saudi Iron and Steel Company (Hadeed).",
    "how can i request a booth?": "You can request a booth by filling out the 'Company Registration' form in this app; the exhibition & booth sales team will follow up within 48 hours.",
}

SECTOR_DEMO_COUNTS = [
    ("فولاد و زنجیره ارزش", 38), ("معادن: سنگ‌آهن، آلومینیوم و صنایع معدنی", 31),
    ("صنعت نفت، گاز و پتروشیمی", 44), ("مهندسی، ساخت، فناوری‌های انرژی و نیروگاه‌ها", 27),
    ("بانک‌ها، صندوق‌های ثروت ملی و سرمایه‌گذاری", 22), ("فناوری‌های نوین، هوش مصنوعی و بلاک‌چین", 19),
    ("صنایع غذایی، کشاورزی و امنیت غذایی", 17), ("صنایع دارویی، پزشکی و سلامت", 16),
]

TASKS = [
    ("done", "تأیید نهایی لیست ۳۰ شرکت هدف صنعت فولاد و معدن", "تکمیل‌شده — ۲ روز پیش"),
    ("pending", "هماهنگی جلسه هسته مدیریتی با دبیرکل و مدیر PMO", "در انتظار پاسخ — ۱ روز پیش"),
    ("pending", "ارسال دعوت‌نامه رسمی به Ma'aden و ACWA Power", "در حال پیگیری"),
    ("risk", "تأخیر در تأیید ۶ اسپانسر باقی‌مانده", "نیاز به پیگیری فوری"),
    ("done", "راه‌اندازی نسخه اول موتور تطبیق B2B", "تکمیل‌شده — امروز"),
]
DOT_COLOR = {"done": GREEN, "pending": GOLD_LIGHT, "risk": RED}

# ============================================================
# GOOGLE SHEETS — اتصال اختیاری. اگر Secrets تنظیم نشده باشد،
# اپ بدون خطا روی یک فایل CSV محلی fallback می‌کند تا دمو همیشه کار کند.
# ============================================================
@st.cache_resource(show_spinner=False)
def _get_gsheet_worksheet():
    """
    برای فعال‌سازی واقعی:
    1) یک Service Account در Google Cloud بساز و کلید JSON آن را بگیر.
    2) شیت گوگل مقصد را با ایمیل client_email آن سرویس‌اکانت Share کن (نقش Editor).
    3) در Streamlit Cloud → Settings → Secrets این ساختار را اضافه کن:

        gsheet_key = "SPREADSHEET_ID_or_URL"

        [gcp_service_account]
        type = "service_account"
        project_id = "..."
        private_key_id = "..."
        private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
        client_email = "...@...iam.gserviceaccount.com"
        client_id = "..."
        token_uri = "https://oauth2.googleapis.com/token"
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        creds_dict = dict(st.secrets["gcp_service_account"])
        sheet_key = st.secrets["gsheet_key"]
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        sh = client.open_by_key(sheet_key) if len(sheet_key) < 100 else client.open_by_url(sheet_key)
        try:
            ws = sh.worksheet("registrations")
        except gspread.WorksheetNotFound:
            ws = sh.add_worksheet(title="registrations", rows=1000, cols=len(REG_COLUMNS))
            ws.append_row(REG_COLUMNS)
        return ws
    except Exception:
        return None  # اتصال تنظیم نشده یا خطا — fallback به CSV محلی


def is_gsheet_connected() -> bool:
    return _get_gsheet_worksheet() is not None


def save_registration(record: dict):
    """ثبت یک شرکت جدید — ابتدا تلاش برای Google Sheets، در غیر این صورت CSV محلی."""
    row = [record.get(c, "") for c in REG_COLUMNS]
    ws = _get_gsheet_worksheet()
    if ws is not None:
        try:
            ws.append_row(row)
            return "gsheet"
        except Exception:
            pass
    df_row = pd.DataFrame([row], columns=REG_COLUMNS)
    if os.path.exists(LOCAL_CSV_FALLBACK):
        df_row.to_csv(LOCAL_CSV_FALLBACK, mode="a", header=False, index=False)
    else:
        df_row.to_csv(LOCAL_CSV_FALLBACK, mode="w", header=True, index=False)
    return "local"


@st.cache_data(ttl=15, show_spinner=False)
def load_registrations() -> pd.DataFrame:
    ws = _get_gsheet_worksheet()
    if ws is not None:
        try:
            records = ws.get_all_records()
            if records:
                return pd.DataFrame(records)
            return pd.DataFrame(columns=REG_COLUMNS)
        except Exception:
            pass
    if os.path.exists(LOCAL_CSV_FALLBACK):
        return pd.read_csv(LOCAL_CSV_FALLBACK)
    return pd.DataFrame(columns=REG_COLUMNS)


# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 موتور تطبیق B2B",
    "💬 دستیار هوشمند",
    "📊 داشبورد مدیریتی",
    "📝 ثبت‌نام شرکت‌ها",
    "🔐 پنل مدیریت",
])

# ------------------------------------------------------------
# TAB 1 — MATCHING ENGINE
# ------------------------------------------------------------
with tab1:
    st.markdown("#### موتور هوشمند تطبیق B2B")
    st.markdown(
        f"<p style='color:{INK_DIM}; font-size:14px;'>یک شرکت ایرانی را انتخاب کنید تا موتور تطبیق، "
        "بهترین طرف‌های مقابل را از میان شرکت‌های هدف اجلاس عمان با امتیاز و دلیل پیشنهاد دهد.</p>",
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        company_name = st.selectbox("شرکت ایرانی", list(COMPANIES.keys()))
        c = COMPANIES[company_name]
        st.markdown(f"""
        <div class="scx-card">
            <div class="scx-tag">{c['sector']}</div>
            <div style="font-size:12.8px; color:{INK_DIM}; margin-top:8px; line-height:2;">
                {"<br>".join(c['meta'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        run = st.button("▸ اجرای تطبیق هوشمند", key="run_match")

    with col_right:
        if run:
            with st.spinner("در حال تحلیل پروفایل و تطبیق…"):
                time.sleep(0.9)
            for m in c["matches"]:
                gcol1, gcol2 = st.columns([1, 4])
                with gcol1:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=m["score"],
                        number={"suffix": "٪", "font": {"size": 20, "color": GOLD_LIGHT}},
                        gauge={
                            "axis": {"range": [0, 100], "visible": False},
                            "bar": {"color": GOLD, "thickness": 0.85},
                            "bgcolor": "rgba(233,228,214,0.08)",
                            "borderwidth": 0,
                        },
                    ))
                    fig.update_layout(
                        height=110, margin=dict(l=6, r=6, t=6, b=6),
                        paper_bgcolor="rgba(0,0,0,0)", font={"color": INK},
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                with gcol2:
                    st.markdown(f"""
                    <div class="scx-card" style="margin-bottom:8px;">
                        <div class="scx-tag">{m['country']} · {m['tag']}</div>
                        <div class="scx-name">{m['name']}</div>
                        <div class="scx-reason">{m['reason']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.button(f"پیشنهاد جلسه B2B با {m['name']}", key=f"btn_{m['name']}")
        else:
            st.markdown(f"""
            <div style="text-align:center; padding:60px 20px; color:{INK_DIM};
                        border:1px dashed rgba(233,228,214,0.15); border-radius:14px;">
                برای مشاهده پیشنهادهای تطبیق، «اجرای تطبیق هوشمند» را در سمت راست بزنید.
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------
# TAB 2 — MULTILINGUAL ASSISTANT
# ------------------------------------------------------------
with tab2:
    st.markdown("#### دستیار هوشمند چندزبانه")
    st.markdown(
        f"<p style='color:{INK_DIM}; font-size:14px;'>دستیاری برای پاسخ به سؤالات شرکت‌کنندگان درباره "
        "برنامه، شرکت‌های حاضر و جلسات B2B — به فارسی و انگلیسی.</p>",
        unsafe_allow_html=True,
    )

    lang = st.radio("زبان", ["فارسی", "English"], horizontal=True, label_visibility="collapsed")
    is_fa = lang == "فارسی"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "text_fa": "سلام! من دستیار هوشمند اسکوکواکس هستم. درباره برنامه، شرکت‌ها یا جلسات B2B بپرسید.",
             "text_en": "Hi! I'm the SCOCOEX AI assistant. Ask about the agenda, companies, or B2B sessions."}
        ]

    suggestion_labels_fa = ["جلسات B2B صنعت فولاد کی برگزار می‌شود؟", "کدام شرکت‌های عمانی در حوزه معدن حضور دارند؟", "برای ثبت‌نام غرفه باید چه کار کنم؟"]
    suggestion_labels_en = ["Which sectors have the most B2B sessions?", "Who are the main Saudi steel companies attending?", "How can I request a booth?"]
    labels = suggestion_labels_fa if is_fa else suggestion_labels_en

    scol1, scol2 = st.columns([1, 2], gap="large")
    with scol1:
        st.markdown("**سؤالات پیشنهادی**" if is_fa else "**Suggested questions**")
        picked = None
        for lbl in labels:
            if st.button(lbl, key=f"sugg_{lbl}"):
                picked = lbl

    with scol2:
        chat_container = st.container(height=380)
        with chat_container:
            for msg in st.session_state.chat_history:
                text = msg.get("text_fa") if is_fa else msg.get("text_en", msg.get("text_fa"))
                with st.chat_message(msg["role"]):
                    st.write(text)

        user_input = st.chat_input("سؤال خود را بنویسید…" if is_fa else "Type your question…")

        q = picked or user_input
        if q:
            st.session_state.chat_history.append({"role": "user", "text_fa": q, "text_en": q})
            bank = ANSWERS_FA if is_fa else ANSWERS_EN
            answer = bank.get(q.strip().lower())
            if not answer:
                answer = ("این یک نسخه دمو است — در نسخه نهایی، پاسخ از پایگاه‌داده کامل شرکت‌ها و برنامه اجلاس تولید می‌شود."
                           if is_fa else
                           "This is a demo — in the final version, the answer is generated from the full company and agenda database.")
            st.session_state.chat_history.append({"role": "assistant", "text_fa": answer, "text_en": answer})
            st.rerun()

# ------------------------------------------------------------
# TAB 3 — MANAGEMENT DASHBOARD
# ------------------------------------------------------------
with tab3:
    st.markdown("#### داشبورد مدیریتی زنده")
    st.markdown(
        f"<p style='color:{INK_DIM}; font-size:14px;'>نمای کلی وضعیت اجلاس برای هسته مدیریتی — "
        "ثبت‌نام، جلسات B2B، اسپانسرها و پیشرفت اجرایی.</p>",
        unsafe_allow_html=True,
    )

    regs = load_registrations()
    real_reg_count = len(regs)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("شرکت ثبت‌نام‌شده", f"{214 + real_reg_count:,}", "۱۲٪ نسبت به هفته قبل")
    k2.metric("جلسات B2B برنامه‌ریزی‌شده", "۶۸", "۸٪")
    k3.metric("اسپانسر تأییدشده", "۱۹", "در انتظار ۶ مورد", delta_color="off")
    k4.metric("پیشرفت آماده‌سازی کلی", "۴۲٪", "۴ ماه تا رویداد", delta_color="off")

    st.markdown("<br>", unsafe_allow_html=True)
    dcol1, dcol2 = st.columns([1.3, 1], gap="large")

    with dcol1:
        st.markdown("**ثبت‌نام به تفکیک صنعت (۱۰ صنعت رسمی اسکوکواکس)**")
        labels = [s[0] for s in SECTOR_DEMO_COUNTS][::-1]
        values = [s[1] for s in SECTOR_DEMO_COUNTS][::-1]
        fig = go.Figure(go.Bar(
            x=values, y=labels, orientation="h",
            marker=dict(color=GOLD, line=dict(width=0)),
        ))
        fig.update_layout(
            height=320, margin=dict(l=0, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=INK_DIM, size=12),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=False, autorange="reversed"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with dcol2:
        st.markdown("**وضعیت اجرایی این هفته**")
        for status, t, s in TASKS:
            color = DOT_COLOR[status]
            st.markdown(f"""
            <div style="display:flex; gap:10px; padding:9px 0; border-bottom:1px solid rgba(233,228,214,0.06);">
                <div style="width:8px; height:8px; border-radius:50%; background:{color}; margin-top:5px; flex-shrink:0;"></div>
                <div>
                    <div style="font-size:12.8px; color:{INK};">{t}</div>
                    <div style="font-size:11.5px; color:{INK_DIM};">{s}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------
# TAB 4 — PUBLIC REGISTRATION FORM  (→ Google Sheets)
# ------------------------------------------------------------
with tab4:
    st.markdown("#### ثبت‌نام شرکت‌ها")
    conn_ok = is_gsheet_connected()
    conn_html = ('<span class="scx-conn-ok">● متصل به Google Sheets</span>' if conn_ok
                 else '<span class="scx-conn-off">● Google Sheets متصل نیست — فعلاً ذخیره محلی (CSV)</span>')
    st.markdown(f"<p style='font-size:12px;'>{conn_html}</p>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:{INK_DIM}; font-size:14px;'>شرکت‌های علاقه‌مند به حضور در اجلاس، اطلاعات خود را از "
        "اینجا ثبت می‌کنند. هر ثبت‌نام بر اساس «صنعت» تگ می‌شود تا در پنل مدیریت به‌سرعت قابل جست‌وجو و فیلتر باشد.</p>",
        unsafe_allow_html=True,
    )

    with st.form("reg_form", clear_on_submit=True):
        rc1, rc2 = st.columns(2)
        with rc1:
            f_name = st.text_input("نام شرکت *")
            f_country = st.text_input("کشور *")
            f_sector = st.selectbox("صنعت *", SECTORS)
        with rc2:
            f_contact = st.text_input("نام رابط")
            f_email = st.text_input("ایمیل")
            f_phone = st.text_input("تلفن")
        f_note = st.text_area("توضیحات (محصولات، اهداف همکاری و…)", height=90)

        submitted = st.form_submit_button("▸ ثبت اطلاعات شرکت")
        if submitted:
            if not f_name or not f_country:
                st.warning("لطفاً حداقل نام شرکت، کشور و صنعت را وارد کنید.")
            else:
                record = {
                    "زمان ثبت": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "نام شرکت": f_name, "کشور": f_country, "صنعت": f_sector,
                    "نام رابط": f_contact, "ایمیل": f_email, "تلفن": f_phone, "توضیحات": f_note,
                }
                dest = save_registration(record)
                load_registrations.clear()
                if dest == "gsheet":
                    st.success("ثبت‌نام با موفقیت در Google Sheets ذخیره شد. ✅")
                else:
                    st.info("ثبت‌نام محلی ذخیره شد (Google Sheets هنوز متصل نیست — راهنما در README).")

# ------------------------------------------------------------
# TAB 5 — ADMIN PANEL (protected)
# ------------------------------------------------------------
with tab5:
    st.markdown("#### پنل مدیریت")

    if "admin_ok" not in st.session_state:
        st.session_state.admin_ok = False

    if not st.session_state.admin_ok:
        st.markdown(f"<p style='color:{INK_DIM}; font-size:13px;'>این بخش فقط برای هسته مدیریتی است.</p>", unsafe_allow_html=True)
        pwd = st.text_input("رمز عبور مدیریت", type="password")
        if st.button("ورود"):
            admin_pwd = st.secrets.get("admin_password", "demo1234")
            if pwd == admin_pwd:
                st.session_state.admin_ok = True
                st.rerun()
            else:
                st.error("رمز عبور نادرست است.")
        st.caption("رمز پیش‌فرض نسخه دمو: `demo1234` — حتماً پیش از استفاده واقعی آن را در Secrets تغییر دهید.")
    else:
        top1, top2 = st.columns([4, 1])
        with top1:
            conn_ok = is_gsheet_connected()
            conn_html = ('<span class="scx-conn-ok">● اتصال Google Sheets فعال است</span>' if conn_ok
                         else '<span class="scx-conn-off">● اتصال Google Sheets تنظیم نشده — نمایش داده‌های محلی</span>')
            st.markdown(f"<p style='font-size:12.5px;'>{conn_html}</p>", unsafe_allow_html=True)
        with top2:
            if st.button("خروج"):
                st.session_state.admin_ok = False
                st.rerun()

        regs = load_registrations()

        st.markdown("**جست‌وجو و فیلتر بر اساس صنعت**")
        fcol1, fcol2, fcol3 = st.columns([2, 2, 1])
        with fcol1:
            sector_filter = st.multiselect("فیلتر صنعت", SECTORS, default=[])
        with fcol2:
            text_query = st.text_input("جست‌وجو (نام شرکت / کشور / رابط)")
        with fcol3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 بروزرسانی"):
                load_registrations.clear()
                st.rerun()

        filtered = regs.copy()
        if not filtered.empty:
            if sector_filter:
                filtered = filtered[filtered["صنعت"].isin(sector_filter)]
            if text_query:
                q = text_query.strip().lower()
                mask = filtered.apply(lambda r: q in str(r.get("نام شرکت", "")).lower()
                                       or q in str(r.get("کشور", "")).lower()
                                       or q in str(r.get("نام رابط", "")).lower(), axis=1)
                filtered = filtered[mask]

        st.markdown(f"<p style='font-size:12.5px; color:{INK_DIM};'>{len(filtered)} نتیجه از {len(regs)} ثبت‌نام کل</p>", unsafe_allow_html=True)
        st.dataframe(filtered, use_container_width=True, height=320)

        if not regs.empty:
            st.markdown("**تعداد ثبت‌نام‌ها به تفکیک صنعت**")
            counts = regs["صنعت"].value_counts().reindex(SECTORS).fillna(0)
            fig2 = go.Figure(go.Bar(
                x=counts.values, y=counts.index, orientation="h",
                marker=dict(color=TEAL),
            ))
            fig2.update_layout(
                height=300, margin=dict(l=0, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=INK_DIM, size=11),
                xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

            csv_bytes = filtered.to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇ خروجی CSV از نتایج فیلترشده", data=csv_bytes,
                                file_name="scocoex_registrations.csv", mime="text/csv")
        else:
            st.info("هنوز هیچ ثبت‌نامی وجود ندارد. از تب «ثبت‌نام شرکت‌ها» یک رکورد آزمایشی اضافه کنید.")

st.markdown(f"<p style='text-align:center; color:{INK_DIM}; font-size:11px; opacity:.6; margin-top:30px;'>"
            "SCOCOEX AI Core — نمونه اولیه مفهومی برای نمایش قابلیت‌ها · داده‌های تطبیق/داشبورد نمایشی هستند</p>",
            unsafe_allow_html=True)
