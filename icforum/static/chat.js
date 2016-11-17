
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function csrfSafeMethod(method) {
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function updateChatUI() {
	$('.footer .btn').click(function(){
		$(this).parent().find('input').focus();
	});

	$('.chat').keypress(function(e) {
		if(e.which == 13) {
			e.preventDefault();
			$.ajax({
				url: '/chat/api/chat_messages/',
				type: 'POST',
				data: {
					'room': parseInt($(this).parent().parent().attr('id').substring(5)),
					'content': $(this).val()
				},
				dataType: 'json',
				success: function(response, status) {
					updateChat();
					$(this).val('');
				},
				error: function(response, status, error) {
					alert('Chat connection trouble, message couldn\'t be sent ! Please check your network connection and try again.');
				}
			});
			$(this).val('');
		}
	});
}

function updateChat() {
	$.ajax({
		url: '/chat/api/rooms/',
		type: 'GET',
		dataType: 'json',
		success: function(response, status) {
			for(var i = 0; i < response.length; i++) {
				if(!$('#chat_'+response[i].id.toString()).length) {
					var members = '';
					for(var k = 0; k < response[i].members.length; k++) {
						members += response[i].members[k].username + ' ,';
					}
					$('#chatbox').append('<div class="dropup" id="chat_'+response[i].id.toString()+'"><button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">'+((response[i].name)?response[i].name:members)+'<span class="caret"></span></button><div class="dropdown-menu"><ul class="chatlist"></ul><input type="text" class="chat" /></div></div>'); // Duplicated HTML code in _base.html
					updateChatUI();
				}
				$.ajax({
					url: '/chat/api/chat_messages/',
					type: 'GET',
					dataType: 'json',
					success: function(response, status) {
						$('#chaterror').html('');
						for(var j = 0; j < response.length; j++) {
							if(!$('#chat_msg_'+response[j].id.toString()).length)
								$('#chat_'+response[j].room.toString()+' ul').append('<li id="chat_msg_'+response[j].id.toString()+'"><strong>'+response[j].author.username+' : </strong>'+response[j].content+'</li>');
						}
						$('.chatlist').each(function(index) {
							$(this).scrollTop($(this).scrollHeight);
						});
					},
					error: function(response, status, error) {
						$('#chaterror').html('Problem with connection !');
					}
				});
			}
		},
		error: function(response, status, error) {
			$('#chaterror').html('Chat connection trouble !');
		}
	});
}

$(document).ready(function(){
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
			}
		}
	});
	updateChatUI();
	setInterval(updateChat, 2000);
});
