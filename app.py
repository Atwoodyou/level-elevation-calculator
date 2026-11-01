import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="水準儀高程計算機", page_icon="📐", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
/* 手機優先：避免 Streamlit 預設的大字級、寬留白 */
.block-container {max-width: 1100px; padding-top: 1rem; padding-bottom: 2rem;}
#MainMenu, footer {visibility: hidden;}
.app-title {font-size: 1.65rem; font-weight: 750; line-height: 1.3; margin: .25rem 0 .3rem; color: var(--text-color);}
.app-caption {font-size: .88rem; color: #7b8493; margin-bottom: 1.25rem; line-height: 1.45;}
.section-title {font-size: 1.18rem; font-weight: 700; line-height: 1.35; margin: .4rem 0 1rem;}
/* 降低欄位、結果字級 */
div[data-testid="stNumberInput"] label p {font-size: .96rem !important;}
div[data-testid="stNumberInput"] input {font-size: 1rem !important; min-height: 2.45rem;}
div[data-testid="stNumberInput"] {margin-bottom: -.45rem;}
div[data-testid="stMetric"] {background: rgba(125, 139, 156, .09); border: 1px solid rgba(125,139,156,.14); border-radius: 10px; padding: .7rem .85rem;}
div[data-testid="stMetricLabel"] p {font-size: .88rem !important;}
div[data-testid="stMetricValue"] {font-size: 1.3rem !important;}
@media (max-width: 640px) {
    .block-container {padding: .65rem .85rem 2rem !important;}
    .app-title {font-size: 1.32rem !important; margin: .1rem 0 .25rem; white-space: nowrap;}
    .app-caption {font-size: .75rem !important; margin-bottom: .7rem;}
    .section-title {font-size: 1.03rem !important; margin: .35rem 0 .55rem;}
    div[data-testid="stNumberInput"] label p {font-size: .84rem !important;}
    div[data-testid="stNumberInput"] input {font-size: .95rem !important; min-height: 2.2rem;}
    div[data-testid="stMetric"] {padding: .55rem .7rem;}
    div[data-testid="stMetricLabel"] p {font-size: .79rem !important;}
    div[data-testid="stMetricValue"] {font-size: 1.1rem !important;}
    div[data-testid="stAlert"] p {font-size: .85rem !important;}
    div[data-testid="stVerticalBlock"] {gap: .5rem;}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="app-title">📐 水準儀高程計算機</div>', unsafe_allow_html=True)
st.markdown('<div class="app-caption">施工測量｜基準點 GL｜後視／前視讀尺｜設計高程</div>', unsafe_allow_html=True)

left, right = st.columns([1, 1.1], gap="large")

with left:
    st.markdown('<div class="section-title">① 測量資料輸入</div>', unsafe_allow_html=True)
    bm_gl = st.number_input("基準點 BN GL（cm）", value=120, step=1, format="%d")
    back_read = st.number_input("基準點讀尺／後視（cm）", min_value=0, value=150, step=1, format="%d")
    front_read = st.number_input("目標點讀尺／前視（cm）", min_value=0, value=180, step=1, format="%d")
    design_gl = st.number_input("設計高程 GL（cm）", value=90, step=1, format="%d")

instrument_gl = bm_gl + back_read
target_gl = instrument_gl - front_read
design_read = instrument_gl - design_gl
difference = target_gl - design_gl

def gl_text(value):
    if value > 0:
        return f"GL +{value:,d} cm"
    if value < 0:
        return f"GL {value:,d} cm"
    return "GL 0 cm"

with right:
    st.markdown('<div class="section-title">② 自動計算結果</div>', unsafe_allow_html=True)
    st.metric("水準儀視準線高程", gl_text(instrument_gl))
    st.metric("目標點實際高程", gl_text(target_gl))
    st.metric("設計高程應讀尺數", f"{design_read:,d} cm")
    st.metric("實際與設計高程差", f"{difference:+,d} cm")
    if difference == 0:
        st.success("✅ 目標點已達設計高程")
    elif difference > 0:
        st.warning(f"目標點高於設計高程 {difference:d} cm")
    else:
        st.info(f"目標點低於設計高程 {abs(difference):d} cm")

st.divider()
st.markdown('<div class="section-title">③ 水準儀測量示意圖</div>', unsafe_allow_html=True)

diagram = f"""
<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8"><style>
body{{font-family:Arial,'Microsoft JhengHei',sans-serif;margin:0;background:transparent;}}
svg{{width:100%;height:auto;display:block;}}
</style></head><body>
<svg viewBox="0 0 900 340" xmlns="http://www.w3.org/2000/svg">
<rect width="900" height="340" fill="#f8fafc" rx="12"/>
<path d="M0 265 H900 V340 H0 Z" fill="#e5cfac"/><path d="M0 265 H900" stroke="#9a7449" stroke-width="3"/>
<line x1="75" y1="88" x2="825" y2="88" stroke="#2563eb" stroke-width="3" stroke-dasharray="10 7"/>
<rect x="185" y="88" width="18" height="177" fill="white" stroke="#334155" stroke-width="2"/>
<rect x="705" y="88" width="18" height="177" fill="white" stroke="#334155" stroke-width="2"/>
<rect x="424" y="78" width="65" height="19" rx="5" fill="#2563eb"/>
<circle cx="456" cy="105" r="8" fill="#475569"/>
<path d="M456 113 V190 M456 190 L415 265 M456 190 L497 265" fill="none" stroke="#475569" stroke-width="5"/>
<g fill="#0f172a" font-size="19">
<text x="75" y="40">視準線：{gl_text(instrument_gl)}</text>
<text x="105" y="293">基準點 BN：{gl_text(bm_gl)}</text>
<text x="595" y="293">目標點：{gl_text(target_gl)}</text>
<text x="393" y="308">水準儀</text></g>
<g font-size="17" fill="#1d4ed8"><text x="105" y="140">後視 {back_read:d} cm</text>
<text x="734" y="140">前視 {front_read:d} cm</text></g>
</svg></body></html>"""
components.html(diagram, height=350, scrolling=False)
st.caption("示意圖僅說明測量關係，不代表實際高程比例。")
st.divider()
with st.expander("④ 查看計算公式"):
    st.code("視準線高程 = 基準點 GL + 後視讀尺\n目標點高程 = 視準線高程 - 前視讀尺\n設計高程應讀尺 = 視準線高程 - 設計 GL\n高程差 = 目標點實際高程 - 設計高程", language="text")
    st.caption("單位統一使用 cm。GL 負值請直接輸入負號，不需要額外括號。")
