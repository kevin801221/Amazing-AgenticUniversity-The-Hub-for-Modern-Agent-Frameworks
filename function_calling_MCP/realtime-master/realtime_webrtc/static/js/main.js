let mediaStream = null; // 取得麥克風輸入的串流物件
let actionButton = null; // 開/關麥克風的按鈕
let outputArea = null; // 顯示事件的輸出區域
let statusLabel = null; // 顯示狀態的標籤
let mic_on = false; // 麥克風狀態
let dc = null; // DataChannel 物件

// 更新按鈕狀態和文字
function updateButtonState(isActive) {
    if (isActive) {
        actionButton.textContent = '關閉麥克風';
        actionButton.classList.remove('btn-primary');
        actionButton.classList.add('btn-danger');
    } else {
        actionButton.textContent = '開啟麥克風';
        actionButton.classList.remove('btn-danger');
        actionButton.classList.add('btn-primary');
    }
}

// 在輸出區域顯示新的一行文字
function appendToOutput(text) {
    outputArea.innerHTML += text + '<br/>';
}

// 清除狀態標籤內容
function clearStatus() {
    statusLabel.textContent = '';
}

// 在狀態標籤尾端添加文字
function appendStatus(text) {
    statusLabel.textContent += text;
}

document.addEventListener('DOMContentLoaded', async function() {
    // 取得 HTML 元素
    actionButton = document.getElementById('actionButton');
    outputArea = document.getElementById('outputArea');
    statusLabel = document.getElementById('statusLabel');

    try {
        // 取得語音輸入的裝置
        mediaStream = await 
            navigator.mediaDevices.getUserMedia({
                audio: true
            });
        updateButtonState(true); // 更新按鈕文字
        mic_on = true; // 麥克風狀態
        clearStatus(); // 清除狀態標籤內容
        appendStatus('麥克風已開啟');
        
        // 建立 WebRTC 連線
        await initWebRTC(mediaStream);
    } catch (error) {
        console.error('無法取得麥克風存取權限:', error);
        clearStatus();
        appendStatus('無法取得麥克風存取權限');
        actionButton.disabled = true; // 禁用按鈕
    }

    actionButton.addEventListener('click', async function() {
        mic_on = !mic_on; // 切換麥克風狀態
        mediaStream.getTracks().forEach(
            track => track.enabled = mic_on
        );
        updateButtonState(mic_on); // 更新按鈕文字
        clearStatus(); // 清除狀態標籤內容

        if (!mic_on) {
            appendStatus(mic_on ? '麥克風已開啟' : '麥克風已關閉');
        }
    });
});

function setEventHandler() {
    // 處理代表伺服端事件的 "message" 事件
    dc.addEventListener("message", (e) => {
        // data 是 JSON 格式的 Realtime API 伺服端事件
        const event = JSON.parse(e.data);
        // 在輸出區域顯示事件類型供檢視流程
        appendToOutput(event.type);

        if(event.type === "session.created") {
            // 傳送用戶端事件修改 session
            dc.send(JSON.stringify({
                type: "session.update",
                session: {
                    instructions: "使用繁體中文",
                }
            }));
        }
        else if (event.type === "conversation.item.created") {
            // 生成新內容時先清除顯示內容的標籤
            clearStatus();
        }
        else if (event.type === 
            "response.audio_transcript.delta") {
            // 生成文字完成顯示在標籤內
            appendStatus(event.delta);
        }
    });
}

async function initWebRTC(stream) {
    // 取得臨時的 API 金鑰
    const response = await fetch("/key");
    const EPHEMERAL_KEY = await response.text();
    
    appendStatus('正在初始化 WebRTC...');
  
    // 建立 WebRTC 連線物件
    const pc = new RTCPeerConnection();
  
    // 建立播放語音的元素
    const audioElm = document.createElement("audio");
    audioElm.autoplay = true;
    // 對方加入音軌時觸發，這裡將音訊資料串流給語音元素自動播放
    pc.ontrack = e => audioElm.srcObject = e.streams[0];

    // 加入要串流給伺服端的音軌，此處串接麥克風
    pc.addTrack(stream.getTracks()[0]);
    clearStatus();
    appendStatus('使用 ' + stream.getTracks()[0].label);
  
    // 設定標籤為 "oai-events"，用來傳遞 Realtime API 事件的資料通道
    dc = pc.createDataChannel("oai-events");

    setEventHandler(); // 處理 DataChannel 事件

    // 取得目前設定（提供哪些媒體串流、格式等）的供應資訊（offer）
    const offer = await pc.createOffer();
    // 設定本地端的供應資訊
    await pc.setLocalDescription(offer);
  
    // 送出本地端供應資訊給遠端並取得對方的供應資訊
    const baseUrl = "https://api.openai.com/v1/realtime";
    const model = "gpt-4o-realtime-preview";
    const sdpResponse = await fetch(
        `${baseUrl}?model=${model}`, 
        {
            method: "POST",
            body: offer.sdp,
            headers: {
                Authorization: `Bearer ${EPHEMERAL_KEY}`,
                "Content-Type": "application/sdp"
            },
        }
    );

    const answer = {
        type: "answer",
        sdp: await sdpResponse.text(),
    };
    // 儲存遠端的供應資訊
    await pc.setRemoteDescription(answer);
}