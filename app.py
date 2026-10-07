from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="StayPredict AI | Hotel Cancellation Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

theme_col, toggle_col = st.columns([8, 1])
with toggle_col:
    light_mode = st.toggle("Light mode", value=st.session_state.theme == "light", key="light_mode")
    st.session_state.theme = "light" if light_mode else "dark"

is_light = st.session_state.theme == "light"


# -----------------------------
# Theme and reusable UI helpers
# -----------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --ink: #f6f7fb;
  --muted: #9aa4b8;
  --line: rgba(255,255,255,.10);
  --panel: rgba(16, 19, 32, .72);
  --violet: #9d7aff;
  --cyan: #59d9ff;
  --pink: #ff71c8;
  --bg: #070912;
}

html { scroll-behavior: smooth; }
@keyframes drift { 0%,100% { transform: translate3d(0,0,0) scale(1); } 50% { transform: translate3d(14px,-18px,0) scale(1.05); } }
@keyframes floatCard { 0%,100% { transform: rotate(2deg) translateY(0); } 50% { transform: rotate(0deg) translateY(-12px); } }
@keyframes pulseGlow { 0%,100% { opacity:.45; } 50% { opacity:1; } }
@keyframes scan { 0% { transform: translateX(-110%); } 100% { transform: translateX(420%); } }
@keyframes revealUp { from { opacity:0; transform:translateY(24px); } to { opacity:1; transform:translateY(0); } }
@keyframes marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }

