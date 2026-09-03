import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def calculate(expression):

    def evaluate(node):

        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Invalid number.")

        if isinstance(node, ast.BinOp):

            left = evaluate(node.left)
            right = evaluate(node.right)

            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Operator not allowed.")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):

            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Operator not allowed.")

            return operation(evaluate(node.operand))

        raise ValueError("Expression not allowed.")

    tree = ast.parse(expression, mode="eval")

    return evaluate(tree.body)