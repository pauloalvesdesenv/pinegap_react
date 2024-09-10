var doc = $('.document');
var a4 = $('.a4');
var a4_model = $('.a4-model').html();
var a4_prepend = $('.a4-prepend').find('.a4');
var a4_append = $('.a4-append').find('.a4');
var a4_dynamic_total = 3;
var a4_total = (a4_prepend.length+a4_append.length)+a4_dynamic_total;

//var a4_display_length = 4;
var a4_new = new Array();

for(let i=0; i<a4_dynamic_total; i++) {

    a4_new[i] = $(a4_model).clone();
    a4_content = $(a4_new[i]).find('.a4-content');

    //add content
    $(a4_content).append('#'+i);
    $(a4_new[i]).append(a4_content);

    //add page
    $(doc).append(a4_new[i]);
    $(doc).append('<br />');
}
$(doc).append($('.a4-append').html());
$(doc).prepend($('.a4-prepend').html());

var a4num = $('.a4:visible');
alert(a4num.length);
for(i=0; i<a4num.length; i++) {
    $(a4num[i]).addClass('a4-'+i);
}
