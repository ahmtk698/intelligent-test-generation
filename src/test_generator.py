import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq

API_KEY = os.getenv("GROQ_API_KEY")


def generate_tests_with_ai(func_name, func_code):
    try:
        client = Groq(api_key=API_KEY)
        
        prompt_text = f"""
        You are an Expert Python QA Engineer. Write `pytest` tests for the function `{func_name}`.
        
        CONTEXT:
        The following imports are ALREADY present in the global scope. DO NOT re-import them:
        - `import pytest`
        - `import math`
        - `from hypothesis import given, strategies as st`
        - `from samples... import {func_name}`
        
        CRITICAL RULES (STRICT):
        1. **Just Tests:** Output ONLY the test functions.
        2. **NO `import st`:** NEVER write `import st`. `st` is already imported.
        3. **SYNTAX SAFETY:** DOUBLE CHECK your parentheses `()`. Ensure every opening bracket has a closing bracket. Do not write complex one-liners.
        4. **Hypothesis Logic:** - If using `st.floats`, SET `allow_nan=False` if min/max are used.
           - For lists of dicts, use `st.lists(st.fixed_dictionaries(...))` structure, it is safer.
        5. **Zero Division:** `x / 0` ALWAYS raises `ZeroDivisionError`.
        
        SPECIFIC FIXES:
        A) **calculate_cart_total:** - Use `pytest.approx(expected, abs=0.1)`.  
           - Return 0.0 for NaN.
           - For Hypothesis: `st.lists(st.fixed_dictionaries({{'price': st.floats(min_value=0, max_value=1000, allow_nan=False), 'qty': st.floats(min_value=0, max_value=100, allow_nan=False)}}))`
           
        B) **reverse_words:** Simple inputs only ("hello world").
        C) **mask_email:** `test_mask_email_no_at_symbol` input MUST NOT contain `@`.
        D) **is_palindrome:** Simple words ("radar").
        E) **is_even:** `is_even(float('inf'))` should expect `False`.
        F) divide: In Hypothesis tests, the divisor `b` must never be 0 (use `st.floats(...).filter(lambda x: x != 0.0)`), and add a separate test asserting that `divide(x, 0)` raises `ZeroDivisionError`.

        Function Details:
        Name: {func_name}
        Code:
        {func_code}
        
        Output ONLY executable Python code. No markdown.
        """
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_text}],
            model="llama-3.3-70b-versatile", 
            temperature=0.1, 
        )

        text = chat_completion.choices[0].message.content
        cleaned_text = text.replace("```python", "").replace("```", "").strip()
        
        # Ekstra Güvenlik: Hatalı importları temizle
        lines = cleaned_text.split('\n')
        filtered_lines = [
            line for line in lines 
            if "import st" not in line 
            and "import numpy" not in line
        ]
        return '\n'.join(filtered_lines)

    except Exception as e:
        return f"# Error generating tests with Groq: {e}"
