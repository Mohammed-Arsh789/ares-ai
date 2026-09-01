import ast
import operator

from tools.base import Tool


class CalculatorTool(Tool):
    name = "calculator"
    description = "Performs basic arithmetic calculations safely."

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def run(self, expression: str):
        if not expression:
            raise ValueError("No expression provided.")

        expression = expression.strip()

        if len(expression) > 100:
            raise ValueError("Expression is too long.")

        try:
            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body)

        except ZeroDivisionError:
            raise ValueError("Division by zero is not allowed.")

        except (SyntaxError, ValueError, TypeError):
            raise ValueError("Invalid mathematical expression.")

        return result

    def _evaluate(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numbers are allowed.")

        if isinstance(node, ast.BinOp):
            operation = self.OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operation = self.OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator.")

            return operation(self._evaluate(node.operand))

        raise ValueError("Unsupported expression.")