.stApp {
  background:
    radial-gradient(circle at 82% 8%, rgba(111, 77, 255, .20), transparent 28rem),
    radial-gradient(circle at 8% 24%, rgba(34, 198, 255, .10), transparent 25rem),
    linear-gradient(135deg, #070912 0%, #0b0d18 54%, #090a13 100%);
  color: var(--ink);
  font-family: 'Manrope', sans-serif;
  overflow-x: hidden;
}
.stApp:before {
  content: '';
  position: fixed; inset: 0; pointer-events: none; opacity: .18;
  background-image: linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
  background-size: 72px 72px;
  mask-image: linear-gradient(to bottom, black, transparent 75%);
}
.block-container { max-width: 1240px; padding-top: 1.2rem; padding-bottom: 5rem; }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.navbar {
  position: sticky; top: 12px; z-index: 10; display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; margin-bottom: 70px; border: 1px solid var(--line); border-radius: 18px;
  background: rgba(9, 11, 22, .72); backdrop-filter: blur(20px); box-shadow: 0 16px 48px rgba(0,0,0,.22);
  animation: revealUp .7s ease both;
}
.brand { display: flex; align-items: center; gap: 11px; color: #fff; text-decoration: none; font-weight: 800; letter-spacing: -.03em; }
.brand small { display: block; color: #8892aa; font-size: .58rem; font-weight: 500; letter-spacing: .06em; margin-top: 2px; }
.logo { width: 32px; height: 32px; display: grid; place-items: center; border: 1px solid rgba(157,122,255,.75); border-radius: 10px; background: linear-gradient(145deg, rgba(157,122,255,.25), rgba(89,217,255,.12)); box-shadow: 0 0 24px rgba(157,122,255,.22); }
.navlinks { display: flex; align-items: center; gap: 24px; }
.navlinks a { color: #9ca5b8; text-decoration: none; font-size: .77rem; font-weight: 600; transition: color .2s ease; }
.navlinks a:hover { color: #fff; }
.navcta, .primary-link { color: #080911 !important; text-decoration: none; font-weight: 800; font-size: .78rem; padding: 11px 16px; border-radius: 999px; background: linear-gradient(100deg, #b8a2ff, #68dcff); box-shadow: 0 8px 28px rgba(112, 157, 255, .25); }

.eyebrow { display: inline-flex; align-items: center; gap: 8px; color: #b7a6ff; font: 500 .69rem 'DM Mono', monospace; letter-spacing: .09em; padding: 8px 12px; border: 1px solid rgba(157,122,255,.28); border-radius: 99px; background: rgba(157,122,255,.08); }
.eyebrow i { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #7bffca; box-shadow: 0 0 12px #7bffca; }
.hero { position:relative; padding: 18px 0 72px; animation: revealUp .8s .08s ease both; }
.hero:after { content:''; position:absolute; left:0; right:0; bottom:22px; height:1px; background:linear-gradient(90deg,transparent,rgba(157,122,255,.65),rgba(89,217,255,.55),transparent); animation:pulseGlow 3s ease-in-out infinite; }
.hero h1 { max-width: 750px; margin: 22px 0 18px; color: #fff; font-size: clamp(3.3rem, 7vw, 6.7rem); line-height: .96; letter-spacing: -.075em; font-weight: 800; }
.gradient-text { background: linear-gradient(100deg, #fff 10%, #b7a2ff 56%, #64dcff 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
.hero p { max-width: 560px; margin-bottom: 26px; color: #aab2c4; font-size: 1.05rem; line-height: 1.7; }
.hero-actions { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.secondary-link { color: #d8dbea; text-decoration: none; font-size: .84rem; font-weight: 700; padding: 11px 3px; }
.secondary-link:after { content: ' ↗'; color: #8f7aff; }

.visual-wrap { position: relative; min-height: 445px; display: grid; place-items: center; }
.visual-wrap:before, .visual-wrap:after { content: ''; position: absolute; border-radius: 50%; filter: blur(3px); }
.visual-wrap:before { width: 240px; height: 240px; background: rgba(124, 87, 255, .17); box-shadow: 0 0 100px 50px rgba(124,87,255,.12); animation:drift 6s ease-in-out infinite; }
.visual-wrap:after { width: 120px; height: 120px; margin: 180px 0 0 270px; background: rgba(44, 215, 255, .16); box-shadow: 0 0 80px 28px rgba(44,215,255,.12); animation:drift 7s 1s ease-in-out infinite reverse; }
.risk-card { position: relative; z-index: 2; width: min(100%, 390px); padding: 25px; border: 1px solid rgba(255,255,255,.15); border-radius: 24px; background: linear-gradient(145deg, rgba(25,28,46,.88), rgba(10,12,23,.78)); box-shadow: 0 28px 80px rgba(0,0,0,.38), inset 0 1px rgba(255,255,255,.10); animation:floatCard 5s ease-in-out infinite; }
.risk-card:after { content: ''; position: absolute; inset: -1px; border-radius: inherit; pointer-events: none; background: linear-gradient(135deg, rgba(157,122,255,.55), transparent 38%, rgba(89,217,255,.35)); mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); mask-composite: exclude; padding: 1px; }
.risk-card:before { content:''; position:absolute; top:0; left:0; width:24%; height:1px; background:#fff; filter:blur(1px); animation:scan 4.2s linear infinite; }
.card-top { display:flex; justify-content:space-between; align-items:center; color:#8993aa; font: 500 .67rem 'DM Mono', monospace; letter-spacing:.07em; }
.live { color: #7bffca; }
.risk-number { margin: 29px 0 3px; font-size: 4.2rem; line-height: 1; font-weight: 800; letter-spacing: -.08em; }
.risk-label { color: #ff9ee2; font: 500 .72rem 'DM Mono', monospace; letter-spacing:.11em; }
.risk-line { position:relative; height: 7px; margin: 26px 0 24px; border-radius: 99px; background: linear-gradient(90deg, #55dbff, #a77aff 52%, #ff71c8); }
.risk-line:after { content:''; position:absolute; top:50%; left:78%; width:15px; height:15px; border: 3px solid #fff; border-radius:50%; background:#b184ff; box-shadow:0 0 0 5px rgba(177,132,255,.25), 0 0 18px #b184ff; transform:translate(-50%,-50%); }
.signal-row { display:grid; grid-template-columns: 1fr auto; gap: 11px; align-items:center; margin-top: 13px; color:#abb2c3; font-size:.73rem; }
.signal-row b { color:#f4f5f8; font-weight:700; }
.signal-bar { height: 5px; margin-top: 5px; border-radius: 99px; background: #25283a; overflow:hidden; }
.signal-bar span { display:block; height:100%; border-radius:inherit; background:linear-gradient(90deg,#6adfff,#aa86ff); }
.confidence { display:flex; justify-content:space-between; margin-top:23px; padding-top:17px; border-top:1px solid rgba(255,255,255,.1); color:#8e98ac; font-size:.73rem; }
.confidence strong { color:#7bffca; }
.float-chip { position:absolute; z-index:3; padding: 11px 13px; border:1px solid rgba(255,255,255,.13); border-radius:14px; background:rgba(22,25,42,.85); backdrop-filter:blur(14px); color:#c8cde0; font:500 .64rem 'DM Mono', monospace; box-shadow:0 15px 30px rgba(0,0,0,.25); animation:floatCard 4s 1s ease-in-out infinite reverse; }
.chip-one { top: 12%; left: 2%; } .chip-two { right: 0; bottom: 15%; }

.section { position:relative; padding: 112px 0 20px; scroll-margin-top: 90px; animation:revealUp .8s ease both; }
.section:before { content:''; position:absolute; top:48px; left:-10vw; right:-10vw; height:1px; background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent); }
.section-kicker { color:#8f7aff; font:500 .7rem 'DM Mono',monospace; letter-spacing:.13em; text-transform:uppercase; }
.section h2 { margin: 12px 0 14px; color:#f8f8fb; font-size:clamp(2.25rem,4vw,4rem); line-height:1.04; letter-spacing:-.065em; }
.section-lead { max-width: 610px; color:#9fa8bb; font-size:.98rem; line-height:1.7; }
.stats { display:grid; grid-template-columns:repeat(4,1fr); gap:1px; margin: 8px 0 14px; border:1px solid var(--line); border-radius:18px; overflow:hidden; background:var(--line); }
.stat { padding: 22px 24px; background:rgba(12,14,26,.76); }
.stat strong { display:block; color:#fff; font-size:1.45rem; letter-spacing:-.04em; } .stat span { color:#8e98ac; font-size:.7rem; }
.panel { height:100%; padding:25px; border:1px solid var(--line); border-radius:20px; background:linear-gradient(145deg, rgba(20,23,39,.77), rgba(10,12,22,.64)); box-shadow:inset 0 1px rgba(255,255,255,.05); }
.panel { transition:transform .3s ease, border-color .3s ease, box-shadow .3s ease; }
.panel:hover { transform:translateY(-8px); border-color:rgba(157,122,255,.42); box-shadow:0 18px 45px rgba(0,0,0,.24), inset 0 1px rgba(255,255,255,.1); }
.panel h3 { margin:0 0 10px; color:#f4f5fb; font-size:1.04rem; letter-spacing:-.02em; } .panel p { color:#929caf; font-size:.82rem; line-height:1.6; }
.icon-box { display:grid; place-items:center; width:38px; height:38px; margin-bottom:18px; border:1px solid rgba(157,122,255,.25); border-radius:12px; color:#b7a2ff; background:rgba(157,122,255,.1); font-size:1.15rem; }
.flow { display:grid; grid-template-columns:repeat(5,1fr); align-items:center; gap:12px; margin-top:30px; }
.flow-step { text-align:center; padding:20px 10px; border:1px solid var(--line); border-radius:16px; background:rgba(17,20,34,.75); } .flow-step b { display:block; color:#fff; font-size:.85rem; } .flow-step span { color:#818ba1; font-size:.68rem; } .flow-arrow { color:#8f7aff; text-align:center; }
.flow-step { transition:transform .3s ease, background .3s ease; } .flow-step:hover { transform:scale(1.04); background:rgba(43,37,78,.7); }
.model-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:28px; } .model-stat { padding:18px; border:1px solid var(--line); border-radius:15px; background:rgba(17,20,34,.65); } .model-stat small { color:#808ba1; font: .63rem 'DM Mono',monospace; } .model-stat strong { display:block; margin-top:7px; color:#fff; font-size:1.25rem; }
.footer { margin-top:110px; padding-top:25px; border-top:1px solid var(--line); color:#6e788d; font-size:.72rem; }
.marquee { width:100vw; margin:52px calc(50% - 50vw) 0; overflow:hidden; border-top:1px solid var(--line); border-bottom:1px solid var(--line); background:rgba(14,16,29,.6); }
.marquee-track { display:flex; width:max-content; animation:marquee 24s linear infinite; }
.marquee-item { padding:17px 28px; color:#7f89a2; font:500 .68rem 'DM Mono',monospace; letter-spacing:.1em; white-space:nowrap; }
.marquee-item b { color:#b59fff; margin-right:28px; }
.scroll-cue { display:flex; align-items:center; gap:10px; margin-top:50px; color:#7f89a2; font:500 .63rem 'DM Mono',monospace; letter-spacing:.1em; }
.scroll-cue span { width:30px; height:46px; border:1px solid rgba(255,255,255,.25); border-radius:20px; position:relative; }
.scroll-cue span:after { content:''; position:absolute; width:4px; height:8px; left:50%; top:8px; border-radius:4px; background:#a992ff; transform:translateX(-50%); animation:scrollDot 1.8s ease-in-out infinite; }
@keyframes scrollDot { 0% { opacity:0; transform:translate(-50%,0); } 35% { opacity:1; } 100% { opacity:0; transform:translate(-50%,19px); } }

div[data-testid="stForm"] { border:1px solid var(--line); border-radius:20px; background:rgba(17,20,34,.72); }
.stButton > button { border-radius:999px; border:1px solid rgba(157,122,255,.35); background:linear-gradient(100deg,#b8a2ff,#68dcff); color:#080911; font-weight:800; }
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div { background:rgba(9,11,21,.75); border-color:var(--line); }
@media (max-width: 800px) { .navlinks { display:none; } .navbar { margin-bottom:38px; } .hero { padding-top:10px; } .visual-wrap { min-height:390px; margin-top:22px; } .stats { grid-template-columns:repeat(2,1fr); } .flow { grid-template-columns:1fr; } .flow-arrow { transform:rotate(90deg); } .model-grid { grid-template-columns:repeat(2,1fr); } .section { padding-top:85px; } }
</style>
""",
    unsafe_allow_html=True,
)

mode_bg = "#ffffff" if is_light else "#070912"
mode_ink = "#101827" if is_light else "#f6f7fb"
mode_muted = "#64748b" if is_light else "#9aa4b8"
mode_surface = "rgba(255,255,255,.96)" if is_light else "rgba(16,19,32,.72)"
mode_surface_2 = "#f5f7fb" if is_light else "rgba(25,29,48,.7)"
mode_line = "rgba(15,23,42,.14)" if is_light else "rgba(255,255,255,.10)"
mode_accent = "#7457e8" if is_light else "#9d7aff"
mode_cyan = "#087ea4" if is_light else "#59d9ff"
mode_pink = "#d647a4" if is_light else "#ff71c8"
st.markdown(
    f"""
<style>
/* Cinematic lightweight AI SaaS treatment */
.stApp {{ background:{mode_bg}; color:{mode_ink}; font-family:'Manrope',sans-serif; overflow-x:hidden; }}
.stApp:before {{ opacity:.18; background-image:linear-gradient({mode_line} 1px,transparent 1px),linear-gradient(90deg,{mode_line} 1px,transparent 1px); background-size:72px 72px; mask-image:linear-gradient(to bottom,black,transparent 72%); }}
.block-container {{ max-width:none; width:100%; padding:0.35rem 4.2vw 5rem; }}
.navbar {{ position:sticky; top:12px; margin-top:-28px; z-index:10; border:0; border-radius:0; margin-bottom:70px; padding:12px 0; background:transparent; backdrop-filter:none; box-shadow:none; }}
.brand {{ color:{mode_ink}; }} .brand small {{ color:{mode_muted}; }} .logo {{ border:1px solid {mode_accent}; background:linear-gradient(145deg,rgba(157,122,255,.25),rgba(89,217,255,.12)); color:{mode_ink}; box-shadow:0 0 24px rgba(157,122,255,.22); }}
.navlinks a {{ color:{mode_muted}; }} .navlinks a:hover {{ color:{mode_ink}; }} .navcta,.primary-link {{ color:#080911 !important; border-radius:999px; background:linear-gradient(100deg,#b8a2ff,#68dcff); box-shadow:0 8px 28px rgba(112,157,255,.25); }}
.hero {{ padding:18px 0 72px; }} .hero h1 {{ max-width:750px; color:{mode_ink}; font-size:clamp(3.3rem,7vw,6.7rem); line-height:.96; letter-spacing:-.075em; font-weight:800; }} .gradient-text {{ background:linear-gradient(100deg,{mode_ink} 10%,{mode_accent} 56%,{mode_cyan} 100%); -webkit-background-clip:text; background-clip:text; color:transparent; background-size:180% auto; animation:gradientMove 5s ease-in-out infinite; }} .hero p {{ color:{mode_muted}; }} .secondary-link {{ color:{mode_ink}; }} .secondary-link:after {{ color:{mode_accent}; }}
.visual-wrap {{ min-height:500px; }} .visual-wrap:before {{ width:250px; height:250px; background:rgba(124,87,255,.17); box-shadow:0 0 100px 50px rgba(124,87,255,.12); animation:drift 6s ease-in-out infinite; }} .visual-wrap:after {{ background:rgba(44,215,255,.16); box-shadow:0 0 80px 28px rgba(44,215,255,.12); animation:drift 7s 1s ease-in-out infinite reverse; }}
.risk-card {{ border:0; border-left:1px solid rgba(157,122,255,.42); border-radius:0; background:transparent; box-shadow:none; padding-left:30px; animation:floatCard 5s ease-in-out infinite; }} .risk-card:after {{ display:none; }} .risk-number {{ color:{mode_ink}; }} .risk-label {{ color:{mode_pink}; }} .risk-line {{ background:linear-gradient(90deg,{mode_cyan},{mode_accent},{mode_pink}); }} .signal-row {{ color:{mode_muted}; }} .signal-row b {{ color:{mode_ink}; }} .confidence {{ border-color:{mode_line}; color:{mode_muted}; }} .confidence strong {{ color:#7bffca; }} .float-chip {{ border:0; border-radius:0; background:transparent; color:#c8cde0; box-shadow:none; }}
.stats {{ border:0; background:transparent; }} .stat {{ background:transparent; border-right:1px solid {mode_line}; }} .stat strong {{ color:{mode_ink}; }} .stat span {{ color:{mode_muted}; }} .marquee {{ border-color:{mode_line}; background:{mode_surface_2}; }} .marquee-item {{ color:{mode_muted}; }} .marquee-item b {{ color:{mode_accent}; }}
.section {{ padding:112px 0 20px; }} .section:before {{ background:linear-gradient(90deg,transparent,{mode_line},transparent); }} .section-kicker {{ color:{mode_accent}; }} .section h2 {{ color:{mode_ink}; font-size:clamp(2.25rem,4vw,4rem); }} .section-lead {{ color:{mode_muted}; }}
.panel {{ border:0; border-top:1px solid {mode_line}; border-radius:0; background:transparent; box-shadow:none; padding:28px 0; }} .panel:hover {{ transform:translateY(-5px); border-color:{mode_accent}; box-shadow:none; }} .panel h3 {{ color:{mode_ink}; }} .panel p {{ color:{mode_muted}; }} .icon-box {{ border:0; border-radius:0; color:{mode_accent}; background:transparent; padding:0; width:auto; height:auto; place-items:start; }} .flow-step {{ border:0; border-bottom:1px solid {mode_line}; border-radius:0; background:transparent; }} .flow-step b {{ color:{mode_ink}; }} .flow-step span,.flow-arrow {{ color:{mode_accent}; }} .model-stat {{ border:0; border-left:1px solid {mode_line}; border-radius:0; background:transparent; }} .model-stat small {{ color:{mode_muted}; }} .model-stat strong {{ color:{mode_ink}; }} .footer {{ border-color:{mode_line}; color:{mode_muted}; }}
.stCheckbox {{ position:fixed; top:20px; right:4.2vw; z-index:40; padding:8px 14px; border:1px solid rgba(157,122,255,.35); border-radius:999px; background:linear-gradient(100deg,#b8a2ff,#68dcff); box-shadow:0 8px 28px rgba(112,157,255,.2); }} .stCheckbox label {{ color:#080911 !important; font-weight:800; }} .stButton > button {{ border-radius:999px; border:1px solid rgba(157,122,255,.35); background:linear-gradient(100deg,#b8a2ff,#68dcff); color:#080911; box-shadow:0 8px 28px rgba(112,157,255,.2); font-weight:800; }}
.intro-overlay {{ position:fixed; inset:0; z-index:999; pointer-events:none; background:#070912; animation:introExit 1.8s cubic-bezier(.76,0,.24,1) forwards; }} .intro-mark {{ position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); color:#fff; text-align:center; font:800 1.1rem Manrope,sans-serif; letter-spacing:.12em; animation:introMark 1.15s ease forwards; }} .intro-mark small {{ display:block; margin-top:10px; color:#9d7aff; font:500 .6rem 'DM Mono',monospace; letter-spacing:.2em; }} .intro-line {{ position:absolute; left:10%; right:10%; top:54%; height:1px; background:linear-gradient(90deg,transparent,#59d9ff,#9d7aff,#ff71c8,transparent); transform:scaleX(0); transform-origin:left; animation:introLine 1s .2s ease forwards; box-shadow:0 0 18px #59d9ff; }}
.orbit {{ position:absolute; border:1px solid rgba(157,122,255,.28); border-radius:50%; transform:rotate(-18deg); pointer-events:none; }} .orbit-a {{ width:455px; height:170px; animation:orbitSpin 12s linear infinite; }} .orbit-b {{ width:520px; height:245px; border-color:rgba(89,217,255,.2); transform:rotate(32deg); animation:orbitSpin 16s linear infinite reverse; }} .orbit:after {{ content:''; position:absolute; width:7px; height:7px; top:14%; left:18%; border-radius:50%; background:#59d9ff; box-shadow:0 0 16px #59d9ff; }}
.data-transition {{ position:relative; min-height:210px; margin:45px 0 20px; padding:32px 0; overflow:hidden; border-top:1px solid {mode_line}; border-bottom:1px solid {mode_line}; border-radius:0; background:transparent; }} .data-transition h3 {{ margin:0; color:{mode_ink}; font-size:1.05rem; }} .data-transition p {{ margin:6px 0 22px; color:{mode_muted}; font-size:.78rem; }} .data-dots {{ display:flex; flex-wrap:wrap; gap:12px; max-width:760px; }} .data-dots i {{ width:8px; height:8px; border-radius:50%; background:linear-gradient(135deg,#59d9ff,#9d7aff); box-shadow:0 0 10px rgba(89,217,255,.55); animation:dotPop 2.8s ease-in-out infinite alternate; }} .data-dots i:nth-child(3n) {{ animation-delay:.7s; }} .data-dots i:nth-child(4n) {{ animation-delay:1.1s; }} .data-count {{ position:absolute; right:32px; top:50%; transform:translateY(-50%); color:{mode_ink}; font-size:3rem; font-weight:800; letter-spacing:-.08em; }} .data-count span {{ display:block; color:{mode_muted}; font:500 .62rem 'DM Mono',monospace; letter-spacing:.1em; text-align:right; }}
@keyframes gradientMove {{ 0%,100% {{ background-position:0 50%; }} 50% {{ background-position:100% 50%; }} }} @keyframes introLine {{ to {{ transform:scaleX(1); }} }} @keyframes introMark {{ from {{ opacity:0; transform:translate(-50%,-35%); }} to {{ opacity:1; transform:translate(-50%,-50%); }} }} @keyframes introExit {{ 0%,72% {{ opacity:1; }} 100% {{ opacity:0; visibility:hidden; }} }} @keyframes orbitSpin {{ from {{ transform:rotate(-18deg) rotate(0deg); }} to {{ transform:rotate(-18deg) rotate(360deg); }} }} @keyframes dotPop {{ from {{ opacity:.25; transform:scale(.7); }} to {{ opacity:1; transform:scale(1.3); }} }}
</style>
""",
    unsafe_allow_html=True,
)


def anchor(href: str, label: str, cls: str = "") -> str:
    return f'<a class="{cls}" href="{href}">{label}</a>'


# -----------------------------
# Navigation + hero
# -----------------------------
st.markdown('<div class="intro-overlay"><div class="intro-line"></div><div class="intro-mark">STAYPREDICT AI<small>HOTEL INTELLIGENCE / 01</small></div></div>', unsafe_allow_html=True)
st.markdown(
    f"""
<nav class="navbar">
  <a class="brand" href="#home">
    <span class="logo"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 20V9.5L12 4l8 5.5V20"/><path d="M8 20v-5h8v5M8 10h.01M12 10h.01M16 10h.01"/><path d="m14 7 2-2 1.5 1.5"/></svg></span>
    <span>StayPredict<small>HOTEL INTELLIGENCE, BEFORE CHECK-IN.</small></span>
  </a>
  <div class="navlinks">
    {anchor('#home','Home')}{anchor('#insights','Intelligence')}{anchor('#how-it-works','How it works')}{anchor('#model','Model')}{anchor('#predictor','Predictor')}
    {anchor('#predictor','Launch predictor →','navcta')}
  </div>
</nav>
<section id="home" class="hero">
  <div class="eyebrow"><i></i> AI-POWERED HOTEL INTELLIGENCE</div>
  <div style="height:14px"></div>
</section>
""",
    unsafe_allow_html=True,
)

hero_left, hero_right = st.columns([1.06, 0.94], gap="large")
with hero_left:
    st.markdown(
        """
<h1>Predict cancellations.<br><span class="gradient-text">Before they happen.</span></h1>
<p>StayPredict AI analyzes hotel reservation patterns and estimates cancellation risk before check-in — turning booking data into actionable intelligence.</p>
<div class="hero-actions"><a class="primary-link" href="#predictor">Start predicting&nbsp; →</a><a class="secondary-link" href="#insights">Explore the intelligence</a></div>
<div class="scroll-cue"><span></span>SCROLL TO EXPLORE</div>
""",
        unsafe_allow_html=True,
    )
with hero_right:
    st.markdown(
        """
<div class="visual-wrap">
  <div class="orbit orbit-a"></div><div class="orbit orbit-b"></div>
  <div class="float-chip chip-one">↗ SIGNAL DETECTED&nbsp;&nbsp; 12.8ms</div>
  <div class="float-chip chip-two">✦ MODEL CONFIDENCE&nbsp;&nbsp; 91.2%</div>
  <div class="risk-card">
    <div class="card-top"><span>CANCELLATION RISK</span><span class="live">● LIVE</span></div>
    <div class="risk-number">78.4<span style="font-size:1.7rem;color:#aaa9be">%</span></div>
    <div class="risk-label">HIGH RISK</div>
    <div class="risk-line"></div>
    <div class="signal-row"><div>Lead time<div class="signal-bar"><span style="width:88%"></span></div></div><b>HIGH</b></div>
    <div class="signal-row"><div>Previous cancellations<div class="signal-bar"><span style="width:68%"></span></div></div><b>HIGH</b></div>
    <div class="signal-row"><div>Deposit type<div class="signal-bar"><span style="width:42%"></span></div></div><b style="color:#f5ca75">MEDIUM</b></div>
    <div class="confidence"><span>AI CONFIDENCE</span><strong>91.2%</strong></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown(
    """
<div class="stats">
  <div class="stat"><strong>36,275</strong><span>reservations in source dataset</span></div>
  <div class="stat"><strong>19</strong><span>booking columns explored</span></div>
  <div class="stat"><strong>6</strong><span>classification models benchmarked</span></div>
  <div class="stat"><strong>0.9558</strong><span>Random Forest test ROC-AUC</span></div>
</div>
<div class="marquee"><div class="marquee-track">
  <div class="marquee-item"><b>✦</b> RESERVATION SIGNALS</div><div class="marquee-item"><b>✦</b> LEAD TIME PATTERNS</div><div class="marquee-item"><b>✦</b> GUEST HISTORY</div><div class="marquee-item"><b>✦</b> ACTIONABLE RISK</div><div class="marquee-item"><b>✦</b> RESERVATION SIGNALS</div><div class="marquee-item"><b>✦</b> LEAD TIME PATTERNS</div><div class="marquee-item"><b>✦</b> GUEST HISTORY</div><div class="marquee-item"><b>✦</b> ACTIONABLE RISK</div>
</div></div>
""",
    unsafe_allow_html=True,
)

st.markdown('''<div class="data-transition"><h3>ONE RESERVATION <span style="color:#9d7aff">→</span> THOUSANDS OF RESERVATIONS</h3><p>From a single booking signal to a living map of hotel intelligence.</p><div class="data-dots">''' + ''.join('<i></i>' for _ in range(58)) + '''</div><div class="data-count">36K+<span>BOOKINGS ANALYZED</span></div></div>''', unsafe_allow_html=True)

# -----------------------------
# Story sections
# -----------------------------
st.markdown(
    """
<section id="about" class="section">
  <div class="section-kicker">01 / The problem</div>
  <h2>Every cancellation<br>has a cost.</h2>
  <p class="section-lead">Empty rooms, uncertain inventory, and reactive decisions compound quickly. StayPredict helps teams see the risk while there is still time to act.</p>
</section>
""",
    unsafe_allow_html=True,
)

problem_cols = st.columns(3, gap="medium")
for col, icon, title, body in zip(
    problem_cols,
    ["↘", "⌁", "◎"],
    ["Lost revenue", "Uncertain inventory", "Reactive decisions"],
    ["Unexpected cancellations create empty rooms and lost revenue.", "Hotels struggle to forecast demand when booking intent is unclear.", "Without prediction, teams can only react after the cancellation happens."],
):
    with col:
        st.markdown(f'<div class="panel"><div class="icon-box">{icon}</div><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)

st.markdown(
    """
<section id="how-it-works" class="section">
  <div class="section-kicker">02 / The intelligence layer</div>
  <h2>Don’t just track reservations.<br><span class="gradient-text">Predict them.</span></h2>
  <p class="section-lead">A practical ML workflow turns reservation signals into a probability that hotel teams can understand and act on.</p>
  <div class="flow"><div class="flow-step"><b>Reservation data</b><span>Capture</span></div><div class="flow-arrow">→</div><div class="flow-step"><b>Feature patterns</b><span>Analyze</span></div><div class="flow-arrow">→</div><div class="flow-step"><b>Risk probability</b><span>Predict</span></div></div>
</section>
""",
    unsafe_allow_html=True,
)

st.markdown('<section id="insights" class="section"><div class="section-kicker">03 / Project signals</div><h2>From raw data<br>to hotel intelligence.</h2><p class="section-lead">The source project explores the behavioral signals behind cancellations, from lead time and market segment to guest history and special requests.</p></section>', unsafe_allow_html=True)
insight_cols = st.columns([1.4, 1, 1], gap="medium")
with insight_cols[0]:
    st.markdown('<div class="panel"><h3>Cancellation signal map</h3><p>Lead time and guest history are surfaced alongside stay, pricing, segment, and request details.</p><div style="height:170px;display:flex;align-items:end;gap:9px;padding:20px 4px 4px;background:linear-gradient(180deg,transparent,rgba(157,122,255,.05));border-bottom:1px solid rgba(255,255,255,.1)"><span style="height:74%;flex:1;background:linear-gradient(#a47fff,#5d50bc);border-radius:7px 7px 0 0"></span><span style="height:43%;flex:1;background:linear-gradient(#6adeff,#397d9c);border-radius:7px 7px 0 0"></span><span style="height:88%;flex:1;background:linear-gradient(#ff9bda,#a94389);border-radius:7px 7px 0 0"></span><span style="height:59%;flex:1;background:linear-gradient(#a47fff,#5d50bc);border-radius:7px 7px 0 0"></span><span style="height:34%;flex:1;background:linear-gradient(#6adeff,#397d9c);border-radius:7px 7px 0 0"></span><span style="height:66%;flex:1;background:linear-gradient(#a47fff,#5d50bc);border-radius:7px 7px 0 0"></span></div><p style="font: .62rem DM Mono,monospace;color:#707b91;margin:12px 0 0">LEAD TIME&nbsp;&nbsp; SEGMENT&nbsp;&nbsp; HISTORY&nbsp;&nbsp; ADR&nbsp;&nbsp; REQUESTS</p></div>', unsafe_allow_html=True)
with insight_cols[1]:
    st.markdown('<div class="panel"><div class="icon-box">↗</div><h3>Explainable</h3><p>Understand which reservation features influence risk instead of receiving a black-box label.</p></div>', unsafe_allow_html=True)
with insight_cols[2]:
    st.markdown('<div class="panel"><div class="icon-box">⌁</div><h3>Actionable</h3><p>Convert model output into earlier follow-ups, inventory planning, and smarter decisions.</p></div>', unsafe_allow_html=True)

st.markdown('<section id="model" class="section"><div class="section-kicker">04 / Under the hood</div><h2>Built to be<br>portfolio-ready.</h2><p class="section-lead">The repository notebook benchmarks multiple classifiers with leakage-aware preprocessing, resampling, model tuning, and SHAP explainability.</p><div class="model-grid"><div class="model-stat"><small>BEST MODEL</small><strong>Random Forest</strong></div><div class="model-stat"><small>TEST ACCURACY</small><strong>90.21%</strong></div><div class="model-stat"><small>F1 SCORE</small><strong>84.89%</strong></div><div class="model-stat"><small>ROC-AUC</small><strong>0.9558</strong></div></div></section>', unsafe_allow_html=True)

# -----------------------------
# Predictor section
# -----------------------------
st.markdown('<section id="predictor" class="section"><div class="section-kicker">05 / Live prediction</div><h2>Ready to test<br>a reservation?</h2><p class="section-lead">Give the model a reservation. Let the data decide.</p></section>', unsafe_allow_html=True)

model_path = Path("model/model.pkl")
if not model_path.exists():
    st.markdown('<div class="panel" style="border-color:rgba(157,122,255,.28);"><h3>Model not connected yet</h3><p>The landing page is live. Add the trained pipeline at <code>model/model.pkl</code> to activate real predictions; this app never fabricates a result.</p></div>', unsafe_allow_html=True)
else:
    with st.form("predictor_form"):
        st.markdown("#### Reservation risk predictor")
        c1, c2, c3 = st.columns(3)
        with c1:
            lead_time = st.number_input("Lead time (days)", 0, 500, 60)
            arrival_year = st.number_input("Arrival year", 2017, 2030, 2018)
            arrival_month = st.slider("Arrival month", 1, 12, 7)
            arrival_date = st.slider("Arrival date", 1, 31, 15)
            no_of_adults = st.number_input("Adults", 0, 10, 2)
        with c2:
            no_of_children = st.number_input("Children", 0, 10, 0)
            no_of_weekend_nights = st.number_input("Weekend nights", 0, 20, 1)
            no_of_week_nights = st.number_input("Week nights", 0, 30, 2)
            repeated_guest = st.selectbox("Repeated guest", [0, 1], format_func=lambda x: "Yes" if x else "No")
            no_of_special_requests = st.number_input("Special requests", 0, 5, 1)
        with c3:
            avg_price_per_room = st.number_input("Average price per room", 0.0, 1000.0, 100.0)
            no_of_previous_cancellations = st.number_input("Previous cancellations", 0, 20, 0)
            no_of_previous_bookings_not_canceled = st.number_input("Previous bookings not canceled", 0, 50, 0)
            meal_plan = st.selectbox("Meal plan", ["Meal Plan 1", "Meal Plan 2", "Meal Plan 3", "Not Selected"])
            room_type = st.selectbox("Room type", [f"Room_Type {i}" for i in range(1, 8)])
        submitted = st.form_submit_button("Predict cancellation →")
    if submitted:
        st.warning("The model file is present, but the app needs the repository’s complete preprocessing pipeline to safely run this prediction.")

st.markdown('<div class="footer"><strong>StayPredict AI</strong> · Hotel intelligence, before check-in. Built for transparent ML experimentation.</div>', unsafe_allow_html=True)
