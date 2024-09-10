//populate data[]
var data = [];
var a4_loop_model = [];
var mm_total = 0;

//loop dataset
for (var dataset in _dataset) {

    data[dataset] = [];

    if(dataset=='finding' || dataset== 'list') {

      for(z=1;z<_dataset[dataset].length; z++) {

           data[dataset][z] = [];
           for(x=1; x <_dataset[dataset][z].length;x++) {
              //clone html model
              a4_loop_model[x] = $('.a4-loop-model[loop-item="'+dataset+'"]').clone();
              //new recipient
              var new_a4_loop_model = [];
              new_a4_loop_model[dataset] = [];
              //param2array
              var param2array = [];

              //loop dataset items
              var additional_mm=0;
              for(attr in _dataset[dataset][z][x]) {

                  var param2temp2 = '';
                  //subparams to insert
                  var param2 = document.createElement('tr');
                  $(param2).addClass(dataset+'-subitem');
                  //params
                  var param = _dataset[dataset][z][x][attr];

                  //is Array
                  if(Array.isArray(param)) {

                      //loop subitems
                      param2array[attr] = [];
                      for(y=0; y<_dataset[dataset][z][x][attr].length; y++) {
                          //append subitems in tr
                          param2array[attr][y]=[];
                          //append subitems in new tr
                          for(attr2 in _dataset[dataset][z][x][attr][y]) {

                              //additional mm CVE
                              if(attr2=='CVE' || attr2=='CPE' || attr2=='link') {

                                   $(param2).addClass(dataset+'-'+attr2);

                                   var cves = _dataset[dataset][z][x][attr][y][attr2].split(',');

                                   var cve_line = 1;
                                   for(let v=1; v<=cves.length; v++){
                                       var cves_diff = (v*7)-cves.length;
                                       if(cves_diff>=0) {
                                           cve_line++;
                                           break;
                                       }
                                   }
                                   additional_mm += cve_line*3;
                              }

                              var param2temp = $(param2).clone().append('<td style="padding-left:20px !important;">'+attr2+'</td><td>'+_dataset[dataset][z][x][attr][y][attr2]+'</td>');
                              param2temp2 += $(param2temp)[0].outerHTML;

                          }
                      }
                      var temp = $(new_a4_loop_model[dataset][x]);
                      var temp_after = $(temp).find('tr[after="'+attr+'"]');

                      $(temp_after).after(param2temp2);
                      new_a4_loop_model[dataset][x] = temp;

                  } else {

                      //if exists
                      if(new_a4_loop_model[dataset][x]) {

                          var temp = $(new_a4_loop_model[dataset][x]);
                          new_a4_loop_model[dataset][x] = $(new_a4_loop_model[dataset][x]).clone();
                          temp = new_a4_loop_model[dataset][x][0].outerHTML;
                          temp = temp.replaceArray(['##'+attr+'##'], [param]);

                          new_a4_loop_model[dataset][x] = temp;

                      } else {

                        //first time el populate
                        new_a4_loop_model[dataset][x] = $(a4_loop_model[x]).html().replaceArray(['##'+attr+'##'], [param]);

                        //list exception
                        if(dataset=='list'){
                            new_a4_loop_model[dataset][x] = $(a4_loop_model[x]).find('table').html().replaceArray(['##'+attr+'##'], [param]);
                        }
                      }
                  }

                  //additional mm ('solution_complete' || attr=='comments_complete')
                  if(attr=='solution_complete' || attr=='comments_complete') {
                    //br = $('<div>'+param+'</div>').find('br');
                    //additional_mm += (br.length*4);//4mm line

                    linebreak = param.replace(/(.{1,115})/g, '$1<br/>');
                    br = $('<div>'+linebreak+'</div>').find('br');
                    additional_mm += (br.length*4);//4mm line
                  }
               }

               //create final data array
               data[dataset][z][x] = [{
                   //'_length': new_a4_loop_model[dataset].length,
                   '_html': new_a4_loop_model[dataset][x],
                   '_mm': parseInt($(a4_loop_model[x]).attr('mm'))+additional_mm,
                   '_bypass': false,
                   '_childs': []
               }];
               additional_mm = 0;

               //alert(data[dataset][z][x][0]._html);
            }
          }
        } else {

          for(x=1; x <_dataset[dataset].length;x++) {
             //clone html model
             a4_loop_model[x] = $('.a4-loop-model[loop-item="'+dataset+'"]').clone();
             //new recipient
             var new_a4_loop_model = [];
             new_a4_loop_model[dataset] = [];
             //param2array
             var param2temp2 = '';
             //loop dataset items
             var param2array = [];

             var additional_mm = 0;

             for(attr in _dataset[dataset][x]) {

                 var param2temp2 = '';

                 //subparams to insert
                 var param2 = document.createElement('tr');
                 $(param2).addClass(dataset+'-subitem');
                 //$(param2).addClass(dataset+'-'+attr);
                 //params
                 var param = _dataset[dataset][x][attr];
                 //is Array
                 if(Array.isArray(param)) {
                     //loop subitems
                     param2array[attr] = [];
                     for(y=0; y<_dataset[dataset][x][attr].length; y++) {
                         //append subitems in tr
                         param2array[attr][y]=[];
                         //append subitems in new tr
                         for(attr2 in _dataset[dataset][x][attr][y]) {

                             //additional mm CVE
                             if(attr2=='CVE' || attr2=='CPE'|| attr2=='link') {

                                  $(param2).addClass(dataset+'-'+attr2);
                                  //var cves = _dataset[dataset][x][attr][y][attr2].split(',');
                                  var cves = _dataset[dataset][x][attr][y][attr2].split(',');

                                  var cve_line = 1;
                                  for(let v=1; v<=cves.length; v++){
                                      var cves_diff = (v*7)-cves.length;
                                      if(cves_diff>=0) {
                                          cve_line++;
                                          break;
                                      }
                                  }
                                  additional_mm += cve_line*2;
                             }

                             var param2temp = $(param2).clone().append('<td style="padding-left:20px !important;">'+attr2+'</td><td>'+_dataset[dataset][x][attr][y][attr2]+'</td>');
                             param2temp2 += $(param2temp)[0].outerHTML;

                         }
                     }

                     var temp = $(new_a4_loop_model[dataset][x]);
                     var temp_after = $(temp).find('tr[after="'+attr+'"]');
                     //alert(param2temp2);

                     $(temp_after).after(param2temp2);

                     new_a4_loop_model[dataset][x] = temp;
                 } else {

                     //if exists
                     if(new_a4_loop_model[dataset][x]) {

                         var temp = $(new_a4_loop_model[dataset][x]);
                         new_a4_loop_model[dataset][x] = $(new_a4_loop_model[dataset][x]).clone();
                         temp = new_a4_loop_model[dataset][x][0].outerHTML;
                         temp = temp.replaceArray(['##'+attr+'##'], [param]);
                         new_a4_loop_model[dataset][x] = temp;

                     } else {
                       //first time el populate
                       new_a4_loop_model[dataset][x] = $(a4_loop_model[x]).html().replaceArray(['##'+attr+'##'], [param]);
                     }
                 }

                 //additional mm ('solution_complete' || attr=='comments_complete')
                 if(attr=='solution_complete' || attr=='comments_complete'){

                    //br = $('<div>'+param+'</div>').find('br');
                    //additional_mm += (br.length*4);//4mm line

                    linebreak = param.replace(/(.{1,115})/g, '$1<br/>');
                    br = $('<div>'+linebreak+'</div>').find('br');

                    //alert(attr+'#'+br.length);

                    additional_mm += (br.length*3);//4mm line



                 }
              }
              //if exists
              /*if(param2temp2) {
                //alert($(new_a4_loop_model[dataset][x]).find('table tbody')[0].outerHTML);
                var temp2 = $(new_a4_loop_model[dataset][x]).clone();
                $(temp2).find('table tbody').append(param2temp2);
                new_a4_loop_model[dataset][x] = $(temp2)[0].outerHTML;
              }*/

              //create final data array
              data[dataset][x] = [{
                  //'_length': new_a4_loop_model[dataset].length,
                  '_html': new_a4_loop_model[dataset][x],
                  '_mm': parseInt($(a4_loop_model[x]).attr('mm'))+additional_mm,
                  '_bypass': false,
                  '_childs': []
              }];
              additional_mm=0;
           }

    }
}

