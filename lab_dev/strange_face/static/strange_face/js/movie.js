var video = document.getElementById('video')// 適当にvideoタグのオブジェクトを取得
  var constrains = { video: true, audio: true }// 映像・音声を取得するかの設定
  navigator.mediaDevices.getUserMedia(constrains)
  .then(function(stream) {
      video.srcObject = stream // streamはユーザーのカメラとマイクの情報で、これをvideoの入力ソースにする
      video.play()
  })
  .catch(function(err) {
      console.log("An error occured! " + err)
  })

  // まずはユーザーのカメラ・マイクへのアクセスを実施
    navigator.mediaDevices.getUserMedia(constrains)
    .then(function (stream) {
      recorder = new MediaRecorder(stream) // 映像の入力ソースをユーザーのデバイスから取得
      recorder.ondataavailable = function (e) {
        var testvideo = document.getElementById('test')
        var width = 500
        var height = 350
        testvideo.setAttribute('controls', '')
        testvideo.setAttribute('width', width)
        testvideo.setAttribute('height', height)
        var outputdata = window.URL.createObjectURL(e.data) // videoタグが扱えるように、記録データを加工
        testvideo.src = outputdata // テスト用のビデオのソースに記録データを設置
      }
    })

    var startbutton = document.getElementById('start');
    var stopbutton = document.getElementById('stop');

    startbutton.addEventListener('click', function(ev){
      recorder.start()
      ev.preventDefault()
    }, false);

    stopbutton.addEventListener('click', function(ev) {
      recorder.stop()
    })

    downloadbutton.addEventListener('click', function(ev) {
    console.log(record_data)
    var blob = new Blob(record_data, { type: 'video/webm' })// 録画ファイルをblob形式に出力
    var url = window.URL.createObjectURL(blob) // データにアクセスするためのURLを作成
    var a = document.createElement('a') // download属性を持ったaタグをクリックするとダウンロードができるので、それをシミュレートする
    document.body.appendChild(a)
    a.style = 'display:none'
    a.href = url;
    a.download = 'test.webm'
    a.click()
    window.URL.revokeObjectURL(url)
  })
