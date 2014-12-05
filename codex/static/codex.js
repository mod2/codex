$(document).ready(function() {
	// From https://gist.github.com/alanhamlett/6316427
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		}
	});

	$(".toggle-layout").on("click", function() {
		$("#main.transcribe").toggleClass("side-by-side");
	});

	$(".toggle-lights").on("click", function() {
		$("body").toggleClass("dark");
	});

	$("#title-fieldset input[type=text]").on("keyup", function(e) {
		var url = '/transcribe/api/projects/';
		var method = 'POST';
		var field = $(this);

		// Put loading sign up
		var savedSign = $(this).parents("fieldset:first").find("span.saved");
		savedSign.html('...').removeClass("error").show();

		// Check to see if the project has already been created
		if (typeof field.attr("data-id") != 'undefined') {
			// Already created, so update the title
			// (If it isn't created yet, we don't need to do anything special here)
			url += field.attr("data-id") + "/";
			method = 'PUT';
		}

		var newTitle = $(this).val().trim();
		var owner = $("#user-id").html();

		$.ajax({
			url: url,
			method: method,
			data: {
				name: newTitle,
				owner: owner,
			},
			success: function(data) {
				savedSign.html("Saved");

				// Add ID if it came back and it's not already there
				if (data.id && typeof field.attr("data-id") == 'undefined') {
					field.attr("data-id", data.id);
				}

				// Fade in the rest
				$("fieldset.faded").removeClass("faded");
			},
			error: function(data) {
				savedSign.html("Error").addClass("error");
			},
		});
	});

	// Modal helper functions
	function showModal(type) {
		$(".modal-background").fadeIn(100);

		$(".modal ." + type).show();
		$(".modal").fadeIn(100);
	}

	function hideModal() {
		$(".modal").fadeOut(100);
		$(".modal-background").fadeOut(100);
	}

	// General modal cancel
	$(".modal a.cancel-link").on("click", function() {
		hideModal();
		return false;
	});

	$(".modal-background").on("click", function() {
		hideModal();
		return false;
	});


	// Show delete modal
	$(".delete-project-link").on("click", function() {
		showModal("delete-project");
		return false;
	});

	// Actually delete the project
	$(".modal .delete-project input[type=submit]").on("click", function() {
		var projectId = $(this).attr("data-id");
		var url = "/transcribe/api/projects/" + projectId;

		$.ajax({
			url: url,
			method: 'DELETE',
			success: function(data) {
				// Hide modal
				hideModal();

				// Redirect to dashboard
				window.location.href = "/";
			},
			error: function(data) {
				$(this).siblings("h2").html("Error");
				$(this).siblings("label").html("Error deleting project.");
				$(this).parents("form:first").addClass("error");
				console.log(data);
			},
		});

		return false;
	});


	// Add items modal
	$("#add-items-button").on("click", function() {
		showModal("add-items");
		return false;
	});

	// Toggle between item source type
	$("form.add-items section ul li span").on("click", function() {
		var newType = $(this).attr("data-type");

		$("form.add-items section .main article:visible").hide();
		$("form.add-items section .main article[data-type=" + newType + "]").show();

		$("form.add-items section ul li span.selected").removeClass("selected");
		$("form.add-items section ul li span[data-type=" + newType + "]").addClass("selected");
	});


	// Autocomplete for adding userst to a project
	var options = {
		serviceUrl: '/account/api/users/',
		paramName: 'search',
		transformResult: function(response) {
			// Load as JSON
			response = JSON.parse(response);
			console.log(response);

			// Map name/email to the format the plugin wants (value/data)
			return {
				suggestions: $.map(response, function(item) {
					if (item.name) {
						return { value: item.name, data: item.email };
					} else {
						return { value: item.email, data: item.email };
					}
				})
			};
		},
		formatResult: function(suggestion, currentValue) {
			return '<div id="' + suggestion.data + '">' + suggestion.value + '</div>';
		},
		onSelect: function(suggestion) {
			$("input[name=user-email]").val(suggestion.data);
			return false;
		},
		triggerSelectOnValidInput: false,
	};

	$("#add-user-autocomplete").autocomplete(options);

	// Add User button
	$("#add-user-button").on("click", function() {
		var userName = $("#add-user-autocomplete").val();
		var userEmail = $("input[name=user-email]").val();

		if (userName && userEmail != userName && userEmail != '') {
			// They typed in a user who has set a name
			var displayName = userName + " (" + userEmail + ")";
		} else if (userName && userEmail == '') {
			// They typed an email in that wasn't in the system
			var displayName = userName;
		} else {
			// They typed in an email for a user who hasn't set a name
			var displayName = userEmail;
		}

		// Add them to the list
		$("div.userlist").append("<div class='user'>" + displayName + "<span class='delete'>x</span></div>");

		// Clear out the text box and hidden field
		$("#add-user-autocomplete").val('');
		$("input[name=user-email]").val('');

		// Don't focus on the button anymore
		$("#add-user-button").blur();

		return false;
	});
});

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i=0; i<cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
