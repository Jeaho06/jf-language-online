// frontend/script.js
// CodeMirror 에디터를 초기화합니다.
const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
    lineNumbers: true,
    mode: 'python', // JF 언어용 문법 하이라이팅이 없으므로, 일단 python으로 설정
    theme: 'material-darker'
});

const runButton = document.getElementById('run-button');
const outputContainer = document.getElementById('output-container');

// 백엔드 API 서버의 주소입니다.
// 로컬 테스트 시에는 'http://127.0.0.1:5000/run'
// 나중에 배포 후에는 실제 배포된 서버 주소로 변경해야 합니다.
const API_ENDPOINT = 'https://jf-language-online.onrender.com';

runButton.addEventListener('click', async () => {
    const code = editor.getValue(); // 에디터에 입력된 코드를 가져옵니다.
    outputContainer.textContent = 'Executing...';
    outputContainer.classList.remove('error');

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        });

        const result = await response.json();

        if (result.error) {
            // 에러가 있다면 에러 메시지를 빨간색으로 표시
            outputContainer.textContent = result.output + result.error;
            outputContainer.classList.add('error');
        } else {
            // 성공했다면 결과 출력
            outputContainer.textContent = result.output;
        }

    } catch (err) {
        outputContainer.textContent = 'Failed to connect to the server. Is it running?';
        outputContainer.classList.add('error');
    }
});

// 예시 코드 설정
editor.setValue(`
note: JF Language Example Code

name is "World".
greeting is "Hello, " + name + "!".

console.print(greeting).
console.print("1 + 2 is", 1 + 2).
`);