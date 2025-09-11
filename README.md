# jf-language-online
# JF Language Online IDE

[![Run Online IDE](https://img.shields.io/badge/Run-Online%20IDE-blue.svg)](https://jf-language-online.pages.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**JF Language**는 웹 기반의 온라인 IDE를 통해 누구나 쉽게 배우고 실행할 수 있는 간단한 스크립트 언어입니다.

---

## ✨ 주요 기능 (Features)

* 변수 선언, 산술/논리/비교 연산 등 기본적인 프로그래밍 언어 기능 지원
* `console.print()`를 이용한 표준 출력 기능
* 실시간 코드 실행 및 결과 확인
* CodeMirror를 활용한 사용성 높은 코드 에디터 (라인 번호, 기본 문법 하이라이팅)

## 🛠️ 기술 스택 (Tech Stack)

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript (CodeMirror)
* **Deployment:**
    * Backend API: Render
    * Frontend: Cloudflare Pages

## 📖 JF 언어 기본 문법 (Language Syntax)

JF 언어는 다음과 같은 간단한 문법을 가집니다.

**변수 선언:**
```jf
note: 'is' 키워드를 사용합니다.
my_variable is 123.
message is "Hello, JF!".
```

**출력:**
```jf
console.print("Hello, World!").
x is 10.
y is 20.
console.print(x, "+", y, "is", x + y).
```

## 🚀 로컬에서 실행하기 (Getting Started)

1.  이 저장소를 복제(clone)합니다.
    ```bash
    git clone [https://github.com/Jeaho06/jf-language-online.git](https://github.com/Jeaho06//jf-language-online.git)
    cd jf-language-online
    ```
2.  백엔드 서버를 실행합니다.
    ```bash
    cd backend
    pip install -r requirements.txt
    python app.py
    ```
3.  `frontend/index.html` 파일을 브라우저에서 엽니다.

---

## 📜 라이선스 (License)

이 프로젝트는 [MIT License](LICENSE)를 따릅니다.