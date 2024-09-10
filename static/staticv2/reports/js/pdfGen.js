//pdfGen
function pdfGen() {

  $('#modal').modal({
    	backdrop: 'static',
    	keyboard: false
	});
  $('#modal').modal('show');

  $('.btn').prop('disabled', true);
  $('.page-number').css('padding-top', '2px');
  $('.more i').css('padding-top', '5px');

  var a4 = $('.a4:visible');
  var quality = $('.pdf').attr('quality');
  let doc = new jsPDF('p', 'mm', 'a4', true);

  var i = 0;
  function recursive_html2canvas() {
    i++;
    if(i > a4.length) return;
    html2canvas(document.querySelector('.a4-'+i), {scale: quality}).then(function(canvas) {

        var div = document.createElement("div");
        $(div).addClass('shot');
        $(div).attr('shot', canvas.toDataURL('image/png'));
        $('.pdf').append(div);
        var shots = $('.shot');
        var sn = shots.length;
        $(div).addClass('shot-'+sn);

        recursive_html2canvas();
    });
  }
  recursive_html2canvas();

  var a4num = $('.a4:visible');
  var time = 5000;
  for(let i=0; i<a4num.length; i++) {
      time += 5000;
  }
  setTimeout(function() {
      var shot = $('.shot');
      for (i=0; i < shot.length; i++) {
          //alert($(shot[i]).attr('shot'));//debug
          doc.addImage($('.shot-'+(i+1)).attr('shot'), 'PNG', 0, 0, 210, 297, '','FAST');//shot[i]
          if(i<(shot.length-1))
              doc.addPage();
      }
      doc.save($('.pdf').attr('filename'));

      $('#modal').modal('hide');
      $('.back').show();
  }, time);
}
