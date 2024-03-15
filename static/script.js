document.addEventListener('DOMContentLoaded', function () {
    
    // Generate Invitation
    var generateInvitationButton = document.getElementById('generateInvitationButton');
    if (generateInvitationButton) {
        generateInvitationButton.addEventListener('click', function() {
            fetch('http://localhost:8000/ui-event/generate-invitation', { method: 'GET', credentials: 'include' })
                .then(response => response.json())
                .then(data => {
                    // Generate QR-Code
                    const qrCodeDisplay = document.getElementById('qrCodeDisplay');
                    qrCodeDisplay.classList.remove('hidden'); // Show the QR code display
                    const qrCode = new QRCode(qrCodeDisplay, {
                        text: data.invitation_url,
                        width: 400,
                        height: 400,
                        colorDark: "#000000",
                        colorLight: "#ffffff",
                        correctLevel: QRCode.CorrectLevel.L
                    });
                })
                .catch(error => console.error('Error:', error));
        });
    } else {
        console.error('Generate Invitation Button not found');
    }

    // Start eID process
    var startEIdProcess = document.getElementById('startEIdProcess');
    if (startEIdProcess) {
        startEIdProcess.addEventListener('click', function() {
            fetch('http://localhost:8000/ui-event/start-eID', { method: 'GET', credentials: 'include' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('eIDMessage').textContent = data.message;
                    if (data.success == true) {
                        startEIdProcess.classList.add('hidden'); // Hide the eID process section
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    } else {
        console.error('Start eID Button not found');
    }

    const websocket = new WebSocket('ws://localhost:8000/ws');

    websocket.onmessage = function(event) {
        if (event.data === 'update_ui_conn_suc') {
            updateUIForActiveConnection();
        } 
        else if (event.data === 'update_ui_cred_issued') {
            updateUIForCredIssued();
        }
    };

    function updateUIForActiveConnection() {
        var generateInvButton = document.getElementById('generateInvitationButton');
        var qrCodeDisplay = document.getElementById('qrCodeDisplay');
        var eIdButton = document.getElementById('startEIdProcess');
        if (generateInvButton) {
            generateInvButton.classList.add('hidden'); // Hide the generate invitation button
        }
        if (qrCodeDisplay) {
            qrCodeDisplay.classList.add('hidden'); // Hide the QR code display
        }
        if (eIdButton) {
            eIdButton.classList.remove('hidden'); // Show the eID process section
        }
    }

    function updateUIForCredIssued() {
        document.getElementById('eIDMessage').textContent = "Vielen Dank. Ihr digitaler Wahlschein wurde erfolgreich in Ihrem Wallet gespeichert. Sie können den digitalen Wahlschein nun verwenden, um Ihre Stimmen im Wahlportal abzugeben.";
        document.getElementById('startEIdProcess').classList.add('hidden'); //Hide startEIdProcess button
    }
});
