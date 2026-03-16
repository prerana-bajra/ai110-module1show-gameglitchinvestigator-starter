# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - The hints provided were also contradictory, telling the player to go higher when the guess was already too high, and to go lower when the guess was too low.


- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  - When guess is greater than secret, it returned Too High but tells the player Go HIGHER.
  - When guess is lower, it returned Too Low but tells the player Go LOWER.
  - After the first game although the game was reinitiated the history was not cleared so it kept showing "Game over. Start a new game to play again." and the player could not play again.
  - Easy mode was 1 to 20, medium mode was 1 to 100 and hard mode was 1 to 50 which does not make sense as hard mode should be more difficult than medium mode.

--- 

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Copilot on this project.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - When I was trying to fix the hints, I asked Copilot to suggest a way to change the hints. It suggested changing the hint for when the guess is greater than the secret number to "Go LOWER" and the hint for when the guess is lower than the secret number to "Go HIGHER". I implemented this change and verified the result by running the game and testing different guesses to see if the hints were now correct.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - The AI suggested to set the status to "playing" after reset however it did not clear the history and the guesses of the new game kept getting added up.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I decided a bug was really fixed by running the game and testing the specific functionality that was supposed to be fixed.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - I ran a manual test where I made a guess that was too high and checked if the hint was correct. I also made a guess that was too low and checked the hint for that as well. This showed me that the hints were now correct after I implemented the changes suggested by Copilot.
- Did AI help you design or understand any tests? How?
  - AI helped me understand how to test the game by suggesting that I should run the game and make different guesses to see if the hints were correct. It also helped me understand that I should test the reset functionality by starting a new game and if the status was set to "playing".

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  - The secret number kept changing in the original app because it was not initialized properly
- What change did you make that finally gave the game a stable secret number?
  - I initialized the secret number in the reset function and made sure it was only set once when the game starts. This way, the secret number remains stable throughout the game until it is reset again.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  - One habit I want to reuse is to always run the game and test the specific functionality that I am trying to fix or implement. This helps me verify that my changes are working as intended and that I have actually fixed the bug.
- What is one thing you would do differently next time you work with AI on a coding task?
  - Next time I work with AI on a coding task, I would be more critical of the suggestions provided by the AI and not just implement them blindly. I would take the time to understand why the AI is suggesting a certain change and how it fits into the overall codebase before implementing it. This way, I can avoid implementing suggestions that may be incorrect or misleading.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - This project made me realize that while AI can be a helpful tool for generating code and providing suggestions, it is not infallible and can sometimes provide incorrect or misleading suggestions. It is important to critically evaluate the suggestions provided by AI and understand the underlying code before implementing any changes. AI should be seen as a teammate that can assist in the coding process, but ultimately, the developer is responsible for the final code and its functionality.

---

## Challenge 5: AI Model Comparison (Logic Bug Fix)

I compared fixes for the reversed hint bug ("Too High" / "Too Low" messaging) from Copilot Chat and ChatGPT. Both models identified the root issue correctly, but Copilot's suggestion fit the existing code style more directly and was quicker to paste into place in `logic_utils.py`.

For readability, Copilot gave the cleaner minimal diff, while ChatGPT gave a more narrative explanation. ChatGPT was slightly stronger at explaining the "why" behind the bug and how to validate the fix with test cases, but Copilot produced the more immediately usable fix for this codebase.
