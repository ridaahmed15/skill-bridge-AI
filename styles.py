CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root{--ink:#0E0E12;--muted:#8A8D9A;--line:#E7E9F3;--lav:#ECEEFF;--peri:#A3B4FF;--green:#06D6A0;--purple:#8B4DFF;
--yellow:#F7BE0B;--pink:#F8D7FB;--butter:#FBF6A8;--blue:#1B5CFF;--orange:#FF7A1A;--grey:#F3F3F5}
html,body,.stApp,[class*="css"],button,input,textarea,select{font-family:'Plus Jakarta Sans','Segoe UI',system-ui,sans-serif !important}
.stApp{background:var(--peri)}
#MainMenu,footer{visibility:hidden}
header[data-testid="stHeader"]{background:transparent}
.block-container{background:#fff;border-radius:30px;max-width:1560px;padding:1.8rem 2.4rem 2.6rem !important;margin:1rem auto 1.4rem;box-shadow:0 24px 70px rgba(40,50,140,.28)}
h1,h2,h3{font-weight:800 !important;letter-spacing:-.02em;color:var(--ink)}
h1{font-size:2.3rem !important;margin:.4rem 0 .2rem !important;padding:0 !important}
.sub{color:var(--muted);font-weight:500;margin:-.2rem 0 1.2rem}
.sec{display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:1.05rem;margin:1.6rem 0 .8rem}

/* sidebar */
section[data-testid="stSidebar"]{background:var(--lav);border-right:none}
section[data-testid="stSidebar"] > div{padding-top:1rem}
.brand{display:flex;align-items:center;gap:.6rem;font-weight:800;font-size:1.45rem;margin:.2rem 0 1rem}
.brand i{width:34px;height:34px;border-radius:11px;background:var(--ink);display:inline-flex;align-items:center;justify-content:center;color:#fff;font-style:normal;font-size:1.1rem}
section[data-testid="stSidebar"] div[role="radiogroup"]{gap:.2rem}
section[data-testid="stSidebar"] div[role="radiogroup"] label{padding:.72rem 1rem;border-radius:18px;width:100%;cursor:pointer;transition:background .15s}
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child{display:none}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{background:rgba(255,255,255,.6)}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:#fff;box-shadow:0 2px 10px rgba(60,70,160,.12)}
section[data-testid="stSidebar"] div[role="radiogroup"] label p{font-size:1.02rem;font-weight:600;color:var(--ink)}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{font-weight:800}
.pro{position:relative;background:linear-gradient(180deg,#FAF7A5,#FFFDE0);border-radius:26px;padding:1.4rem 1rem 1rem;text-align:center;margin:1.2rem 0 .6rem;overflow:hidden}
.pro .gem{position:absolute;top:-14px;left:26px;width:46px;height:46px;background:#BDE88B;border-radius:12px;transform:rotate(25deg)}
.pro .pill{position:absolute;top:6px;right:22px;width:62px;height:24px;background:#F59AF4;border-radius:999px;transform:rotate(-18deg)}
.pro .cyl{position:absolute;top:30px;left:14px;width:34px;height:52px;background:#F2C230;border-radius:16px;transform:rotate(35deg)}
.pro h4{margin:3rem 0 .3rem;font-size:1.45rem;font-weight:800}
.pro p{margin:0 0 .6rem;font-size:.82rem;font-weight:500}
.pro .rate{display:inline-block;background:#F2F23A;border-radius:8px;padding:.1rem .5rem;font-weight:700;font-size:.85rem}

/* cards (containers keyed card_*) */
div[class*="st-key-card"]{background:#fff;border:1.5px solid var(--line);border-radius:26px;padding:1.3rem 1.4rem}
div[class*="st-key-card_dark"]{background:#000;border-color:#000;color:#fff}
div[class*="st-key-card_pink"]{background:var(--pink);border-color:var(--pink)}
div[class*="st-key-card_lav"]{background:#DDE3FF;border-color:#DDE3FF}
div[class*="st-key-card_butter"]{background:var(--butter);border-color:var(--butter)}
div[class*="st-key-card_grey"]{background:var(--grey);border-color:var(--grey)}
div[class*="st-key-card_soft"]{background:linear-gradient(180deg,#F7F5FF,#fff)}
.ch{display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:1.02rem}
.big{font-size:4.6rem;font-weight:800;line-height:1;letter-spacing:-.04em;margin:.5rem 0 .2rem}
.big small{font-size:.9rem;font-weight:700;letter-spacing:0;margin-left:.4rem;vertical-align:middle}
.up{color:var(--green)}.down{color:var(--orange)}
.cap{color:var(--muted);font-weight:500;font-size:.95rem}
.flex{display:flex;justify-content:space-between;align-items:flex-end;gap:1rem}
.barrow{margin-bottom:.9rem}
.barhead{display:flex;justify-content:space-between;font-weight:600;font-size:.95rem;margin-bottom:.35rem}
.track{height:9px;border-radius:99px;background:#F0F0F4;overflow:hidden}
.fill{height:100%;border-radius:99px}
.tag{display:inline-block;border:1px solid currentColor;border-radius:8px;padding:.05rem .5rem;font-size:.78rem;font-weight:600;margin-right:.35rem;opacity:.85}
.chip{display:inline-block;background:var(--lav);border-radius:99px;padding:.2rem .75rem;font-size:.82rem;font-weight:700;margin:.15rem .25rem .15rem 0}
.chip.g{background:#D7F8EC;color:#047857}.chip.o{background:#FFE7D3;color:#B45309}.chip.p{background:#EBDDFF;color:#6D28D9}.chip.r{background:#FFDADA;color:#B91C1C}
.jobcard{background:#fff;color:var(--ink);border-radius:22px;padding:1rem 1.1rem;margin:.9rem 0}
.jobcard .logo{width:42px;height:42px;border-radius:12px;background:var(--lav);display:inline-flex;align-items:center;justify-content:center;font-weight:800;margin-right:.7rem}
.jobcard .t{font-weight:800;font-size:1.1rem;line-height:1.2}
.jobcard .m{color:var(--muted);font-weight:600;font-size:.85rem;margin-top:.5rem}
.cal{width:100%;border-collapse:separate;border-spacing:4px;text-align:center;font-weight:600;font-size:.9rem}
.cal th{color:var(--muted);font-weight:600;padding:.2rem 0}
.cal td{height:38px;border-radius:50%}
.cal td.out{color:#C4C6D2;background:#F6F6F9}
.cal td.in{background:#F5F5F8}
.cal td.ses{background:var(--ink);color:#fff}
.cal td.today{box-shadow:inset 0 0 0 2px var(--ink);background:#fff}
.big2{font-size:2.6rem;font-weight:800;letter-spacing:-.03em;margin:0}
.rec h3{font-size:1.5rem !important;margin:.6rem 0 .3rem !important}
.avatar{width:46px;height:46px;border-radius:50%;background:#FBEF5B;display:inline-flex;align-items:center;justify-content:center;font-weight:800;position:relative}
.avatar b{position:absolute;top:-6px;right:-8px;background:var(--ink);color:#fff;font-size:.65rem;border-radius:99px;padding:.1rem .35rem}
.note{background:#F6F4FF;border-left:5px solid var(--purple);border-radius:14px;padding:.8rem 1rem;font-size:.9rem;font-weight:500;margin:.6rem 0}

/* controls */
.stButton>button,.stDownloadButton>button,div[data-testid="stFormSubmitButton"]>button{border-radius:999px;font-weight:700;border:1.5px solid var(--ink);background:#fff;color:var(--ink);padding:.5rem 1.3rem;transition:all .15s}
.stButton>button:hover,.stDownloadButton>button:hover,div[data-testid="stFormSubmitButton"]>button:hover{background:var(--ink);color:#fff;border-color:var(--ink)}
.stButton>button[kind="primary"],div[data-testid="stFormSubmitButton"]>button[kind="primaryFormSubmit"]{background:var(--ink);color:#fff}
.stButton>button[kind="primary"]:hover{background:var(--purple);border-color:var(--purple)}
div[class*="st-key-card_dark"] .stButton>button{background:#2E2E32;color:#fff;border-color:#2E2E32}
div[class*="st-key-card_dark"] .stButton>button:hover{background:#fff;color:#000}
div[class*="st-key-lnk"] button{border:none !important;background:transparent !important;color:var(--blue) !important;padding:0 !important;font-weight:700;box-shadow:none}
div[class*="st-key-lnk"] button:hover{text-decoration:underline}
div[data-testid="stPopover"] > button{border-radius:999px;border:3px solid transparent;font-weight:700;background:linear-gradient(#fff,#fff) padding-box,linear-gradient(90deg,#8CF0B0,#FFD36E,#FF7AD9,#7B8CFF) border-box;color:var(--ink)}
.st-key-search div[data-baseweb="input"]{border-radius:999px;background:var(--grey);border:none}
.st-key-search input{padding-left:1rem}
div[data-baseweb="input"],div[data-baseweb="select"]>div,div[data-baseweb="textarea"]{border-radius:14px !important}
div[data-testid="stMetric"]{background:var(--grey);border-radius:20px;padding:1rem 1.2rem}
div[data-testid="stMetricValue"]{font-weight:800;letter-spacing:-.02em}
button[data-baseweb="tab"]{font-weight:700}
div[data-testid="stFileUploaderDropzone"]{border:2px dashed #A9C0FF;background:#F4F8FF;border-radius:20px}
div[data-testid="stDataFrame"]{border-radius:18px;overflow:hidden;border:1.5px solid var(--line)}
div[data-testid="stExpander"]{border-radius:18px;border:1.5px solid var(--line)}
@media (max-width:900px){.block-container{padding:1rem !important;border-radius:18px}.big{font-size:3.2rem}}
@media (prefers-reduced-motion:reduce){*{transition:none !important}}
"""
