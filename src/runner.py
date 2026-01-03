from src.test_generator import generate_tests

def write_tests(functions):
    content = "from samples.sample_code import *\n\n"

    for test_block in generate_tests(functions):
        content += test_block + "\n"

    with open("tests/test_generated.py", "w", encoding="utf-8") as f:
        f.write(content)
