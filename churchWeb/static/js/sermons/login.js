$(document).ready(function(){
	$('#tabs').tabs();
	$('#id_sermonDate').datepicker();
});

function login() {
	$.ajax({
		type:'POST',
		url:$('#sermonFormHTML').attr('url') + '/' +  Math.floor(Math.random()*1000),
		data:$('#sermonFormHTML').serialize(),
		success: function(data){checkResult(data);},
	});
	return false;
}

function checkResult(data) {
	if ($(data).find('#error').size()!=0){
		$.notifyBar({
			context:document.body,
    		html: $(data).find('#error').html(),
    		delay: 1000,
    		animationSpeed: "normal",
    		cls: "error"
    	});
		$('#sermonFormWrapper').html($(data).find('#sermonFormWrapper').html());
		baseInit();
	} else {
		window.location = '/upload';
	}
}