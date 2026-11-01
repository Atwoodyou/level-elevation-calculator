
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="水準儀高程計算機",
    page_icon="📐",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
div[data-testid="stMetric"] {
    background: #f1f5f9;
    border-radius: 10px;
    padding: 15px;
}
div[data-testid="stMetricLabel"] {
    color: #334155;
}
div[data-testid="stMetricValue"] {
    color: #0f172a;
}
</style>
""", unsafe_allow_html=True)

st.title("📐 水準儀高程計算機")
st.caption("施工測量｜基準點 GL｜後視讀尺｜前視讀尺｜設計高程")

left, right = st.columns([1, 1.1], gap="large")

with left:
    st.subheader("① 測量資料輸入")

    bm_gl = st.number_input(
        "基準點 BN GL（cm）",
        value=120.0,
        step=1.0,
        format="%.2f"
    )

    back_read = st.number_input(
        "基準點讀尺／後視（cm）",
        min_value=0.0,
        value=150.0,
        step=1.0,
        format="%.2f"
    )

    front_read = st.number_input(
        "目標點讀尺／前視（cm）",
        min_value=0.0,
        value=180.0,
        step=1.0,
        format="%.2f"
    )

    design_gl = st.number_input(
        "設計高程 GL（cm）",
        value=90.0,
        step=1.0,
        format="%.2f"
    )

# 高程計算
instrument_gl = bm_gl + back_read
target_gl = instrument_gl - front_read
design_read = instrument_gl - design_gl
difference = target_gl - design_gl

def gl_text(value):
    if value > 0:
        return f"GL +{value:,.2f} cm"
    if value < 0:
        return f"GL {value:,.2f} cm"
    return "GL 0.00 cm"

with right:
    st.subheader("② 自動計算結果")

    st.metric(
        "水準儀視準線高程",
        gl_text(instrument_gl)
    )

    st.metric(
        "目標點實際高程",
        gl_text(target_gl)
    )

    st.metric(
        "設計高程應讀尺數",
        f"{design_read:,.2f} cm"
    )

    st.metric(
        "實際與設計高程差",
        f"{difference:+,.2f} cm"
    )

    if abs(difference) < 0.005:
        st.success("✅ 目標點已達設計高程")
    elif difference > 0:
        st.warning(
            f"目標點高於設計高程 {difference:.2f} cm"
        )
    else:
        st.info(
            f"目標點低於設計高程 {abs(difference):.2f} cm"
        )

st.divider()
st.subheader("③ 水準儀測量示意圖")

# HTML SVG 施工示意圖
diagram = f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<style>
body {{
    font-family: Arial, "Microsoft JhengHei", sans-serif;
    margin: 0;
    background: white;
}}
svg {{
    width: 100%;
    height: auto;
}}
</style>
</head>
<body>
<svg viewBox="0 0 900 340"
 xmlns="http://www.w3.org/2000/svg">

<rect width="900" height="340" fill="#f8fafc"/>

<!-- 地面 -->
<path d="M0 265 H900 V340 H0 Z"
 fill="#e5cfac"/>
<line x1="0" y1="265" x2="900" y2="265"
 stroke="#9a7449" stroke-width="3"/>

<!-- 視準線 -->
<line x1="75" y1="88" x2="825" y2="88"
 stroke="#2563eb" stroke-width="3"
 stroke-dasharray="10 7"/>

<!-- 基準點尺 -->
<rect x="185" y="88" width="18" height="177"
 fill="white" stroke="#334155" stroke-width="2"/>

<!-- 目標點尺 -->
<rect x="705" y="88" width="18" height="177"
 fill="white" stroke="#334155" stroke-width="2"/>

<!-- 水準儀 -->
<rect x="424" y="78" width="65" height="19"
 rx="5" fill="#2563eb"/>
<circle cx="456" cy="105" r="8" fill="#475569"/>
<line x1="456" y1="113" x2="456" y2="190"
 stroke="#475569" stroke-width="5"/>
<line x1="456" y1="190" x2="415" y2="265"
 stroke="#475569" stroke-width="5"/>
<line x1="456" y1="190" x2="497" y2="265"
 stroke="#475569" stroke-width="5"/>

<!-- 標示文字 -->
<g fill="#0f172a" font-size="19">
<text x="75" y="40">
視準線：{gl_text(instrument_gl)}
</text>
<text x="105" y="293">
基準點 BN：{gl_text(bm_gl)}
</text>
<text x="600" y="293">
目標點：{gl_text(target_gl)}
</text>
<text x="393" y="308">水準儀</text>
</g>

<g font-size="17" fill="#1d4ed8">
<text x="105" y="140">
後視 {back_read:.2f} cm
</text>
<text x="734" y="140">
前視 {front_read:.2f} cm
</text>
</g>

</svg>
</body>
</html>
"""

components.html(diagram, height=350, scrolling=False)

st.caption(
    "示意圖僅說明測量關係，不代表實際高程比例。"
)

st.divider()
st.subheader("④ 計算公式")

st.code(
    "視準線高程 = 基準點 GL + 後視讀尺\n"
    "目標點高程 = 視準線高程 - 前視讀尺\n"
    "設計高程應讀尺 = 視準線高程 - 設計 GL\n"
    "高程差 = 目標點實際高程 - 設計高程",
    language="text"
)

st.caption(
    "單位統一使用 cm。"
    "GL 負值請直接輸入負號，不需要額外括號。"
)

