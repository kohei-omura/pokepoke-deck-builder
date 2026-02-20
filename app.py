"""
ポケポケ デッキビルダー - Streamlit Webアプリ版
起動方法: streamlit run app.py
"""

import json
import os
import streamlit as st

# ─────────────────────────────────────────────
#  設定
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ポケポケ デッキビルダー",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded",
)

DECKS_FILE = "decks.json"

TYPE_EMOJI = {
    "草": "🌿", "炎": "🔥", "水": "💧", "雷": "⚡", "超": "🔮",
    "闘": "👊", "悪": "🌑", "鋼": "⚙️", "無色": "⭐", "ドラゴン": "🐉",
}

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
  html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }
  .deck-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px; padding: 24px; color: white;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4); margin-bottom: 16px;
  }
  .deck-title { font-size: 2rem; font-weight: 700; margin-bottom: 4px; }
  .tag {
    display: inline-block; padding: 4px 12px; border-radius: 20px;
    font-size: 0.8rem; font-weight: 700; margin-right: 8px; margin-bottom: 8px;
  }
  .phase-card {
    background: rgba(255,255,255,0.05); border-radius: 12px;
    padding: 12px 16px; margin-bottom: 8px; border-left: 4px solid;
  }
  .strength-item { color: #4ade80; font-weight: 500; }
  .weakness-item { color: #f87171; font-weight: 500; }
  .recipe-table { width: 100%; border-collapse: collapse; }
  .recipe-table th {
    background: rgba(255,255,255,0.15); padding: 8px 12px;
    text-align: left; font-size: 0.9rem; border-radius: 6px 6px 0 0;
  }
  .recipe-table td { padding: 6px 12px; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 0.9rem; }
  .total-row { background: rgba(255,255,255,0.1); font-weight: 700; }
  .tip-box {
    background: linear-gradient(135deg, #065f46, #047857);
    border-radius: 12px; padding: 14px 18px; margin-top: 12px;
  }
  .stSelectbox label { font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  データ読み込み
# ─────────────────────────────────────────────
@st.cache_data
def load_decks() -> dict:
    if not os.path.exists(DECKS_FILE):
        return {}
    with open(DECKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_decks(decks: dict) -> None:
    with open(DECKS_FILE, "w", encoding="utf-8") as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
#  サイドバー
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🃏 ポケポケ\nデッキビルダー")
    st.divider()

    decks = load_decks()
    deck_names = list(decks.keys())

    selected_deck = st.selectbox(
        "デッキ主軸を選択",
        options=[""] + deck_names,
        format_func=lambda x: "--- デッキを選んでください ---" if x == "" else x,
    )

    st.divider()

    # 検索フィルター
    st.markdown("**🔍 タイプで絞り込み**")
    all_types = list(set(d.get("タイプ", "") for d in decks.values()))
    selected_type = st.selectbox("タイプ", ["すべて"] + sorted(all_types))

    if selected_type != "すべて":
        filtered = [n for n, d in decks.items() if d.get("タイプ") == selected_type]
        if filtered:
            st.markdown("**対象デッキ:**")
            for f in filtered:
                st.markdown(f"・{f}")

    st.divider()

    with st.expander("➕ 新規デッキ追加"):
        new_name = st.text_input("デッキ名")
        new_type = st.selectbox("タイプ", ["炎", "水", "草", "雷", "超", "闘", "悪", "鋼", "無色", "ドラゴン"])
        new_diff = st.select_slider("難易度", options=["★", "★★", "★★★", "★★★★", "★★★★★"])
        new_strength = st.text_area("強み（1行1項目）")
        new_weakness = st.text_area("弱み（1行1項目）")
        new_tips = st.text_input("対策・アドバイス")
        new_color = st.color_picker("イメージカラー", "#3B82F6")

        if st.button("💾 追加・保存", use_container_width=True):
            if new_name and new_name not in decks:
                decks[new_name] = {
                    "タイプ": new_type,
                    "難易度": new_diff,
                    "レシピ": {"ポケモン": [], "トレーナー": []},
                    "回し方": {"序盤": "", "中盤": "", "終盤": ""},
                    "強み": [s for s in new_strength.split("\n") if s.strip()],
                    "弱み": [w for w in new_weakness.split("\n") if w.strip()],
                    "対策": new_tips,
                    "イメージカラー": new_color,
                }
                save_decks(decks)
                st.success(f"「{new_name}」を追加しました！")
                st.cache_data.clear()
                st.rerun()
            elif new_name in decks:
                st.error("同名のデッキが既に存在します。")
            else:
                st.error("デッキ名を入力してください。")


# ─────────────────────────────────────────────
#  メインエリア
# ─────────────────────────────────────────────
if not selected_deck:
    # ホーム画面
    st.markdown("# 🃏 ポケポケ デッキビルダー")
    st.markdown("**Pokémon TCG Pocket** のデッキレシピ・回し方・強み/弱みを確認できるアプリです。")
    st.divider()

    st.markdown("### 📦 収録デッキ一覧")
    cols = st.columns(3)
    for i, (name, data) in enumerate(decks.items()):
        color = data.get("イメージカラー", "#3B82F6")
        emoji = TYPE_EMOJI.get(data.get("タイプ", ""), "🃏")
        diff = data.get("難易度", "?")
        tier = data.get("Tier", "")
        tier_colors = {"Tier1": "#FFD700", "Tier2": "#C0C0C0", "Tier3": "#CD7F32", "参考": "#6B7280"}
        tier_color = tier_colors.get(tier, "#6B7280")
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}44, {color}22);
                        border: 2px solid {color}; border-radius: 12px;
                        padding: 16px; margin-bottom: 12px; text-align: center;">
              <div style="font-size: 2rem">{emoji}</div>
              <div style="font-weight:700; font-size:1rem; margin:6px 0">{name}</div>
              <div style="font-size:0.8rem; color:#888">{data.get('タイプ','?')}タイプ　難易度: {diff}</div>
              {f'<div style="margin-top:6px;font-size:0.75rem;font-weight:800;color:{tier_color}">{tier}</div>' if tier else ''}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("👈 左サイドバーからデッキを選んでください。")

else:
    # デッキ詳細
    deck = decks[selected_deck]
    color = deck.get("イメージカラー", "#3B82F6")
    emoji = TYPE_EMOJI.get(deck.get("タイプ", ""), "🃏")

    tier = deck.get("Tier", "")
    tier_colors = {"Tier1": "#FFD700", "Tier2": "#C0C0C0", "Tier3": "#CD7F32", "参考": "#6B7280"}
    tier_color = tier_colors.get(tier, "#6B7280")

    # ヘッダー
    st.markdown(f"""
    <div class="deck-card" style="border: 2px solid {color}">
      <div class="deck-title">{emoji} {selected_deck}</div>
      <span class="tag" style="background:{color}44; border: 1px solid {color}">
        {deck.get('タイプ','?')}タイプ
      </span>
      <span class="tag" style="background:#ffffff22; border: 1px solid #ffffff44">
        難易度: {deck.get('難易度','?')}
      </span>
      {f'<span class="tag" style="background:{tier_color}44; border: 1px solid {tier_color}; color:{tier_color}; font-weight:800">{tier}</span>' if tier else ''}
    </div>
    """, unsafe_allow_html=True)

    # 3カラムレイアウト
    col1, col2 = st.columns([1, 1])

    with col1:
        # レシピ
        st.markdown("### 📋 デッキレシピ")
        recipe = deck.get("レシピ", {})
        pokemon_list = recipe.get("ポケモン", [])
        trainer_list = recipe.get("トレーナー", [])
        total_pokemon = sum(p["枚数"] for p in pokemon_list)
        total_trainer = sum(t["枚数"] for t in trainer_list)

        tab1, tab2 = st.tabs([f"ポケモン ({total_pokemon}枚)", f"トレーナー ({total_trainer}枚)"])
        with tab1:
            if pokemon_list:
                for p in pokemon_list:
                    st.markdown(f"🔵 **{p['名前']}** × {p['枚数']}")
            else:
                st.info("データなし")

        with tab2:
            if trainer_list:
                for t in trainer_list:
                    st.markdown(f"🟡 **{t['名前']}** × {t['枚数']}")
            else:
                st.info("データなし")

        total_all = total_pokemon + total_trainer
        st.metric("合計枚数", f"{total_all} 枚", delta=f"{20 - total_all} 枠空き" if total_all < 20 else "✅ 20枚")

    with col2:
        # 回し方
        st.markdown("### 🎮 回し方")
        phase_colors = {"序盤": "#3B82F6", "中盤": "#8B5CF6", "終盤": "#EF4444"}
        howto = deck.get("回し方", {})
        for phase, desc in howto.items():
            border_color = phase_colors.get(phase, "#64748B")
            st.markdown(f"""
            <div class="phase-card" style="border-left-color: {border_color}; background: rgba(255,255,255,0.03)">
              <span style="font-weight:700; color:{border_color}">【{phase}】</span>
              <span style="font-size:0.92rem"> {desc}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # 強み・弱み
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### ✅ 強み")
        for s in deck.get("強み", []):
            st.markdown(f'<p class="strength-item">▶ {s}</p>', unsafe_allow_html=True)

    with col4:
        st.markdown("### ❌ 弱み")
        for w in deck.get("弱み", []):
            st.markdown(f'<p class="weakness-item">▶ {w}</p>', unsafe_allow_html=True)

    # 対策
    st.markdown("### 💡 対策・アドバイス")
    st.markdown(f"""
    <div class="tip-box">
      💡 {deck.get('対策', '記録なし')}
    </div>
    """, unsafe_allow_html=True)

    # 削除ボタン
    with st.expander("⚠️ このデッキを削除"):
        st.warning(f"「{selected_deck}」を削除しますか？この操作は元に戻せません。")
        if st.button("🗑️ 削除する", type="primary"):
            del decks[selected_deck]
            save_decks(decks)
            st.cache_data.clear()
            st.success("削除しました。")
            st.rerun()
