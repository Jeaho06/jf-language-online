Markdown

# JF 언어 공식 가이드북 (v1.0)

JF 언어에 오신 것을 환영합니다! 이 문서는 JF 언어의 공식 문법과 규칙을 설명하는 가이드북입니다. 이 문서는 `README.md`에서 간략하게 소개된 문법을 더욱 상세하게 설명하며, JF 언어로 프로그램을 작성하는 데 필요한 모든 정보를 제공합니다.

## 목차
1. [기본 구조](#1-기본-구조)
2. [주석 (Comments)](#2-주석-comments)
3. [변수와 자료형 (Variables and Data Types)](#3-변수와-자료형-variables-and-data-types)
    - [선언과 할당](#31-선언과-할당)
    - [자료형의 종류](#32-자료형의-종류)
    - [문자열 보간 (String Interpolation)](#33-문자열-보간-string-interpolation)
4. [연산자 (Operators)](#4-연산자-operators)
    - [산술 연산자](#41-산술-연산자)
    - [비교 연산자](#42-비교-연산자)
    - [논리 연산자](#43-논리-연산자)
5. [내장 기능 (Built-in Features)](#5-내장-기능-built-in-features)
    - [`console.print()`](#51-consoleprint)
    - [`console.read()`](#52-consoleread)
6. [타입 변환 (Type Casting)](#6-타입-변환-type-casting)

---

### 1. 기본 구조

JF 언어의 모든 실행 문장(statement)은 반드시 마침표(`.`)로 끝나야 합니다. 이는 하나의 명령이 끝났음을 언어에 알려주는 규칙입니다.

만약 한 줄에 여러 개의 문장을 작성하고 싶다면, 각 문장을 콜론(`:`)으로 구분할 수 있습니다.

**예시:** "Hello, World!" 출력
```
console.print("Hello, World!").
```

**예시** 한 줄에 여러 문장 작성
```
x is 10: console.print(x).
```
### 2. 주석 (Comments)

주석은 코드에 대한 설명을 작성하는 부분으로, 실제 프로그램 실행에는 영향을 주지 않습니다. JF 언어에서는 note: 키워드로 주석을 시작합니다. note:가 나오면 그 줄의 끝까지 모든 내용은 주석으로 처리됩니다.

**예시**
```
note: 이 줄은 전체가 주석입니다.
x is 100. note: 이 부분은 주석으로 처리됩니다.
```

### 3.1 변수와 자료형 (Variables and Data Types)

3.1 선언과 할당
변수는 값을 저장하는 공간입니다. JF 언어에서는 is 키워드를 사용하여 변수를 선언하고 값을 할당합니다.

**예시**
```
note: 변수 age에 숫자 25를 할당합니다.
age is 25.

note: 변수 user_name에 문자열 "Jeaho"를 할당합니다.
user_name is "Jeaho".

note: 다른 변수나 연산의 결과를 할당할 수도 있습니다.
total_price is 1000 + 500.
```

### 3.2 자료형의 종류

JF 언어는 다음과 같은 기본 자료형을 지원합니다.

정수 (Integer): 10, 0, -25와 같은 숫자입니다.

문자열 (String): "Hello", 'World'와 같이 따옴표(" 또는 ')로  감싸인 텍스트입니다.

불리언 (Boolean): true 또는 false 값을 가지며, 주로 조건의 참/거짓을 나타냅니다.

**예시**
```
count is 10.         note: 정수형 변수
message is "Hi".     note: 문자열 변수
is_active is true.   note: 불리언 변수
```

### 3.3 문자열 보간 (String Interpolation)

문자열 내부에 변수 값을 쉽게 포함시킬 수 있는 기능입니다. @{변수명} 형식을 사용하면 해당 부분에 변수의 값이 자동으로 삽입됩니다.

**예시**
```
name is "Alex".
age is 30.

note: 문자열 안에 name과 age 변수의 값을 포함하여 출력합니다.
console.print("My name is @{name} and I am @{age} years old.").

note: 실행 결과 -> My name is Alex and I am 30 years old.
```

### 4. 연산자 (Operators)
4.1 산술 연산자
숫자 계산에 사용되는 연산자입니다.

연산자	설명	예시	결과
+	덧셈	10 + 5	15
-	뺄셈	10 - 5	5
*	곱셈	10 * 5	50
/	나눗셈	10 / 5	2

Sheets로 내보내기
특징: + 연산자는 피연산자 중 하나라도 문자열이면, 나머지 값도 문자열로 변환하여 두 문자열을 연결합니다.

코드 스니펫

result is "Price: " + 100.
console.print(result). note: "Price: 100" 출력
4.2 비교 연산자
두 값의 크기를 비교하며, 결과는 불리언(true 또는 false) 값으로 나옵니다.

연산자	설명	예시	결과
==	같음	5 == 5	true
!=	다름	5 != 3	true
<	보다 작음	3 < 5	true
>	보다 큼	3 > 5	false
<=	보다 작거나 같음	5 <= 5	true
>=	보다 크거나 같음	3 >= 5	false

Sheets로 내보내기
4.3 논리 연산자
불리언 값들을 조합하여 새로운 불리언 결과를 만들어냅니다.

연산자	설명	예시	결과
and	그리고(AND): 양쪽 모두 true일 때만 true	true and false	false
or	또는(OR): 둘 중 하나라도 true이면 true	true or false	true
not	아님(NOT): 불리언 값을 반대로 뒤집음	not true	false

Sheets로 내보내기
5. 내장 기능 (Built-in Features)
5.1 console.print()
괄호 안의 값을 화면에 출력합니다. 쉼표(,)를 사용하여 여러 개의 값을 한 번에 출력할 수 있으며, 값들은 공백으로 구분되어 출력됩니다.

코드 스니펫

x is 10.
y is 20.
console.print("The value of x is", x).
console.print(x, "+", y, "is", x + y).

note: 실행 결과
note: The value of x is 10
note: 10 + 20 is 30
5.2 console.read()
사용자로부터 한 줄의 입력을 받습니다. 이 기능은 주로 사용자가 입력한 값을 변수에 저장할 때 사용됩니다. console.read()는 선택적으로 int()나 string()을 인자로 받아 입력받은 값을 해당 타입으로 변환하려고 시도합니다. 기본값은 string() 입니다.

코드 스니펫

note: 사용자의 이름을 입력받아 name 변수에 저장합니다.
console.print("Enter your name: ").
name is console.read(string()).

note: 사용자의 나이를 입력받아 정수형으로 age 변수에 저장합니다.
console.print("Enter your age: ").
age is console.read(int()).

console.print("Hello, @{name}! You are @{age} years old.").
6. 타입 변환 (Type Casting)
값의 자료형을 다른 자료형으로 명시적으로 변환하는 기능입니다.

int(값): 주어진 값을 정수(Integer)로 변환합니다.

string(값): 주어진 값을 문자열(String)로 변환합니다.

코드 스니펫

note: 문자열 "123"을 숫자 123으로 변환합니다.
num_str is "123".
num_int is int(num_str).
console.print(num_int + 7). note: 130 출력

note: 숫자 456을 문자열 "456"으로 변환합니다.
my_num is 456.
my_str is string(my_num).
console.print("The number is " + my_str).