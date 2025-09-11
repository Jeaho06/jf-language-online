# parser.py
from lexer import *


class ASTNode:
    """모든 AST 노드의 부모 클래스"""
    pass

class ProgramNode(ASTNode):
    """프로그램 전체를 나타내는 최상위 노드. 여러 개의 문장을 자식으로 가집니다."""
    def __init__(self, statements):
        self.statements = statements

class VarDeclNode(ASTNode):
    """변수 선언문을 나타내는 노드. 예: x is int(10)."""
    def __init__(self, var_name, var_type, value_node):
        self.var_name = var_name
        self.var_type = var_type
        self.value_node = value_node

class NumberNode(ASTNode):
    """숫자 값을 나타내는 노드."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class VarAccessNode(ASTNode):
    """변수 값을 사용(참조)하는 것을 나타내는 노드."""
    def __init__(self, token):
        self.token = token
        self.var_name = token.value

class BinOpNode(ASTNode):
    """이항 연산(Binary Operation)을 나타내는 노드. 예: 3 + 5"""
    def __init__(self, left, op_token, right):
        self.left = left
        self.op = op_token
        self.right = right

class StringNode(ASTNode):
    """문자열 리터럴을 나타내는 노드. 보간을 위해 여러 부분으로 나뉠 수 있음."""
    def __init__(self, parts):
        self.parts = parts

class BooleanNode(ASTNode):
    """true 또는 false 값을 나타내는 노드"""
    def __init__(self, token): self.token=token; self.value=token.value

class UnaryOpNode(ASTNode):
    """단항 연산 (예: not true)을 나타내는 노드"""
    def __init__(self, op_token, expr): self.op=op_token; self.expr=expr

class MemberAccessNode(ASTNode):
    """객체의 멤버에 접근하는 것을 나타내는 노드 (예: console.print)"""
    def __init__(self, object, member):
        self.object = object
        self.member = member

class MethodCallNode(ASTNode):
    """메소드를 호출하는 것을 나타내는 노드 (예: print("Hello"))"""
    def __init__(self, callee, args):
        self.callee = callee # 호출되는 대상 (예: MemberAccessNode)
        self.args = args     # 전달되는 인자 리스트

# --- 2. Parser 클래스 구현 ---
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.peek_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.peek_token
            self.peek_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Syntax Error: Expected {token_type}, found {self.current_token.type}")

    def primary(self):
        """가장 우선순위가 높은 표현 단위"""
        token = self.current_token
        if token.type == INTEGER: self.eat(INTEGER); return NumberNode(token)
        elif token.type == STRING: self.eat(STRING); return StringNode(token.value)
        elif token.type == TRUE: self.eat(TRUE); return BooleanNode(token)
        elif token.type == FALSE: self.eat(FALSE); return BooleanNode(token)
        elif token.type == ID: self.eat(ID); return VarAccessNode(token)
        elif token.type == LPAREN: self.eat(LPAREN); node = self.expr(); self.eat(RPAREN); return node
        raise Exception("Syntax Error: Invalid primary expression")

    def call(self):
        """메소드 호출 시 쉼표(,)로 구분된 여러 인자를 파싱합니다."""
        node = self.primary()
        while True:
            if self.current_token.type == LPAREN:
                self.eat(LPAREN)
                args = []
                if self.current_token.type != RPAREN:
                    args.append(self.expr())
                    while self.current_token.type == COMMA: # 쉼표로 인자 구분
                        self.eat(COMMA)
                        args.append(self.expr())
                self.eat(RPAREN)
                node = MethodCallNode(callee=node, args=args)
            elif self.current_token.type == DOT and self.peek_token.type in (ID, PRINT):
                self.eat(DOT)
                member = self.current_token
                self.eat(member.type)
                node = MemberAccessNode(object=node, member=member)
            else:
                break
        return node
    
    def factor(self):
        token = self.current_token
        if token.type == NOT:
            self.eat(NOT)
            return UnaryOpNode(op_token=token, expr=self.factor())
        return self.call()
        
    def term(self): # 곱셈/나눗셈
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            op_token = self.current_token
            if op_token.type == MUL: self.eat(MUL)
            elif op_token.type == DIV: self.eat(DIV)
            node = BinOpNode(left=node, op_token=op_token, right=self.factor())
        return node

    def arith_expr(self): # 덧셈/뺄셈
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            op_token = self.current_token
            if op_token.type == PLUS: self.eat(PLUS)
            elif op_token.type == MINUS: self.eat(MINUS)
            node = BinOpNode(left=node, op_token=op_token, right=self.term())
        return node

    def comparison(self): # 비교 연산
        node = self.arith_expr()
        while self.current_token.type in (LT, GT, LTE, GTE):
            op_token = self.current_token; self.eat(op_token.type)
            node = BinOpNode(left=node, op_token=op_token, right=self.arith_expr())
        return node

    def equality(self): # 동등 비교 연산
        node = self.comparison()
        while self.current_token.type in (EQ, NEQ):
            op_token = self.current_token; self.eat(op_token.type)
            node = BinOpNode(left=node, op_token=op_token, right=self.comparison())
        return node
    
    def logical_and(self):
        node = self.equality()
        while self.current_token.type == AND:
            op_token = self.current_token; self.eat(AND)
            node = BinOpNode(left=node, op_token=op_token, right=self.equality())
        return node

    def logical_or(self):
        node = self.logical_and()
        while self.current_token.type == OR:
            op_token = self.current_token; self.eat(OR)
            node = BinOpNode(left=node, op_token=op_token, right=self.logical_and())
        return node
    
    def expr(self):
        """표현식 파싱의 시작점"""
        return self.logical_or()
    
    def variable_declaration(self):
        """'is int(...)' 문법을 제거하여 단순화합니다."""
        var_name = self.current_token.value; self.eat(ID)
        self.eat(IS)
        value_node = self.expr() # is 다음에는 항상 표현식이 옴
        var_type_token = Token('UNKNOWN_TYPE', 'unknown')
        return VarDeclNode(var_name, var_type_token, value_node)

    def statement(self):
        """하나의 문장을 파싱합니다."""
        # ID로 시작하는 것은 변수 선언(is)이거나 메소드 호출(.)일 수 있으므로,
        # 일단 표현식(expr)으로 끝까지 파싱합니다.
        node = self.expr()

        # 만약 파싱이 끝난 뒤 다음 토큰이 'is' 라면,
        # 이것은 사실 변수 선언문의 일부였습니다.
        if self.current_token.type == IS:
            # node가 변수 이름(VarAccessNode)이 맞는지 확인
            if not isinstance(node, VarAccessNode):
                raise Exception("Syntax Error: 'is' keyword can only follow a variable name.")
            
            # 'is' 키워드를 소모하고, 등호(=) 뒤의 값을 다시 파싱합니다.
            self.eat(IS)
            value_node = self.expr()
            
            # 최종적으로 VarDeclNode를 완성하여 반환합니다.
            var_type_token = Token('UNKNOWN_TYPE', 'unknown') # 임시 타입
            return VarDeclNode(node.var_name, var_type_token, value_node)
        
        # 다음 토큰이 'is'가 아니라면, 원래 파싱했던 표현식(메소드 호출 등)이 맞습니다.
        return node
        
    def parse(self):
        """콜론(:)으로 연결된 문장 목록을 파싱합니다."""
        all_statements = []
        while self.current_token.type != EOF:
            while self.current_token.type == NEWLINE: self.eat(NEWLINE)
            if self.current_token.type == EOF: break

            line_statements = [self.statement()]
            while self.current_token.type == COLON: # 쉼표 대신 콜론으로 문장 연결
                self.eat(COLON)
                line_statements.append(self.statement())
            
            all_statements.extend(line_statements)

            # 한 줄의 끝은 점(.), 줄바꿈(NEWLINE), 또는 파일의 끝(EOF)이어야 함
            if self.current_token.type == DOT:
                self.eat(DOT)
                # 점 뒤에는 반드시 줄바꿈이나 파일의 끝이 와야 함
                if self.current_token.type not in (NEWLINE, EOF):
                     raise Exception("Syntax Error: Expected a newline after '.'")
            elif self.current_token.type not in (NEWLINE, EOF):
                raise Exception(f"Syntax Error: Unexpected token '{self.current_token.value}' at the end of a line.")

        return ProgramNode(all_statements)