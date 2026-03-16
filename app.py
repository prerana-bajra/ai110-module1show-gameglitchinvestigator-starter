import random
from pathlib import Path

import streamlit as st
from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    load_high_score,
    parse_guess,
    update_high_score,
    update_score,
)

HIGH_SCORE_FILE = Path(__file__).with_name("high_score.json")

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "selected_difficulty" not in st.session_state:
    st.session_state.selected_difficulty = difficulty
elif st.session_state.selected_difficulty != difficulty:
    # FIX: Copilot helped reset core state on difficulty switch so old-game state does not leak.
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    # FIX: Reset per-game score when difficulty changes so saved high scores stay meaningful.
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_log = []
    st.session_state.selected_difficulty = difficulty
    st.rerun()

if "secret" not in st.session_state:
    # FIX: Initialized secret once in session_state with AI guidance to keep it stable across reruns.
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "high_score" not in st.session_state:
    # FIX: Agent-planned feature loads the best completed-game score from disk.
    st.session_state.high_score = load_high_score(HIGH_SCORE_FILE)

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "guess_log" not in st.session_state:
    st.session_state.guess_log = []

# FIX: Persist latest feedback across reruns so hint/error doesn't disappear after submit.
if "last_hint" not in st.session_state:
    st.session_state.last_hint = None

if "last_error" not in st.session_state:
    st.session_state.last_error = None

st.sidebar.metric("Best Score", st.session_state.high_score)
st.sidebar.metric("Current Score", st.session_state.score)

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: Reset flow updated with Copilot to clear history and status for a true new game.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    # FIX: New rounds start from zero while the best score stays saved on disk.
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_log = []
    # FIX: Clear persisted feedback when starting a fresh round.
    st.session_state.last_hint = None
    st.session_state.last_error = None
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:

    # FIX: Reset previous feedback before processing a new guess.
    st.session_state.last_hint = None
    st.session_state.last_error = None

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.last_error = err
    else:
        st.session_state.attempts += 1

        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        distance = abs(guess_int - secret)
        temperature_label = ""
        temperature_emoji = ""
        if outcome != "Win":
            if distance <= 3:
                temperature_label = "Hot"
                temperature_emoji = "🔥"
            elif distance <= 10:
                temperature_label = "Warm"
                temperature_emoji = "🌤️"
            else:
                temperature_label = "Cold"
                temperature_emoji = "🧊"

        # FIX: Store hint in session_state so it survives Streamlit reruns.
        if outcome == "Win":
            st.session_state.last_hint = f"✅ {message}"
        else:
            st.session_state.last_hint = (
                f"{temperature_emoji} {temperature_label} — {message}"
            )

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        st.session_state.guess_log.append(
            {
                "Attempt": st.session_state.attempts,
                "Guess": guess_int,
                "Outcome": outcome,
                "Heat": temperature_label if outcome != "Win" else "Perfect",
                "Score After": st.session_state.score,
            }
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            # FIX: Agent Mode added persistent high-score tracking via a JSON file.
            st.session_state.high_score, is_new_high_score = update_high_score(
                HIGH_SCORE_FILE,
                st.session_state.score,
            )
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            if is_new_high_score:
                st.info(f"New high score saved: {st.session_state.high_score}")
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

if st.session_state.last_error:
    st.error(st.session_state.last_error)
elif show_hint and st.session_state.last_hint:
    if "Hot" in st.session_state.last_hint:
        st.success(st.session_state.last_hint)
    elif "Warm" in st.session_state.last_hint:
        st.info(st.session_state.last_hint)
    elif "Cold" in st.session_state.last_hint:
        st.warning(st.session_state.last_hint)
    elif "✅" in st.session_state.last_hint:
        st.success(st.session_state.last_hint)
    else:
        st.warning(st.session_state.last_hint)

if st.session_state.guess_log:
    st.subheader("📊 Game Session Summary")
    st.dataframe(st.session_state.guess_log, use_container_width=True, hide_index=True)

# FIX: Render debug panel after submit handling so history shows the latest guess immediately.
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
