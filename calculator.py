import ast
import operator as op

_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval(node):
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPS:
            return _ALLOWED_OPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPS:
            return _ALLOWED_OPS[op_type](operand)
    raise ValueError("Unsupported expression")

def calculate(expr: str) -> str:
    try:
        node = ast.parse(expr, mode='eval').body
        result = _eval(node)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
