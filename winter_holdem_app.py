
import streamlit as st
from itertools import combinations
from treys import Card, Evaluator, Deck

st.set_page_config(page_title="윈터의 홀덤", layout="centered")
st.title("🃏 윈터의 홀덤")
st.markdown("텍사스 홀덤 승률 계산기 (최대 8인)")

# 카드 리스트 (52장)
suits = ['s', 'h', 'd', 'c']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
cards = [r + s for r in ranks for s in suits]

# 플레이어 수 선택
num_players = st.selectbox("👥 플레이어 수", range(2, 9))

# 플레이어 카드 입력
player_hands = []
for i in range(num_players):
    st.markdown(f"**Player {i+1} 카드 선택**")
    col1, col2 = st.columns(2)
    with col1:
        card1 = st.selectbox(f"Player {i+1} 카드 1", cards, key=f"p{i}_1")
    with col2:
        card2 = st.selectbox(f"Player {i+1} 카드 2", [c for c in cards if c != card1], key=f"p{i}_2")
    player_hands.append([card1, card2])

# 보드 카드 입력
st.markdown("### 📍 보드 카드 선택")
flop_cols = st.columns(3)
flop = [flop_cols[i].selectbox(f"Flop 카드 {i+1}", ['--'] + cards, key=f"f{i}") for i in range(3)]
turn = st.selectbox("Turn 카드", ['--'] + cards, key="turn")
river = st.selectbox("River 카드", ['--'] + cards, key="river")

# 중복 체크
selected_cards = [c for pair in player_hands for c in pair]
board_cards = [c for c in flop + [turn, river] if c != '--']
all_selected = selected_cards + board_cards

if len(set(all_selected)) != len(all_selected):
    st.error("❗ 중복된 카드가 있습니다. 다시 선택해주세요.")
else:
    if st.button("🎯 승률 계산하기"):
        evaluator = Evaluator()
        board = [Card.new(c) for c in board_cards]

        scores = []
        for hand in player_hands:
            cards_obj = [Card.new(c) for c in hand]
            score = evaluator.evaluate(board, cards_obj)
            scores.append(score)

        min_score = min(scores)
        winners = [i for i, s in enumerate(scores) if s == min_score]

        st.markdown("### 📊 결과")
        for i, score in enumerate(scores):
            pct = evaluator.get_five_card_rank_percentage(score)
            result = f"Player {i+1}: 점수 {score} → 강도 {100 - pct:.2f}"
            if i in winners:
                st.success("✅ " + result)
            else:
                st.info(result)
