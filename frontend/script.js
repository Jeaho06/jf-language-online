// frontend/script.js

const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
    lineNumbers: true,
    mode: 'python', // JF 언어에 맞는 모드가 없으므로 임시로 python 사용
    theme: 'material-darker'
});

const runButton = document.getElementById('run-button');
const outputContainer = document.getElementById('output-container');


const API_ENDPOINT = 'https://jf-language-online.onrender.com/run';

runButton.addEventListener('click', async () => {
    const code = editor.getValue(); 
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
            // 오류가 발생했다면 오류 메시지 출력
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

// 예시 코드 
editor.setValue(`
note: JF Language Example Code

name is "World".
greeting is "Hello, " + name + "!".

console.print(greeting).
console.print("1 + 2 is", 1 + 2).
`);