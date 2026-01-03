import ast

def analyze_file(file_path):
    """
    Analysis Agent: Python kaynak kodunu analiz eder ve fonksiyon bazlı parçalar.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
        tree = ast.parse(source)

    functions_data = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno - 1
            end_line = node.end_lineno
            func_code = "\n".join(source.splitlines()[start_line:end_line])
            functions_data.append({
                "name": node.name,
                "code": func_code
            })
    return functions_data