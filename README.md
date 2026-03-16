# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
   This project is a Streamlit number guessing game where the player chooses a difficulty, tries to guess the secret number within a limited number of attempts, and earns or loses points based on each guess.
- [x] Detail which bugs you found.
   The main bugs were incorrect higher/lower hints, unstable game feedback that disappeared after submitting a guess, delayed history updates in the debug panel, mismatched difficulty ranges, and scoring issues that did not consistently reward wins or penalize incorrect guesses.
- [x] Explain what fixes you applied.
   I fixed the hint logic in `logic_utils.py`, corrected the difficulty ranges, updated the score calculation to reward earlier wins and apply consistent penalties, and improved Streamlit state handling in `app.py` so the secret number stays stable, feedback persists across reruns, and history updates immediately after each submit.

## 📸 Demo

- [x] [Insert a screenshot of your fixed, winning game here]

![alt text](<image1.png>)



## 🚀 Stretch Features


- [x] Challenge 1: Advanced Edge-Case Testing

![alt text](<image2.png>)
- [x] Challenge 2: Feature Expansion via Agent Mode
   I used Agent Mode to plan and implement a persistent High Score feature. The agent helped break the work into logic, UI, persistence, and testing tasks, then added JSON-backed save/load helpers in `logic_utils.py`, updated `app.py` to display the best score in the sidebar, and saved a new high score whenever a completed game beat the previous best. The agent contribution is also noted directly in the code comments around the high-score state and save flow.
   
- [x] Challenge 4: Enhanced Game UI
   I improved the player experience with structured, color-coded feedback and emoji-based heat hints (Hot/Warm/Cold), plus a summary table showing each attempt, outcome, and running score for the current game session.

![Enhanced Game UI](![alt text](image3.png))
