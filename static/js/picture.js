$(function () {

  var jcrop_api,
      boundx,
      boundy,
      xsize = 300,
      ysize = 300;
  
  $("#crop-picture").Jcrop({
    aspectRatio: 1 / 1,
    minCropBoxWidth: 200,
    minCropBoxHeight: 200,
    onSelect: updateCoords,
    setSelect: [0, 0, 300, 300]
  },function(){
    var bounds = this.getBounds();
    boundx = bounds[0];
    boundy = bounds[1];
    jcrop_api = this;
  });

  function updateCoords(c) {
    $("#x").val(c.x);
    $("#y").val(c.y);
    $("#width").val(c.w);
    $("#height").val(c.h);
  };

  $("#btn-upload-picture").click(function () {
    $("#picture-upload-form input[name='picture']").click();
  });

  $("#picture-upload-form input[name='picture']").change(function () {
    $("#picture-upload-form").submit();
  });

});