//get childs
for(dataset in _dataset) {
    if(dataset=='finding' || dataset=='list') {

        for(z=1; z<_dataset[dataset].length; z++) {
          for(i=1; i<_dataset[dataset][z].length; i++) {
                if(_dataset[dataset][z][i].parent_id) {
                    //get parent array position
                    var childs_len = data[_dataset[dataset][z][i].parent_dataset][_dataset[dataset][z][i].parent_id][0]._childs.length;

                    data[_dataset[dataset][z][i].parent_dataset][_dataset[dataset][z][i].parent_id][0]._childs[i] = [{
                        '_dataset': dataset,
                        '_parent_id': _dataset[dataset][z][i].parent_id,
                        '_html': data[dataset][z][i][0]._html,
                        '_mm': data[dataset][z][i][0]._mm
                    }];
                    data[dataset][z][i][0]._bypass= true;
                }
            }
        }
    }
}

console.log(data);

//alert($(data['asset-finding'][1][0]._html).html())

//create queue
var queue = [];
var q=1;
for(dataset in data) {
    if(dataset=='finding' || dataset=='list') {

        for(z=1; z<data[dataset].length; z++){

            for(i=1; i< data[dataset][z].length; i++) {
                if(data[dataset][z][i][0]._bypass==false) {
                    queue[q] = [{
                        '_html': data[dataset][z][i][0]._html,
                        '_mm': data[dataset][z][i][0]._mm,
                        '_bypass': false,
                        '_dataset': dataset
                    }];

                    q++;
                    if(data[dataset][z][i][0]._childs.length>0) {
                        var last = false;
                        for(x=1; x<data[dataset][z][i][0]._childs.length; x++) {
                            if(x>=data[dataset][i][0]._childs.length-1) {
                                last = true;
                            }
                            queue[q] = [{
                                '_html': data[dataset][z][i][0]._childs[x][0]._html,
                                '_mm': data[dataset][z][i][0]._childs[x][0]._mm,
                                '_dataset': data[dataset][z][i][0]._childs[x][0]._dataset,
                                '_parent_childs_length': data[dataset][i][0]._childs.length,
                                '_parent_dataset': dataset,
                                '_parent_id': i,
                                '_bypass': false,
                                '_last': last
                            }];
                            q++;
                        }
                    }
                }
            }
        }
    } else {

        for(i=1; i< data[dataset].length; i++) {
            if(data[dataset][i][0]._bypass==false) {


                $(data[dataset][i][0]._html).find('table').attr('id', dataset+'-'+i);

                // _mm > 240
                if(data[dataset][i][0]._mm>240) {

                    var diff = data[dataset][i][0]._mm-240;

                    //alert(diff);
                    var comments_complete = $(data[dataset][i][0]._html).find('.comments-complete').clone();
                    var links = $(data[dataset][i][0]._html).find('.links').clone();
                    var links_tr = $(data[dataset][i][0]._html).find('#'+dataset+'-'+i+' .'+dataset+'-link');

                    //remove
                    $(data[dataset][i][0]._html).find('.comments-complete').remove();
                    $(data[dataset][i][0]._html).find('.links').remove();
                    $(links_tr).remove();

                    if(dataset=='asset-finding') {
                        var comments_model = $('.asset-finding-comments-complete').clone();
                        $(comments_model).find('.comments-container').html(comments_complete);
                        $(comments_model).find('.links-container').html(links);

                        for(l=0; l<links_tr.length; l++) {
                            $(comments_model).find('.links').after($(links_tr[l])[0].outerHTML);
                        }
                        var comments_html_a =  data[dataset][i][0]._html;
                        var comments_html_b = $(comments_model).html();
                    }
                    //table A
                    queue[q] = [{
                        '_html': comments_html_a,
                        '_mm': 239,
                        '_bypass': false,
                        '_dataset': dataset
                    }];
                    q++;

                    //table B
                    queue[q] = [{
                        '_html': comments_html_b,
                        '_mm': diff,
                        '_bypass': false,
                        '_dataset': dataset
                    }];
                    q++;
                } else {
                    queue[q] = [{
                        '_html': data[dataset][i][0]._html,
                        '_mm': data[dataset][i][0]._mm,
                        '_bypass': false,
                        '_dataset': dataset
                    }];
                    q++;
                }
                if(data[dataset][i][0]._childs.length>0) {

                    //alert(dataset)


                    var last = false;
                    for(x=1; x<data[dataset][i][0]._childs.length; x++) {
                        if(x>=data[dataset][i][0]._childs.length-1) {
                            last = true;
                        }

                        //////////////////////////////////////////////////
                        $(data[dataset][i][0]._childs[x][0]._html).find('table').attr('id', 'finding-'+x);

                        // _mm > 240
                        if(data[dataset][i][0]._childs[x][0]._mm>240) {

                            var diff = data[dataset][i][0]._childs[x][0]._mm-240;

                            var comments_complete = $(data[dataset][i][0]._childs[x][0]._html).find('.comments-complete').clone();
                            var links = $(data[dataset][i][0]._childs[x][0]._html).find('.links').clone();
                            var links_tr = $(data[dataset][i][0]._childs[x][0]._html).find('#finding-'+x+' .finding-link');

                            //remove
                            $(data[dataset][i][0]._childs[x][0]._html).find('.comments-complete').remove();
                            $(data[dataset][i][0]._childs[x][0]._html).find('.links').remove();
                            $(links_tr).remove();

                            var comments_model = $('.finding-comments-complete').clone();
                            $(comments_model).find('.comments-container').html(comments_complete);
                            $(comments_model).find('.links-container').html(links);

                            for(l=0; l<links_tr.length; l++) {
                                $(comments_model).find('.links').after($(links_tr[l])[0].outerHTML);
                            }
                            var comments_html_a =  data[dataset][i][0]._childs[x][0]._html;
                            var comments_html_b = $(comments_model).html();

                            //alert(comments_html_a)

                            //table A
                            queue[q] = [{
                                '_html': comments_html_a,
                                '_mm': 239,
                                '_dataset': data[dataset][i][0]._childs[x][0]._dataset,
                                '_parent_childs_length': data[dataset][i][0]._childs.length,
                                '_parent_dataset': dataset,
                                '_parent_id': i,
                                '_bypass': false,
                                '_last': last
                            }];
                            q++;

                            //table B
                            queue[q] = [{
                                '_html': comments_html_b,
                                '_mm': diff,
                                '_dataset': data[dataset][i][0]._childs[x][0]._dataset,
                                '_parent_childs_length': data[dataset][i][0]._childs.length,
                                '_parent_dataset': dataset,
                                '_parent_id': i,
                                '_bypass': false,
                                '_last': last
                            }];
                            q++;

                        } else {
                            queue[q] = [{
                                '_html': data[dataset][i][0]._childs[x][0]._html,
                                '_mm': data[dataset][i][0]._childs[x][0]._mm,
                                '_dataset': data[dataset][i][0]._childs[x][0]._dataset,
                                '_parent_childs_length': data[dataset][i][0]._childs.length,
                                '_parent_dataset': dataset,
                                '_parent_id': i,
                                '_bypass': false,
                                '_last': last
                            }];
                            q++;
                        }
                        //////////////////////////////////////////////////





                    }
                }
            }
        }
    }
}

