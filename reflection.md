# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The game's structure and layout looked good and everything seemed like it was fine. The game had a settings navigation menu one the left which can be used to change the difficulty level. The game is titled Game Glitch Investigator and then has the text box to input the guesses in.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| # | Input | Expected Behavior | Actual Behavior | Console Output / Error |
|---|-------|-------------------|-----------------|------------------------|
| 1 | Guess > Secret (e.g., guess 70 when secret is 50) | Hint says "Go LOWER" | Hint says "Go HIGHER" on even attempts due to string conversion causing a TypeError fallback | Logical error |
| 2 | Change difficulty to Easy | Range displays "1 to 20" and stays consistent | Range text always shows "1 to 100" regardless of difficulty | Logical error |
| 3 | Click "New Game" after playing | Score resets to 0 and history clears | Score and history from the previous game carry over | Logical error |
| 4 | Wrong "Too High" guess on even attempt (e.g., attempt 2) | Score decreases by 5 | Score increases by 5 — wrong guesses are rewarded | Logical error in `update_score` |
| 5 | Submit empty or non-numeric input | Attempt count stays the same | Attempt count increments, wasting a turn | Logical error — attempt increments before validation |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I just used Claude code.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

From:
        g = str(guess)
        if g == secret:
To:
        s = int(secret)
        if guess == s:
            return "Win", "🎉 Correct!"

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I didn't really experience any misleading suggestions.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I verified each fix by running the app and manually reproducing the original broken behavior. For example, after fixing the scoring bug I entered a guess higher than the secret on both odd and even attempts and confirmed the score decreased by 5 each time. I also ran `pytest tests/test_game_logic.py` to confirm all 22 unit tests passed, including the new tests I wrote specifically to target the scoring bug.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

I ran `test_too_high_should_always_penalize`, which calls `update_score(50, "Too High", 2)` and asserts the result is less than 50. Before the fix, this test failed because the buggy code returned 55 (rewarding +5 on even attempts). After removing the attempt-parity check, the test passed with a score of 45, confirming the penalty is now applied consistently.

- Did AI help you design or understand any tests? How?

Yes, I used Claude Code to identify the logical errors in the codebase and then generate targeted pytest cases. Claude analyzed the `update_score` function and flagged the inconsistent behavior on even vs odd attempts, then wrote tests that assert the correct behavior — which exposed the bug by failing against the unfixed code.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you interact with a Streamlit app — clicking a button, typing in a text box, changing a dropdown — the entire Python script re-executes from top to bottom. This means any regular variable you define gets reset to its initial value on every interaction. To keep data persistent across these reruns, Streamlit provides `st.session_state`, which is basically a dictionary that survives reruns. You store things like the secret number, attempt count, and score in `st.session_state` so they don't get wiped out every time the user clicks something.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Writing tests that assert the *correct* behavior before fixing a bug. By writing `test_too_high_should_always_penalize` first, I had a clear, automated way to confirm when the bug was actually fixed. This "test-first" approach gave me confidence that the fix worked and prevented me from accidentally re-introducing the bug later.

- What is one thing you would do differently next time you work with AI on a coding task?

I would ask the AI to explain *why* a piece of code might be wrong rather than just asking it to find bugs. Understanding the root cause (like why comparing an int to a string fails in Python 3) helps me catch similar issues on my own in the future, rather than relying on AI to spot them every time.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

AI-generated code can look syntactically correct and pass a quick review while hiding subtle logical bugs that only surface during real usage. This project taught me that AI is a powerful drafting tool, but human review, manual testing, and targeted unit tests are essential to catch the kind of errors that AI introduces but doesn't flag.
