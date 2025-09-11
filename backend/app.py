# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import io
from contextlib import redirect_stdout

# JF 언어 인터프리터 관련 모듈 임포트
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

app = Flask(__name__)
CORS(app) # 모든 도메인에서의 요청을 허용 (개발 편의를 위해)

@app.route('/run', methods=['POST'])
def run_code():
    # 클라이언트로부터 JSON 형식으로 코드를 받음
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'error': 'Code not provided'}), 400

    code = data['code']
    
    # print() 함수의 출력을 가로채기 위한 설정
    output_buffer = io.StringIO()
    
    try:
        with redirect_stdout(output_buffer):
            # 1. Lexer -> Parser -> Interpreter 실행 파이프라인
            lexer = Lexer(code)
            parser = Parser(lexer)
            tree = parser.parse()
            
            # 새로운 인터프리터 인스턴스를 매번 생성하여 실행 환경 초기화
            interpreter = Interpreter()
            interpreter.interpret(tree)

        # 가로챈 출력 결과를 변수에 저장
        output = output_buffer.getvalue()
        
        # 성공적으로 실행되면 출력 결과를 JSON으로 반환
        return jsonify({'output': output, 'error': ''})

    except Exception as e:
        # 실행 중 에러가 발생하면 에러 메시지를 JSON으로 반환
        error_message = f"Error: {e}"
        # 에러 발생 시의 출력도 함께 반환할 수 있음
        output = output_buffer.getvalue()
        return jsonify({'output': output, 'error': error_message})

if __name__ == '__main__':
    # 개발용 서버 실행
    app.run(debug=True, port=5000)