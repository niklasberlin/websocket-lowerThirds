function addForm(){
    $container = $('<div class="form-container"></div>');
    $form = $('<form action="http://'+window.location.host+'/api" metgod="get"></form>');
    $form.append('<label for="l1">Line One:</label>');
    $form.append('<input type="text" id="l1" name="l1">');
    $form.append('<label for="l2">Line Two:</label>');
    $form.append('<input type="text" id="l2" name="l2">');
    $form.append('<label for="d">Delay: (ms, 2000 - 20000)</label>');
    $form.append('<input type="range" id="d" name="d" min=2000 max=20000 step=100 value="4000">');
    $form.append('<input type="submit" value="SHOW">');
    $form.append('<input type="button" class="btn-delete" value="X" onClick="formDelete(this)">');
    $container.append($form);
    $('.grid').append($container);
}

function save(){

}

function load(){


}

function formDelete(elem){
    $(elem).parent().parent().remove();

}

$('form').live('submit', function(){
    $.get($(this).attr('action'), $(this).serialize(), function(response){
          // do something here on success
          console.log("ping");
          $(this).addClass("disabled");
          setTimeout(function(){
            $(this).removeClass("disabled");
          }, $(this).children("#d").val());
    },'json');
    return false;
 });