console.log(queue);

//get total mm
var total_mm=0;
for(x=1; x<queue.length; x++) {
    total_mm += parseFloat(queue[x][0]._mm);
}

//get total of a4 dynamic pages
var temp=0;
var new_a4_total_pages=0;
for(i=0; i<240; i++) {
    var temp = total_mm/i;
    //if list
    if(Array.isArray(_dataset['list']))
        limit = 240;
    //if asset-finding
    else if (Array.isArray(_dataset['asset-finding']))
        limit = 200;
    else
        limit = 200;

    if(temp<=limit) {
      new_a4_total_pages = i;
      break;
    }
}

  //no findings exception
if(total_mm<180 && new_a4_total_pages==1) {
    new_a4_total_pages=0;
    //if no list array
    if(Array.isArray(_dataset['list'])) {
        new_a4_total_pages=1;
    }
}



//add pages in document
var doc = $('.document');
var a4 = $('.a4');
var a4_model = $('.a4-model').html();
var a4_prepend = $('.a4-prepend').find('.a4');
var a4_append = $('.a4-append').find('.a4');
var a4_dynamic_total = 500;
var a4_total = (a4_prepend.length+a4_append.length)+a4_dynamic_total;

//alert(new_a4_total_pages);

//a4 new array
var a4_new = [];
//add pages
for(let i=0; i<a4_dynamic_total; i++) {
    a4_new[i] = $(a4_model).clone();
    //add page
    $(doc).append(a4_new[i]);
    $(doc).append('<br />');
}
//add prepend and append
$(doc).append($('.a4-append').html());
$(doc).prepend($('.a4-prepend').html());


