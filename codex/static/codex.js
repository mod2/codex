// Variable for stashing transcript text (for autosave)
var transcriptionText = '';

$(document).ready(function() {
	// From https://gist.github.com/alanhamlett/6316427
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE' || settings.type == 'PATCH') {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		}
	});

	// Preload transcription if it's there
	transcriptionText = $(".transcript textarea").val();

	$(".toggle-layout").on("click", function() {
		$("#main.transcribe").toggleClass("side-by-side");

		var userId = $("#user-id").html();
		var newLayout = $("#main.transcribe").hasClass("side-by-side") ? "side_by_side" : "stacked";

		// Update just the user list
		$.ajax({
			url: '/accounts/api/users/' + userId + '/',
			method: 'PATCH',
			contentType: 'application/json',
			data: JSON.stringify({ layout: newLayout }),
			success: function(data) {
			},
			error: function(data) {
				console.log("error", data);
			},
		});
	});

	$(".toggle-lights").on("click", function() {
		$("body").toggleClass("dark");

		var userId = $("#user-id").html();
		var newTheme = $("body").hasClass("dark") ? "dark" : "light";

		// Update just the user list
		$.ajax({
			url: '/accounts/api/users/' + userId + '/',
			method: 'PATCH',
			contentType: 'application/json',
			data: JSON.stringify({ theme: newTheme }),
			success: function(data) {
			},
			error: function(data) {
				console.log("error", data);
			},
		});
	});

	$("#name-fieldset input[type=text]").on("keyup", function(e) {
		var url = '/transcribe/api/projects/';
		var method = 'POST';
		var field = $(this);
		var newName = $(this).val().trim();
		var owner = $("#user-id").html();

		// If it's blank, just ignore it
		if (newName == '') {
			return false;
		}

		// Put loading sign up
		var savedSign = $(this).parents("fieldset:first").find("span.saved");
		savedSign.html('...').removeClass("error").show();

		// Check to see if the project has already been created
		if (typeof field.attr("data-id") != 'undefined') {
			// Already created, so update the name
			// (If it isn't created yet, we don't need to do anything special here)
			url += field.attr("data-id") + "/";
			method = 'PUT';
		} else {
			if (field.hasClass("inprogress")) {
				// Don't do anything because we're still waiting for the first
				// AJAX request to come back
				return false;
			} else {
				// Add the inprogress class so we know not to duplicate requests
				field.addClass("inprogress");
			}
		}

		$.ajax({
			url: url,
			method: method,
			data: {
				name: newName,
				owner: owner,
			},
			success: function(data) {
				savedSign.html("Saved");

				// Add ID if it came back and it's not already there
				if (data.id && typeof field.attr("data-id") == 'undefined') {
					$("#name-fieldset input[type=text]").attr("data-id", data.id);
				}

				// Check to see if we're in progress and turn off the flag
				if (field.hasClass("inprogress")) {
					field.removeClass("inprogress");
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

		$(".modal form").hide();
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

	// Helper function to recognize file type
	function getFileType(filename) {
		var extension = filename.slice(filename.lastIndexOf('.') + 1);

		switch (extension) {
			case 'jpg':
			case 'jpeg':
			case 'gif':
			case 'png':
			case 'tif':
			case 'tiff':
				return 'image';
			case 'mp3':
			case 'wav':
			case 'aiff':
				return 'audio';
			case 'mov':
			case 'm4v':
			case 'mp4':
				return 'video';
			default:
				return 'unknown';
		}
	}

	function parseDropboxLink(link) {
		return link.replace("www.dropbox", "dl.dropbox").replace("?dl=0", "?dl=1");
	}

	// Add Dropbox if it's included
	if ($("script#dropboxjs").length > 0) {
		var options = {
			success: function(files) {
				var projectId = $("#name-fieldset input.name").attr("data-id");

				// What order # to start with (start with - 1 because we += 1 before)
				var order = $("#item-list .item").length - 1;

				var items = $.map(files, function(file, i) {
					order += 1;
					return {
						'name': file.name,
						'url': parseDropboxLink(file.link),
						'type': getFileType(file.name),
						'project': parseInt(projectId),
						'source_type': 'dropbox',
						'order': order,
					};
				});

				// Send this to the Codex API
				$.ajax({
					url: '/transcribe/api/projects/' + projectId + '/items/',
					method: 'POST',
					data: JSON.stringify(items),
					contentType: "application/json; charset=utf-8",
					dataType: "json",
					success: function(returnedItems) {
						// Update the item list on the page
						$.map(returnedItems, function(item, i) {
							var html = "<div class='item new' data-id='" + item.id + "'>";
							html += "<span>" + item.name + "</span>\n";
							html += "<div class='controls'>\n";
							html += "<span class='delete'>x</span>\n";
							html += "<span class='edit'>e</span>\n";
							html += "<span class='reorder'>=</span>\n";
							html += "</div>\n";
							html += "</div>";

							$("#item-list").append(html);
						});

						// Close the modal
						hideModal();
					},
					error: function(data) {
						console.log("error", data);
					},
				});
			},
			cancel: function() {
			},
			linkType: 'preview',
			multiselect: true,
			extensions: ['images', '.mp3'],
		};

		var button = Dropbox.createChooseButton(options);

		// Add the button to the form
		$("form.add-items section .main article[data-type=dropbox]").append(button);
	}


	// Autocomplete for adding users to a project
	var options = {
		serviceUrl: '/accounts/api/users/',
		paramName: 'search',
		transformResult: function(response) {
			// Load as JSON
			response = JSON.parse(response);

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
			// Get list of users' emails
			var userEmails = $.map($("div.userlist div.user"), function(user) {
				return $(user).attr("data-email");
			});

			if ($.inArray(suggestion.data, userEmails) == -1) {
				$("input[name=user-email]").val(suggestion.data);

				addUserToProject();
			} else {
				$("#add-user-autocomplete").val('');
			}

			return false;
		},
		triggerSelectOnValidInput: false,
	};

	// Edit project page stuff
	if ($("form.edit-project").length > 0) {
		// Hook up user autocomplete
		$("#add-user-autocomplete").autocomplete(options);

		// Add User button
		$("#add-user-button").on("click", addUserToProject);

		// Reordering items on Edit Project page
		$("#item-list.sortable").sortable({
			placeholder: "item placeholder",
			handle: ".reorder",
			update: function(event, ui) {
				var order = {};
				var items = ui.item.parents("#item-list:first").find("div.item");

				for (var i=0; i<items.length; i++) {
					var item = $(items[i]);
					order[item.attr("data-id")] = i;
				}

				var projectId = $("fieldset#name-fieldset input[type=text]").attr("data-id");
				var url = '/transcribe/api/projects/' + projectId + '/items/update_order/';

				$.ajax({
					url: url,
					method: 'POST',
					contentType: 'application/json',
					data: JSON.stringify(order),
					success: function(data) {
					},
					error: function(data) {
						console.log("Error! :(", data);
					},
				});
			},
		});

		function addUserToProject() {
			var userName = $("#add-user-autocomplete").val();
			var userEmail = $("input[name=user-email]").val();

			if (userName && userEmail != userName && userEmail != '') {
				// They typed in a user who has set a name
				var displayName = userName + " (" + userEmail + ")";
			} else if (userName && userEmail == '') {
				// They typed an email in that wasn't in the system
				var displayName = userName;
				userEmail = userName;
			} else {
				// They typed in an email for a user who hasn't set a name
				var displayName = userEmail;
			}

			// Add them to the list
			$("div.userlist").append("<div class='user' style='display: none; height: 1em;' data-email='" + userEmail + "'>" + displayName + " <span class='delete'>x</span></div>");
			$("div.userlist div.user:last-child").slideDown(150, function() {
				// Send it to the server
				updateUserList();

				// Clear out the text box and hidden field
				$("#add-user-autocomplete").val('');
				$("input[name=user-email]").val('');

				// Don't focus on the button anymore
				$("#add-user-button").blur();
			});

			return false;
		}

		$("div.userlist").on("click", "div.user span.delete", function() {
			// Remove from the user list

			$(this).parents("div.user").slideUp(150, function() {
				$(this).remove();
				updateUserList();
			});

			return false;
		});


		// Send user list to web service
		function updateUserList() {
			// Get project ID
			var projectId = $("fieldset#name-fieldset input[type=text]").attr("data-id");

			// Get user list (emails)
			var userList = $.map($("div.userlist div.user"), function(user) {
				return $(user).attr("data-email");
			});

			// Put loading sign up
			var savedSign = $("fieldset#user-list").find("span.saved");
			savedSign.html('...').removeClass("error").show();

			// Update just the user list
			$.ajax({
				url: '/transcribe/api/projects/' + projectId + '/',
				method: 'PATCH',
				contentType: 'application/json',
				data: JSON.stringify({ users: userList }),
				success: function(data) {
					savedSign.html("Saved");
				},
				error: function(data) {
					savedSign.html("Error").addClass("error");
					console.log("error", data);
				},
			});

			return false;
		}


		// Show delete modal for deleting an item
		$("#item-list").on("click", ".item .controls .delete", function() {
			// Tell the modal which item we're on
			$(".modal .delete-item input[type=submit]").attr("data-id", $(this).parents(".item:first").attr("data-id"));

			// Tell the modal which project we're on
			var projectId = $("fieldset#name-fieldset input[type=text]").attr("data-id");
			$(".modal .delete-item input[type=submit]").attr("data-project-id", projectId);

			// Show the modal
			showModal("delete-item");

			return false;
		});

		// Actually delete the item
		$(".modal .delete-item input[type=submit]").on("click", function() {
			var itemId = $(this).attr("data-id");
			var projectId = $(this).attr("data-project-id");
			var url = "/transcribe/api/projects/" + projectId + "/items/" + itemId;

			$.ajax({
				url: url,
				method: 'DELETE',
				success: function(data) {
					// Hide modal
					hideModal();

					// Remove it from the items list
					$("#item-list .item[data-id=" + itemId + "]").slideUp(150, function() {
						$(this).remove();
					});
				},
				error: function(data) {
					console.log("Error deleting item", data);
				},
			});

			return false;
		});


		// Show modal for renaming an item
		$("#item-list").on("click", ".item .controls .edit", function() {
			// Tell the modal which item we're on
			$(".modal .edit-item input[type=submit]").attr("data-id", $(this).parents(".item:first").attr("data-id"));

			// Tell the modal which project we're on
			var projectId = $("fieldset#name-fieldset input[type=text]").attr("data-id");
			$(".modal .edit-item input[type=submit]").attr("data-project-id", projectId);

			// Prepopulate the name field
			var oldName = $(this).parents(".item:first").find("span a").html();
			$(".modal .edit-item input[type=text]").val(oldName);

			// Show the modal
			showModal("edit-item");

			$(".modal .edit-item input[type=text]").focus();

			return false;
		});

		// Actually edit the item
		$(".modal .edit-item input[type=submit]").on("click", function() {
			var itemId = $(this).attr("data-id");
			var projectId = $(this).attr("data-project-id");
			var url = "/transcribe/api/projects/" + projectId + "/items/" + itemId;

			var newName = $(".modal .edit-item input[name=name]").val().trim();

			if (newName != '') {
				$.ajax({
					url: url,
					method: 'PATCH',
					contentType: 'application/json',
					data: JSON.stringify({ name: newName }),
					success: function(data) {
						// Hide modal
						hideModal();

						// Update it in the items list
						$("#item-list .item[data-id=" + itemId + "] span a").html(newName);
					},
					error: function(data) {
						console.log("Error updating item", data);
					},
				});
			}

			return false;
		});
	}

	// Autosaving (only on transcribe pages), every 5 seconds (5000 ms)
	if ($("#main").hasClass("transcribe")) {
		// On typing into the textarea, clear the "Saved." text
		$(".transcript textarea").on("keypress", function() {
			$("label.saved").html("");
		});

		// Autosave
		var intervalId = window.setInterval(function() {
			var currentTranscript = $(".transcript textarea").val().trim();

			if (currentTranscript != transcriptionText) {
				// The text has changed, so autosave it
				$("label.saved").html("Saving...");

				var itemId = $(".transcript").attr("data-id");
				var projectId = $(".transcript").attr("data-project-id");
				var url = "/transcribe/api/projects/" + projectId + "/items/" + itemId + "/transcripts/";

				// Post it
				$.ajax({
					url: url,
					method: 'POST',
					contentType: 'application/json',
					data: JSON.stringify({
						text: currentTranscript,
						owner: $("#user-id").html(),
						item: itemId,
						status: 'draft',
					}),
					success: function(data) {
						$("label.saved").html("Saved.");

						transcriptionText = currentTranscript;
					},
					error: function(data) {
						$("label.saved").html("Error saving. Trying again...");

						console.log("error", data);
					},
				});
			}
		}, 5000);
	}
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
