function load(canvasId, file) {
  return new Promise((resolve, reject) => {
    var canvas = document.getElementById(canvasId);
    var ctx = canvas.getContext("2d");
    var image = new Image();
    var reader = new FileReader();
    reader.onload = e => {
      image.onload = () => {
        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
        resolve(image);
      }
      image.src = e.target.result;
    }
    reader.readAsDataURL(file);
  });
}

function show(inputCanvasId, outputCanvasId) {
  let src = cv.imread(inputCanvasId);
    let gray = new cv.Mat();
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);
    let faces = new cv.RectVector();
    let eyes = new cv.RectVector();
    let faceCascade = new cv.CascadeClassifier();
    let eyeCascade = new cv.CascadeClassifier();
    faceCascade.load("/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml");
    eyeCascade.load("/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_eye.xml");
    let msize = new cv.Size(0, 0);
    faceCascade.detectMultiScale(gray, faces, 1.1, 3, 0, msize, msize);
    for (let i = 0; i < faces.size(); ++i)
    {
        let roiGray = gray.roi(faces.get(i));
        let roiSrc = src.roi(faces.get(i));
        let point1 = new cv.Point(faces.get(i).x, faces.get(i).y);
        let point2 = new cv.Point(faces.get(i).x + faces.get(i).width, faces.get(i).y + faces.get(i).height);
        cv.rectangle(src, point1, point2, [255, 0, 0, 255]);
        eyeCascade.detectMultiScale(roiGray, eyes);
        for (let j = 0; j < eyes.size(); ++j)
        {
            let point1 = new cv.Point(eyes.get(j).x, eyes.get(j).y);
            let point2 = new cv.Point(eyes.get(j).x + eyes.get(j).width, eyes.get(j).y + eyes.get(j).height);
            cv.rectangle(roiSrc, point1, point2, [0, 0, 255, 255]);
        }
        roiGray.delete();
        roiSrc.delete();
    }
    cv.imshow(outputCanvasId, src);
    src.delete();
    gray.delete();
    faceCascade.delete();
    eyeCascade.delete();
    faces.delete();
    eyes.delete();

}

async function onChange(file) {
  try {
    await load('input', file);
    show('input', 'output');
    await check6(event);
  } catch(e) {
    alert("警告！！");
  }

}

let input = document.querySelector('input[type="file"]');
input.addEventListener('change', e => onChange(e.target.files[0]), false);
//動画流す準備
var video = document.getElementById("videof");
// getUserMedia によるカメラ映像の取得
var media = navigator.mediaDevices.getUserMedia({
    video: true,//ビデオを取得する
    //使うカメラをインカメラか背面カメラかを指定する場合には
    //video: { facingMode: "environment" },//背面カメラ
    //video: { facingMode: "user" },//インカメラ
    audio: false,//音声が必要な場合はture
});
//リアルタイムに再生（ストリーミング）させるためにビデオタグに流し込む
media.then((stream) => {
    video.srcObject = stream;
});