//a4 loop content
var a4_loop_content = $('.a4-loop-content:visible');
var y=0;

for(let i=1; i<a4_loop_content.length+1; i++) {
    //get loop content mm
    var a4_loop_content_mm = $(a4_loop_content[y]).attr('mm');
    //loop queue
    for(x=1; x<queue.length; x++) {

        if(queue[x][0]._bypass==false) {

            //alert('#'+x+' '+queue[x][0]._mm+' '+a4_loop_content_mm);

            if(parseFloat(queue[x][0]._mm) < parseFloat(a4_loop_content_mm)) {


                //alert('##'+x+'- '+queue[x][0]._html);

                a4_loop_content_mm = a4_loop_content_mm - queue[x][0]._mm;

                //if list exists
                if(queue[x][0]._dataset=='list') {

                    var parent_id = queue[x][0]._parent_id;
                    var list_table = $('.a4-loop-model[loop-item="list-table"]').clone();
                    var table_def = $(a4_loop_content[y]).find('.a4-table-'+queue[x][0]._dataset+'-'+parent_id).html();
                    var list_content = $(queue[x][0]._html).html();

                    //if a4-table-dataset-parent_id is ubdenfined
                    if(table_def==undefined) {

                        $(list_table).find('table').addClass('a4-table-'+queue[x][0]._dataset+'-'+parent_id);
                        $(list_table).find('table').addClass('table-striped');

                        //add table to area
                        $(a4_loop_content[y]).append($(list_table).html());
                        //remove table mm
                        //a4_loop_content_mm  = a4_loop_content_mm - 10;
                        //add item to table
                        $(a4_loop_content[y]).find('.a4-table-'+queue[x][0]._dataset+'-'+parent_id).append(list_content);

                        //add total
                        if(queue[x][0]._last==true) {
                            var list_total = $('.a4-loop-model[loop-item="list-total"]').find('tbody').clone();
                            $(list_total).find('h5').html(_dataset[queue[x][0]._parent_dataset][queue[x][0]._parent_id].total+' <b class="total-'+queue[x][0]._parent_id+'"> '+(queue[x][0]._parent_childs_length-1)+'</b>');
                            $(a4_loop_content[y]).find('.a4-table-'+queue[x][0]._dataset+'-'+parent_id).append(list_total);
                            a4_loop_content_mm = a4_loop_content_mm-$('.a4-loop-model[loop-item="list-total"]').attr('mm');

                            //alert(list_total);
                        }
                    } else {
                        //add item list
                        $(a4_loop_content[y]).find('.a4-table-'+queue[x][0]._dataset+'-'+parent_id).append(list_content);

                        //add total
                        if(queue[x][0]._last==true) {

                            var list_total = $('.a4-loop-model[loop-item="list-total"]').find('tbody').clone();
                            $(list_total).find('h5').html(_dataset[queue[x][0]._parent_dataset][queue[x][0]._parent_id].total+' <b class="total-'+queue[x][0]._parent_id+'"> '+(queue[x][0]._parent_childs_length-1)+'</b>');
                            $(a4_loop_content[y]).find('.a4-table-'+queue[x][0]._dataset+'-'+parent_id).append(list_total);
                            a4_loop_content_mm = a4_loop_content_mm-$('.a4-loop-model[loop-item="list-total"]').attr('mm');
                        }
                    }
                    //alert('list');
                //if not
                } else {
                    $(a4_loop_content[y]).append(queue[x][0]._html);
                }
                //bypass item in queue
                queue[x][0]._bypass = true;
            } else {


                //alert('#'+x+' '+queue[x][0]._mm+' '+a4_loop_content_mm);
                break;
            }
        }
    }
    y++;
}


