# interpreter.py

from parser import *
from lexer import *
import sys

class BuiltinFunction:
    def __init__(self, name):
        self.name = name

class BuiltinType:
    """'int', 'string' 같은 내장 타입을 나타내는 객체"""
    def __init__(self, name):
        self.name = name
        
class Interpreter:
    def __init__(self):
        self.GLOBAL_SCOPE = {
            # 내장 객체 및 함수를 미리 정의
            'console': {
                'print': BuiltinFunction('print'),
                'read': BuiltinFunction('read')
            },
            'int': BuiltinType('int'),
            'string': BuiltinType('string')
        }

    def visit(self, node):
        """
        AST 노드의 종류를 보고, 그에 맞는 처리 메소드를 호출해주는 역할.
        예: VarDeclNode를 만나면 'visit_VarDeclNode' 메소드를 호출.
        """
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def no_visit_method(self, node):
        """방문할 메소드가 없을 경우 오류를 발생시킵니다."""
        raise Exception(f"No visit_{type(node).__name__} method defined")
    
    def visit_MemberAccessNode(self, node):
        """console.print 같은 객체 멤버 접근을 처리합니다."""
        obj = self.visit(node.object)
        if isinstance(obj, dict):
            return obj.get(node.member.value)
        raise Exception(f"Cannot access member '{node.member.value}'")

    def visit_MethodCallNode(self, node):
        """메소드/함수 호출을 처리합니다. int(), string() 포함."""
        callee = self.visit(node.callee)
        args = [self.visit(arg_node) for arg_node in node.args]

        # 1. 내장 타입 함수 호출 처리 (예: int("123") 또는 int())
        if isinstance(callee, BuiltinType):
            type_name = callee.name
            if len(args) == 0:
                return callee
            elif len(args) == 1:
                if type_name == 'int':
                    return int(args[0])
                if type_name == 'string':
                    return str(args[0])
            else:
                raise Exception(f"{type_name}() takes 0 or 1 arguments, but {len(args)} were given.")
            
        # 2. 내장 일반 함수 호출 처리 (예: console.read)
        if isinstance(callee, BuiltinFunction):
            func_name = callee.name
            if func_name == 'print':
                print(*args)
                return None
            elif func_name == 'read':
                # args[0]는 이제 BuiltinType 객체 (예: int()의 반환값)
                input_type = args[0] if args else BuiltinType('string')
                if not isinstance(input_type, BuiltinType):
                    raise Exception("Argument to console.read() must be a type like int() or string().")
                
                user_input = input() # 프롬프트 없이 입력받기
                if input_type.name == 'int':
                    try:
                        return int(user_input)
                    except ValueError:
                        raise Exception(f"Invalid input: Could not convert '{user_input}' to int.")
                else: # 기본값은 string
                    return str(user_input)

        raise Exception("Not a callable function.")
    
    def visit_BooleanNode(self, node):
        """BooleanNode를 처리하여 True 또는 False 값을 반환합니다."""
        return node.value
    
    def visit_UnaryOpNode(self, node):
        op_type = node.op.type
        if op_type == NOT:
            # expr을 평가한 후, 논리적으로 뒤집습니다.
            return not self.visit(node.expr)

    def visit_BinOpNode(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        op_type = node.op.type

        if op_type == PLUS:
            if isinstance(left_val, str) or isinstance(right_val, str): return str(left_val) + str(right_val)
            else: return left_val + right_val
        elif op_type == MINUS: return left_val - right_val
        elif op_type == MUL: return left_val * right_val
        elif op_type == DIV:
            if right_val == 0: raise Exception("Runtime Error: Division by zero.")
            return left_val / right_val
        
        # 비교 연산
        elif op_type == EQ: return left_val == right_val
        elif op_type == NEQ: return left_val != right_val
        elif op_type == LT: return left_val < right_val
        elif op_type == GT: return left_val > right_val
        elif op_type == LTE: return left_val <= right_val
        elif op_type == GTE: return left_val >= right_val

        # 논리 연산
        elif op_type == AND: return left_val and right_val
        elif op_type == OR: return left_val or right_val

    def visit_StringNode(self, node):
        """StringNode를 처리하여 최종 문자열을 만듭니다."""
        final_string = ""
        for part in node.parts:
            if isinstance(part, str):
                final_string += part
            elif isinstance(part, Token) and part.type == ID:
                # 보간된 변수의 값을 찾아 문자열로 변환하여 더합니다.
                var_name = part.value
                var_value = self.GLOBAL_SCOPE.get(var_name)
                if var_value is None:
                    raise NameError(f"Error: Variable '{var_name}' is not defined.")
                final_string += str(var_value)
        return final_string


    def visit_ProgramNode(self, node):
        """프로그램 전체를 실행합니다."""
        for statement in node.statements:
            self.visit(statement)

    def visit_VarDeclNode(self, node):
        """변수 선언문을 처리합니다."""
        var_name = node.var_name
        # 변수에 할당될 값을 얻기 위해, 연결된 value_node를 다시 visit합니다.
        value = self.visit(node.value_node)
        # 변수 이름과 계산된 값을 GLOBAL_SCOPE에 저장합니다.
        self.GLOBAL_SCOPE[var_name] = value

    def visit_VarAccessNode(self, node):
        """변수 또는 내장 타입/함수 이름을 찾아 값을 반환합니다."""
        name = node.var_name
        value = self.GLOBAL_SCOPE.get(name)
        if value is None:
            raise NameError(f"Error: Variable '{name}' is not defined.")
        return value

    def visit_NumberNode(self, node):
        """숫자 자체를 처리합니다."""
        return node.value

    def interpret(self, tree):
        """
        Interpreter의 메인 진입점입니다.
        최상위 AST 노드(ProgramNode)를 받아 실행을 시작합니다.
        """
        if tree is None:
            return ''
        return self.visit(tree)