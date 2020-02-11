function videof() {
  face_recognition('videof', 'outputf');
}

function face_recognition(inputVideoId, outputCanvasId) {
  let video = document.getElementById(inputVideoId);
  let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
  let dst = new cv.Mat(video.height, video.width, cv.CV_8UC4);
  let gray = new cv.Mat();
  let cap = new cv.VideoCapture(video);
  let faces = new cv.RectVector();
  let eyes = new cv.RectVector();
  let mouths = new cv.RectVector();
  let noses = new cv.RectVector();
  let faceClassifier = new cv.CascadeClassifier();
  let eyeClassifier = new cv.CascadeClassifier();
  let mouthClassifier = new cv.CascadeClassifier();
  let noseClassifier = new cv.CascadeClassifier();
  var faceCas = document.getElementById("faceCas").value;
  let utils = new Utils('errorMessage');
  let faceCascadeFile = "/haarcascade_frontalface_default.xml";
  let eyeCascadeFile = "/haarcascade_eye.xml";
  let mouthCascadeFile = "/haarcascade_mcs_mouth.xml";
  let noseCascadeFile = "/haarcascade_mcs_nose.xml";

  var xmlhttp = new XMLHttpRequest();
  // xmlhttp.open("GET", faceCascadeFile);
  // xmlhttp.send();

  // load pre-trained classifiers
  classifier.load(faceCascadeFile);
  // utils.createFileFromUrl(faceCascadeFile, faceCascadeFile, () => {
  //   classifier.load(faceCascadeFile); // in the callback, load the cascade from file
  // });

  const FPS = 30;
  function processVideo() {
      try {
          // if (!cap.streaming) {
          //     // clean and stop.
          //     src.delete();
          //     dst.delete();
          //     gray.delete();
          //     faces.delete();
          //     classifier.delete();
          //     return;
          // }
          let begin = Date.now();
          // start processing.
          cap.read(src);
          src.copyTo(dst);
          cv.cvtColor(dst, gray, cv.COLOR_RGBA2GRAY, 0);
          // detect faces.

          // 輪郭
          for (let i = 0; i < faces.size(); ++i) {
              let face = faces.get(i);
              let facePoint1 = new cv.Point(face.x, face.y);
              let facePoint2 = new cv.Point(face.x + face.width, face.y + face.height);
              cv.rectangle(dst, facePoint1, facePoint2, [255, 0, 0, 255]);
          }
          // 目
          for (let i = 0; i < eyes.size(); ++i) {
              let eye = eyes.get(i);
              let eyePoint1 = new cv.Point(eye.x, eye.y);
              let eyePoint2 = new cv.Point(eye.x + eye.width, eye.y + eye.height);
              cv.rectangle(dst, eyePoint1, eyePoint2, [255, 0, 0, 255]);
          }
          // 口
          for (let i = 0; i < mouths.size(); ++i) {
              let mouth = mouths.get(i);
              let mouthPoint1 = new cv.Point(mouth.x, mouth.y);
              let mouthPoint2 = new cv.Point(mouth.x + mouth.width, mouth.y + mouth.height);
              cv.rectangle(dst, mouthPoint1, mouthPoint2, [255, 0, 0, 255]);
          }
          // 鼻
          for (let i = 0; i < noses.size(); ++i) {
              let nose = noses.get(i);
              let nosePoint1 = new cv.Point(nose.x, nose.y);
              let nosePoint2 = new cv.Point(nose.x + nose.width, nose.y + nose.height);
              cv.rectangle(dst, nosePoint1, nosePoint2, [255, 0, 0, 255]);
          }
          
          cv.imshow(outputCanvasId, dst);
          cv.imshow("gray", gray);
          // schedule the next one.
          let delay = 1000/FPS - (Date.now() - begin);
          setTimeout(processVideo, delay);
      } catch (error) {
         error.innerHTML = "<p>" + error + "</p>";
         //utils.printError(error);
         console.error("エラーは", error);
         console.log(error.message);
         console.log(error.name);
      }
    };

  // schedule the first one.
  setTimeout(processVideo, 0);
  }

function gray() {
  let src = cv.imread('inputgray');
  let dst = new cv.Mat();
  // You can try more different parameters
  cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY, 0);
  cv.imshow('canvasOutput', dst);
  src.delete(); dst.delete();
  }