//addClass a4-i
var a4num = $('.a4:visible');
x=1;
for(i=0; i<a4num.length; i++) {

    var a4_loop_content = $(a4num[i]).find('.a4-loop-content').html();

    if(a4_loop_content!=''){

        $(a4num[i]).addClass('a4-'+x);

        if(x<10) {
            var pnstyle = 'style="padding-left:8px;""';
        } else if(x>=100) {
             pnstyle = 'style="padding-left:2px";';
        } else {
             pnstyle = '';
        }
        $(a4num[i]).append('<div '+pnstyle+' class="page-number">'+x+'</div>');
        x++;
    } else {
      //hide excedent a4
      $(a4num[i]).hide();
      //hide excedent br
      if($(a4num[i]).next()[0].tagName=='BR'){
          $(a4num[i]).next().hide();
      }
    }
}

//more container
var more_container = $('.more-container');
for(let i=0; i<more_container.length; i++) {
    var temp = $(more_container[i])[0].outerHTML;
    $(more_container[i]).html(temp.replace('...', '... <div class="more"><i>+</i></div>'));
    $(more_container[i]).find('.more').mouseover(function(){
        $(this).parent().find('.more-content').show();
    });
    $(more_container[i]).find('.more').mouseout(function(){
        $(this).parent().find('.more-content').hide();
    });
}

//no findings exception
if(total_mm<180 && new_a4_total_pages==0){
    $('.finding-results-title').hide();
}
