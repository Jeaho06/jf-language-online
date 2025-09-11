# lexer.py

# --- 1. 토큰 타입 정의 ---
# 우리 언어가 인식할 단어(토큰)의 종류를 미리 정해둡니다.
# 파일의 끝을 의미하는 EOF(End-Of-File)도 중요한 토큰입니다.
INTEGER   = 'INTEGER'   # 숫자 (예: 10)
STRING    = 'STRING'    # 문자열 (예: "hello")
ID        = 'ID'        # 변수 이름 (Identifier, 예: x)
IS        = 'IS'        # 'is' 키워드
PRINT     = 'PRINT'     # 'print' 키워드
INT_TYPE  = 'INT_TYPE'  # 'int' 타입 키워드
LPAREN    = 'LPAREN'    # 왼쪽 괄호 '('
RPAREN    = 'RPAREN'    # 오른쪽 괄호 ')'
DOT       = 'DOT'       # 문장 끝 마침표 '.'
EOF       = 'EOF'       # 코드의 끝
PLUS      = 'PLUS'      # +
MINUS     = 'MINUS'     # -
MUL       = 'MUL'       # *
DIV       = 'DIV'       # /
TRUE      = 'TRUE'      # true
FALSE     = 'FALSE'     # false 
AND      = 'AND'       # and
OR       = 'OR'        # or
NOT      = 'NOT'       # not    
EQ       = 'EQ'        # ==
NEQ      = 'NEQ'       # !=
LT       = 'LT'        # <
LTE      = 'LTE'       # <=
GT       = 'GT'        # >  
GTE      = 'GTE'       # >=
COMMA    = 'COMMA'     # ,
NEWLINE   = 'NEWLINE'   # 줄바꿈
COLON    = 'COLON'     # : ':'

class Token:
    """
    인식된 단어(토큰)를 표현하는 클래스입니다.
    종류(type)와 실제 값(value)을 가집니다.
    예: Token(INTEGER, 10)
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

# --- 2. Lexer 클래스 구현 ---
class Lexer:
    def __init__(self, text):
        self.text = text         # 분석할 전체 코드
        self.pos = 0             # 현재 분석 중인 위치
        self.current_char = self.text[self.pos] if self.text else None # 현재 위치의 글자

    def advance(self):
        """한 글자 앞으로 이동합니다."""
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None # 코드의 끝에 도달

    def peek(self):
        """다음 글자를 '엿보기'만 합니다. (위치 이동은 안 함)"""
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        else:
            return None

    def skip_whitespace(self):
        """공백, 탭, 줄바꿈 등 의미 없는 문자들을 건너뜁니다."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """숫자를 읽습니다. 소수점과 정수를 구분하는 핵심 로직이 여기에 있습니다."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        # 여기서 '엿보기' 규칙을 사용합니다!
        if self.current_char == '.' and self.peek() is not None and self.peek().isdigit():
            # 마침표 뒤에 숫자가 오면 소수점으로 처리 (지금은 구현하지 않음)
            # 이 부분은 나중에 float 타입을 추가할 때 확장할 것입니다.
            # 지금은 정수만 처리하므로, 일단 오류를 발생시키겠습니다.
            raise Exception("Float type is not yet supported.")
        
        return int(result)

    def _id(self):
        """키워드 인식 부분을 수정합니다."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char; self.advance()
        
        # 'int'는 이제 일반 ID이므로 키워드 목록에서 제거합니다.
        RESERVED_KEYWORDS = {
            'is': Token(IS, 'is'), 'print': Token(PRINT, 'print'), # 'print'는 console.print를 위해 임시 유지
            'true': Token(TRUE, True), 'false': Token(FALSE, False),
            'and': Token(AND, 'and'), 'or': Token(OR, 'or'), 'not': Token(NOT, 'not'),
        }
        return RESERVED_KEYWORDS.get(result.lower(), Token(ID, result))
    
    def skip_comment(self):
        """'note:' 주석을 발견했을 때, 해당 줄의 끝까지 건너뛰는 메소드"""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.skip_whitespace() # 줄바꿈 문자 뒤의 공백도 건너뛸 수 있도록 추가
    
    def string(self):
        """문자열 리터럴을 파싱합니다 (보간 포함)."""
        result_parts = []
        current_part = ''
        
        # 시작 따옴표 확인 (", ', """)
        quote = self.current_char
        if self.text[self.pos:self.pos+3] == '"""':
            quote = '"""'
            self.advance()
            self.advance()
            self.advance()
        else:
            self.advance() # 따옴표 한 칸 이동

        while self.current_char is not None:
            # 종료 따옴표 확인
            if quote == '"""' and self.text[self.pos:self.pos+3] == '"""':
                self.advance(); self.advance(); self.advance()
                break
            if self.current_char == quote and quote != '"""':
                self.advance()
                break
            
            # 이스케이프 시퀀스 처리
            if self.current_char == '\\' and self.peek() == 'n':
                current_part += '\n'
                self.advance(); self.advance()
                continue
            
            # 문자열 보간 처리: @{...}
            if self.current_char == '@' and self.peek() == '{':
                if current_part:
                    result_parts.append(current_part)
                current_part = ''
                
                self.advance(); self.advance() # @{ 건너뛰기
                
                # 변수 이름 파싱
                var_name = ''
                while self.current_char is not None and self.current_char != '}':
                    var_name += self.current_char
                    self.advance()
                self.advance() # } 건너뛰기
                
                result_parts.append(Token(ID, var_name.strip()))
                continue

            current_part += self.current_char
            self.advance()
        
        if current_part:
            result_parts.append(current_part)
        
        return result_parts
    

    def skip_whitespace(self):
        """이제 줄바꿈(\n)은 건너뛰지 않습니다!"""
        while self.current_char is not None and self.current_char in ' \t\r':
            self.advance()

    def get_next_token(self):
        """
        호출될 때마다 코드에서 다음 토큰 하나를 찾아 반환합니다.
        """
        while self.current_char is not None:
            if self.current_char in ' \t\r':
                self.skip_whitespace()
                continue

            if self.current_char == '\n':
                self.advance()
                return Token(NEWLINE, '\n')

            if self.current_char == 'n' and self.text[self.pos:self.pos + 5].lower() == 'note:':
                self.skip_comment()
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.current_char.isdigit():
                return Token(INTEGER, self.number())
            
            if self.current_char in ('"', "'"):
                return Token(STRING, self.string())
            
            if self.current_char == '=': self.advance(); return Token(EQ, '=')
            if self.current_char == '!' and self.peek() == '=': self.advance(); self.advance(); return Token(NEQ, '!=')
            if self.current_char == '>' and self.peek() == '=': self.advance(); self.advance(); return Token(GTE, '>=')
            if self.current_char == '<' and self.peek() == '=': self.advance(); self.advance(); return Token(LTE, '<=')
            
            if self.current_char == '>': self.advance(); return Token(GT, '>')
            if self.current_char == '<': self.advance(); return Token(LT, '<')
            if self.current_char == '+': self.advance(); return Token(PLUS, '+')
            if self.current_char == '-': self.advance(); return Token(MINUS, '-')
            if self.current_char == '*': self.advance(); return Token(MUL, '*')
            if self.current_char == '/': self.advance(); return Token(DIV, '/')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
        
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')
            
            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')
            
            raise Exception(f"Invalid character: '{self.current_char}'")

        return Token(EOF, None) # 코드의 끝에 도달하면 EOF 토큰 반환