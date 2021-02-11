//defining const
const canvas = document.querySelector("#canvas");
const context = canvas.getContext("2d");
const video = document.querySelector("video");

//defining canvas dims
canvas.width = 120;
canvas.height = 120;

//getmediadevices constraints
const constraints = {
  audio: false,
  video: { width: 120, height: 120 }
};

//set video sourceobj to webcam
function handleSuccess(stream) {
  window.stream = stream; // make stream available to browser console
  video.srcObject = stream;
}

//set error handler for webcam
function handleError(error) {
  console.log('navigator.MediaDevices.getUserMedia error: ', error.message, error.name);
}

//turn on webcam
navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);

//on photo button press
$("#photoButton").on("click", function() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    $("video").hide();
    $("canvas").show();
});

//clear button
$("#clearButton").on("click", function() {
    context.clearRect( 0, 0, 120, 120 );
    $("canvas").hide();
    $("video").show();
});
 
//predict button
$("#predictButton").click(function(){
    if($("video").is(":hidden")){
        $('#result').text('  Predicting...');
        var img = canvas.toDataURL('image/png');
        $("#result").empty();
        $("#probability").empty();
        $.ajax({
            type: "POST",
            url: "https://ca2-2b11-asdfasdf-web.herokuapp.com/predict",
            //url: "http://localhost:5000/predict",
            data: img,
            success: function(data){
                var labels = ['Angry','Fear','Sad','Neutral','Happy', 'Surprise']
                $('#result').text('Predicted Output: ' + data[data.length -1]);
                $('#probability').append('<h1>Predicted probabilities</h1>')
                for(i=0; i<data.length-1; i++){
                    $('#probability').append('<p>'+labels[i] + ' probability: ' + data[i]+'</p>');
                }
            }
        });

    } 
    else{
        alert("Take a picture first!");
    }

});
