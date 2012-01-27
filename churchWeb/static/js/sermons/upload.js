$(document).ready(function(){
	uploadInit();
});

function uploadInit() {
	$('.buttons').button();
	$('#tabs').tabs();
	$('#id_sermonDate').datepicker();
	$( "#dialog-uploadForm" ).dialog({
		autoOpen: false,
		show:'blind',
		hide:'explode',
		height: 310,
		width: 520,
		modal: true,
		buttons: {
			"Submit changes": function() {
				submitDialog();
				$(this).dialog('close');
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},
	});
	$( "#dialog-folderForm" ).dialog({
		autoOpen: false,
		show:'blind',
		hide:'explode',
		height: 310,
		width: 520,
		modal: true,
		buttons: {
			"Submit changes": function() {
				submitFolderDialog();
				$(this).dialog('close');
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},
	});
	$('.editSermon').click(function(){openDialog($(this));})
	$('.errorlist').next().addClass('ui-state-error');
	$( "#accordion" ).accordion({
		autoHeight:false,
	});
}

function openDialog(obj){
	populateForm(obj);
	$('#dialog-uploadForm').dialog('open');
}

function openFolderDialog(obj){
	populateForm(obj);
	$('#dialog-folderForm').dialog('open');
}

function populateForm(obj){
	text = "<input type='hidden' name='pk' value='" + obj.attr('pk') + "'></input>";
	$('#dialog-uploadForm').empty();
	$('#dialog-uploadForm').attr('title',obj.html());
	$('#dialog-uploadForm').append($('#blankForm').clone().append(text));
}

function populateFolderForm(obj){
	text = "<input type='hidden' name='pk' value='" + obj.attr('pk') + "'></input>";
	$('#dialog-fileForm').empty();
	$('#dialog-fileForm').attr('title',obj.html());
	$('#dialog-fileForm').append($('#blankFolderForm').clone().append(text));
}

function submitDialog() {
	$.ajax({
		type:'POST',
		url:$('#uploadFormHTML').attr('url') + '/' +  Math.floor(Math.random()*1000),
		data:$('#uploadFormHTML').serialize(),
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
	} else {
		$('#tabs-2-content').remove();
		$('#tabs-2').load('#uploadFormHTML').attr('url') + '/' +  Math.floor(Math.random()*1000 + ' #tabs-2-content');
	}
	$('#uploadFormWrapper').html($(data).find('#uploadFormWrapper').html());
	baseInit();
	uploadInit();
}