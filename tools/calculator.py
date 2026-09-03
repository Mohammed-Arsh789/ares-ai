import ast
import operator

from tools.base import Tool
from tools.result import ToolResult


class CalculatorTool(Tool):
    name = "calculator"
    description = "Safely evaluates basic mathematical expressions."

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
        try:
            if not expression:
                raise ValueError("No expression supplied.")

            expression = expression.strip()

            if len(expression) > 100:
                raise ValueError("Expression is too long.")

            tree = ast.parse(
                expression,
                mode="eval",
            )

            result = self._evaluate(
                tree.body
            )

            return ToolResult.ok(
                self.name,
                result,
            )

        except Exception as error:
            return ToolResult.fail(
                self.name,
                error,
            )

    def _evaluate(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError(
                "Only numbers are allowed."
            )

        if isinstance(node, ast.BinOp):
            operation = self.OPERATORS.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError(
                    "Unsupported operator."
                )

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operation = self.OPERATORS.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError(
                    "Unsupported operator."
                )

            return operation(
                self._evaluate(node.operand)
            )

        raise ValueError(
            "Unsupported expression."
        )