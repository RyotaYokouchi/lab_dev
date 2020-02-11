function startVideo() {
    console.info('入出力デバイスを確認してビデオを開始するよ！');

    Promise.resolve()
        .then(function () {
            return navigator.mediaDevices.enumerateDevices();
        })
        .then(function (mediaDeviceInfoList) {
            console.log('使える入出力デバイスs->', mediaDeviceInfoList);

            var videoDevices = mediaDeviceInfoList.filter(function (deviceInfo) {
                return deviceInfo.kind == 'videoinput';
            });
            if (videoDevices.length < 1) {
                throw new Error('ビデオの入力デバイスがない、、、、、。');
            }

            return navigator.mediaDevices.getUserMedia({
                audio: false,
                video: {
                    deviceId: videoDevices[0].deviceId
                }
            });
        })
        .then(function (mediaStream) {
            console.log('取得したMediaStream->', mediaStream);
            videoStreamInUse = mediaStream;
            //document.querySelector('video').src = window.URL.createObjectURL(mediaStream);
            // 対応していればこっちの方が良い
            document.querySelector('video').srcObject = mediaStream;


        })
        .catch(function (error) {
            console.error('ビデオの設定に失敗、、、、', error);
        });
}

//ビデオ停止！ボタンで走るやつ

function stopVideo() {
    console.info('ビデオを止めるよ！');

    videoStreamInUse.getVideoTracks()[0].stop();

    if (videoStreamInUse.active) {
        console.error('停止できかた、、、', videoStreamInUse);
    } else {
        console.log('停止できたよ！', videoStreamInUse);
    }
}

function snapshot() {
    console.info('スナップショットをとるよ！');

    var videoElement = document.querySelector('.stream-video');
    var canvasElement = document.querySelector('canvas');
    var context = canvasElement.getContext('2d');

    context.drawImage(videoElement, 0, 0, videoElement.width, videoElement.height);
    document.querySelector('img').src = canvasElement.toDataURL('image/webp');
}

function normalFaceShot() {
    console.info('真顔の撮影をします。');

    var videoElement = document.querySelector('.stream-video');
    var canvasElement = document.querySelector('.normal-face-canvas');
    //var canvasElement = document.querySelector('canvas');
    var context = canvasElement.getContext('2d');

    context.drawImage(videoElement, 0, 0, videoElement.width, videoElement.height);
    document.querySelector('.normal-face-img').src = canvasElement.toDataURL('image/webp');
    document.querySelector('#id_normal_face').src = canvasElement.toDataURL('image/webp');

    //アンカータグを作成
  	var a = document.createElement('a');
  	//canvasをJPEG変換し、そのBase64文字列をhrefへセット
  	a.href = canvasElement.toDataURL('image/jpeg', 0.85);
  	//ダウンロード時のファイル名を指定
  	a.download = 'normal_face.jpg';
  	//クリックイベントを発生させる
  	a.click();
}

function strangeFaceShot() {
    console.info('変顔の撮影をします。');

    var videoElement = document.querySelector('.stream-video');
    var canvasElement = document.querySelector('.strange-face-canvas');
    var context = canvasElement.getContext('2d');

    context.drawImage(videoElement, 0, 0, videoElement.width, videoElement.height);
    document.querySelector('.strange-face-img').src = canvasElement.toDataURL('image/webp');
    document.querySelector('#id_strange_face').src = canvasElement.toDataURL('image/webp');

    //アンカータグを作成
  	var a = document.createElement('a');
  	//canvasをJPEG変換し、そのBase64文字列をhrefへセット
  	a.href = canvasElement.toDataURL('image/jpeg', 0.85);
  	//ダウンロード時のファイル名を指定
  	a.download = 'strange_face.jpg';
  	//クリックイベントを発生させる
  	a.click();
}
