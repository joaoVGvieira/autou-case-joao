document.addEventListener('DOMContentLoaded', () => {
    
    // --- Lógica para o campo de Upload (Arrastar e Soltar) ---
    const fileDropArea = document.querySelector('.file-drop-area');
    const fileInput = document.querySelector('.file-input');
    const fileMsg = document.querySelector('.file-msg');

    if (fileDropArea) {
        // Evento para quando o arquivo é arrastado sobre a área
        fileDropArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileDropArea.classList.add('dragover');
        });

        // Evento para quando o arquivo sai da área
        fileDropArea.addEventListener('dragleave', () => {
            fileDropArea.classList.remove('dragover');
        });

        // Evento para quando o arquivo é solto na área
        fileDropArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileDropArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length) {
                fileInput.files = files;
                updateFileMsg(files[0].name);
            }
        });

        // Evento para quando um arquivo é selecionado pelo clique
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                updateFileMsg(fileInput.files[0].name);
            }
        });

        const updateFileMsg = (fileName) => {
            fileMsg.innerHTML = `Arquivo selecionado: <strong>${fileName}</strong>`;
        };
    }


    // --- Lógica para o Botão de Carregamento (Spinner) ---
    const form = document.getElementById('email-form');
    const submitBtn = form.querySelector('.btn-submit');

    if (form) {
        form.addEventListener('submit', () => {
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
        });
    }

    // --- Lógica para o Botão de Copiar ---
    const copyBtn = document.getElementById('copy-btn');
    const responseText = document.getElementById('suggested-response');

    if (copyBtn && responseText) {
        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(responseText.innerText)
                .then(() => {
                    copyBtn.classList.add('copied');
                    setTimeout(() => {
                        copyBtn.classList.remove('copied');
                    }, 2000);
                })
                .catch(err => console.error('Erro ao copiar texto: ', err));
        });
    }

});