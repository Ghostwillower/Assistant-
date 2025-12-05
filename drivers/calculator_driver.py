"""
Calculator Driver

Provides basic arithmetic calculation capabilities.
"""

from driver_interface import DriverInterface
from typing import Dict, Any


class CalculatorDriver(DriverInterface):
    """
    Driver for performing basic arithmetic operations.
    """
    
    def __init__(self):
        super().__init__(
            name="Calculator",
            version="1.0.0",
            description="Basic arithmetic calculator"
        )
    
    def initialize(self) -> bool:
        """
        Initialize the calculator driver.
        
        Returns:
            bool: True if successful
        """
        print("Calculator driver initialized")
        return True
    
    def execute(self, command: str, *args, **kwargs) -> Any:
        """
        Execute a calculator command.
        
        Args:
            command: Command to execute (add, subtract, multiply, divide, eval)
            *args: Arguments for the command
            
        Returns:
            Result of the calculation
        """
        if command == "add":
            return self._add(args[0] if args else "")
        elif command == "subtract":
            return self._subtract(args[0] if args else "")
        elif command == "multiply":
            return self._multiply(args[0] if args else "")
        elif command == "divide":
            return self._divide(args[0] if args else "")
        elif command == "eval":
            return self._eval(args[0] if args else "")
        else:
            return f"Unknown command: {command}"
    
    def get_commands(self) -> Dict[str, str]:
        """
        Get available calculator commands.
        
        Returns:
            Dict[str, str]: Command descriptions
        """
        return {
            "add": "Add numbers (e.g., '5+3' or '1+2+3')",
            "subtract": "Subtract numbers (e.g., '10-3')",
            "multiply": "Multiply numbers (e.g., '4*5')",
            "divide": "Divide numbers (e.g., '20/4')",
            "eval": "Evaluate expression (e.g., '(2+3)*4')"
        }
    
    def shutdown(self) -> bool:
        """
        Shutdown the calculator driver.
        
        Returns:
            bool: True if successful
        """
        print("Calculator driver shutdown")
        return True
    
    def _add(self, expression: str) -> str:
        """Add numbers from expression like '5+3' or '1+2+3'"""
        try:
            numbers = [float(x.strip()) for x in expression.split('+')]
            result = sum(numbers)
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _subtract(self, expression: str) -> str:
        """Subtract numbers from expression like '10-3'"""
        try:
            # For more complex expressions with negative numbers, use eval command
            # This simple version handles basic 'a-b' format
            parts = expression.split('-')
            
            # Handle simple case: "a-b"
            if len(parts) == 2 and parts[0] and parts[1]:
                result = float(parts[0].strip()) - float(parts[1].strip())
                return f"{expression} = {result}"
            # Handle negative first number: "-a-b" 
            elif len(parts) == 3 and not parts[0] and parts[1] and parts[2]:
                result = -float(parts[1].strip()) - float(parts[2].strip())
                return f"{expression} = {result}"
            else:
                return "Error: For complex expressions use 'eval' command"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _multiply(self, expression: str) -> str:
        """Multiply numbers from expression like '4*5'"""
        try:
            numbers = [float(x.strip()) for x in expression.split('*')]
            result = 1
            for num in numbers:
                result *= num
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _divide(self, expression: str) -> str:
        """Divide numbers from expression like '20/4'"""
        try:
            numbers = [float(x.strip()) for x in expression.split('/')]
            result = numbers[0]
            for num in numbers[1:]:
                if num == 0:
                    return "Error: Division by zero"
                result /= num
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _eval(self, expression: str) -> str:
        """Evaluate a mathematical expression"""
        try:
            # Only allow safe mathematical operations
            allowed_chars = set('0123456789+-*/()., ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"
            
            # Limit expression length to prevent resource exhaustion
            if len(expression) > 200:
                return "Error: Expression too long (max 200 characters)"
            
            # Use ast for safer evaluation
            import ast
            import operator
            
            # Allowed operators for safe evaluation
            ops = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos,
            }
            
            def eval_expr(node):
                if isinstance(node, ast.Num):  # <number>
                    return node.n
                elif isinstance(node, ast.Constant):  # Python 3.8+
                    return node.value
                elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                    return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
                elif isinstance(node, ast.UnaryOp):  # <operator> <operand>
                    return ops[type(node.op)](eval_expr(node.operand))
                else:
                    raise TypeError(f"Unsupported operation: {type(node)}")
            
            tree = ast.parse(expression, mode='eval')
            result = eval_expr(tree.body)
            return f"{expression} = {result}"
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception as e:
            return f"Error: {str(e)}"
