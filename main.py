"""
ポケポケ デッキビルダー - CLIバージョン
使い方: python main.py
"""

import json
import os


def load_decks(filepath: str = "decks.json") -> dict:
    """JSONファイルからデッキデータを読み込む"""
    if not os.path.exists(filepath):
        print(f"エラー: {filepath} が見つかりません。")
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def display_deck(deck_name: str, deck: dict) -> None:
    """デッキ情報を整形して表示する"""
    print(f"\n{'='*50}")
    print(f"  【{deck_name}デッキ】  タイプ: {deck.get('タイプ', '不明')}  難易度: {deck.get('難易度', '?')}")
    print(f"{'='*50}")

    # レシピ
    print("\n📋 デッキレシピ")
    print("-" * 30)
    recipe = deck.get("レシピ", {})

    print("  [ポケモン]")
    pokemon_total = 0
    for p in recipe.get("ポケモン", []):
        print(f"    {p['名前']} × {p['枚数']}")
        pokemon_total += p['枚数']
    print(f"    （計 {pokemon_total} 枚）")

    print("  [トレーナー]")
    trainer_total = 0
    for t in recipe.get("トレーナー", []):
        print(f"    {t['名前']} × {t['枚数']}")
        trainer_total += t['枚数']
    print(f"    （計 {trainer_total} 枚）")
    print(f"  合計: {pokemon_total + trainer_total} 枚")

    # 回し方
    print("\n🎮 回し方")
    print("-" * 30)
    howto = deck.get("回し方", {})
    for phase, desc in howto.items():
        print(f"  【{phase}】{desc}")

    # 強み
    print("\n✅ 強み")
    print("-" * 30)
    for s in deck.get("強み", []):
        print(f"  ・{s}")

    # 弱み
    print("\n❌ 弱み")
    print("-" * 30)
    for w in deck.get("弱み", []):
        print(f"  ・{w}")

    # 対策
    print("\n💡 対策・アドバイス")
    print("-" * 30)
    print(f"  {deck.get('対策', '')}")
    print()


def add_deck(decks: dict, filepath: str = "decks.json") -> dict:
    """新しいデッキを対話形式で追加する"""
    print("\n=== 新規デッキ追加 ===")
    name = input("デッキ名を入力: ").strip()
    if not name:
        print("デッキ名が空です。キャンセルします。")
        return decks

    deck_type = input("タイプ（例: 炎, 水, 超）: ").strip()
    difficulty = input("難易度（例: ★★★）: ").strip()
    recipe = input("レシピを一行で入力（メモ用）: ").strip()
    howto = input("回し方を一行で入力: ").strip()
    strengths = input("強みを一行で入力: ").strip()
    weaknesses = input("弱みを一行で入力: ").strip()
    tips = input("対策・アドバイス: ").strip()

    decks[name] = {
        "タイプ": deck_type,
        "難易度": difficulty,
        "レシピ": {"ポケモン": [], "トレーナー": []},
        "回し方": {"メモ": howto},
        "強み": [strengths],
        "弱み": [weaknesses],
        "対策": tips,
        "イメージカラー": "#888888"
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)

    print(f"✅ 「{name}」デッキを追加・保存しました。")
    return decks


def main():
    print("╔══════════════════════════════════════╗")
    print("║   ポケポケ デッキビルダー  🃏         ║")
    print("╚══════════════════════════════════════╝")

    decks = load_decks()
    if not decks:
        return

    while True:
        print("\n利用可能なデッキ一覧:")
        for i, name in enumerate(decks.keys(), 1):
            d = decks[name]
            print(f"  {i}. {name}  ({d.get('タイプ','?')}タイプ  難易度: {d.get('難易度','?')})")

        print("\nコマンド: [デッキ名を入力] 表示 / [new] 新規追加 / [quit] 終了")
        user_input = input("デッキ主軸を入力: ").strip()

        if user_input.lower() in ("quit", "q", "exit"):
            print("終了します。")
            break
        elif user_input.lower() == "new":
            decks = add_deck(decks)
        elif user_input in decks:
            display_deck(user_input, decks[user_input])
        else:
            print(f"「{user_input}」は見つかりません。新規追加しますか？ (y/n)")
            if input().strip().lower() == "y":
                decks = add_deck(decks)


if __name__ == "__main__":
    main()
