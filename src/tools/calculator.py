import re
import numexpr
from langchain.tools import tool


def validate_math_expression(expression: str) -> bool:
    """
    Valida se a expressão contém apenas operações matemáticas seguras.
    
    Args:
        expression: String contendo a expressão matemática
        
    Returns:
        True se a expressão é segura, False caso contrário
    """
    expr_clean = expression.replace(" ", "")
    safe_pattern = r'^[\d+\-*/().\s^]+$'
    
    if not re.match(safe_pattern, expr_clean):
        return False
    
    dangerous_keywords = ['import', 'exec', 'eval', '__', 'open', 'file', 'input']
    expr_lower = expression.lower()
    for keyword in dangerous_keywords:
        if keyword in expr_lower:
            return False
    
    if not re.search(r'\d', expr_clean):
        return False
    
    return True


@tool
def calculator(expression: str) -> str:
    """
    Calcula o resultado de uma expressão matemática de forma segura.
    
    Esta ferramenta utiliza numexpr para avaliação segura de expressões matemáticas,
    evitando o uso inseguro de eval() que poderia permitir Code Injection.
    
    Args:
        expression: Expressão matemática a ser calculada (ex: "128 * 46", "2**10", "(5+3)/2")
        
    Returns:
        String contendo o resultado numérico da expressão
        
    Raises:
        ValueError: Se a expressão não for válida ou contiver caracteres não permitidos
    """
    if not validate_math_expression(expression):
        raise ValueError(
            f"Expressão inválida ou insegura: '{expression}'. "
            "Apenas operações matemáticas básicas são permitidas."
        )
    
    try:
        expr_normalized = expression.replace("^", "**")
        result = numexpr.evaluate(expr_normalized)
        
        if isinstance(result, (int, float)):
            if isinstance(result, float) and (result > 1e10 or (result < 1e-4 and result > 0)):
                return f"{result:.10e}"
            return str(result)
        else:
            return str(result)
            
    except Exception as e:
        raise ValueError(f"Erro ao calcular a expressão '{expression}': {str(e)}")
