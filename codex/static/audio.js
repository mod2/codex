$(document).ready(function() {
	// Audio transcription
	var startTime = $("audio").attr("data-start-time");
	var endTime = $("audio").attr("data-end-time");
	var mePlayer = new MediaElementPlayer("audio", {
		features: ['playpause', 'rewind', 'current', 'progress', 'duration', 'volume'],
		enableKeyboard: false,
		success: function(mediaElement, domObject) {
			// Start at the start time
			if (startTime) {
				mediaElement.setCurrentTime(startTime);	
			}

			// Don't go past the end time
			if (endTime) {
				mediaElement.addEventListener("timeupdate", function(data) {
					if (mediaElement.currentTime >= endTime) {
						mediaElement.pause();	
					}
				});
			}

			// Seeking (should we keep this?)
			if (startTime || endTime) {
				mediaElement.addEventListener("seeked", function() {
					if (mediaElement.currentTime < startTime) {
						mediaElement.setCurrentTime(startTime);
					}
					if (mediaElement.currentTime > endTime) {
						mediaElement.setCurrentTime(endTime);
					}
				});
			}
		}
	});


	// Play/pause toggle
	$(".transcript textarea").bind("keydown", "shift+space", function() {
		if (mePlayer.media.paused) {
			mePlayer.media.play();
		} else {
			mePlayer.media.pause();
		}

		$("audio").blur();

		return false;
	});

	// Rewind 30 seconds
	$(".transcript textarea").bind("keydown", "ctrl+h", function() {
		mePlayer.media.setCurrentTime(mePlayer.media.currentTime - 30);

		if (startTime && mePlayer.media.currentTime < startTime) {
			mePlayer.media.setCurrentTime(startTime);
		}

		return false;
	});

	// Rewind 5 seconds
	$(".transcript textarea").bind("keydown", "ctrl+j", function() {
		mePlayer.media.setCurrentTime(mePlayer.media.currentTime - 5);

		if (startTime && mePlayer.media.currentTime < startTime) {
			mePlayer.media.setCurrentTime(startTime);
		}

		return false;
	});

	// Fast forward 5 seconds
	$(".transcript textarea").bind("keydown", "ctrl+k", function() {
		mePlayer.media.setCurrentTime(mePlayer.media.currentTime + 5);

		if (endTime && mePlayer.media.currentTime > endTime) {
			mePlayer.media.setCurrentTime(endTime);
		}

		return false;
	});

	// Fast forward 30 seconds
	$(".transcript textarea").bind("keydown", "ctrl+l", function() {
		mePlayer.media.setCurrentTime(mePlayer.media.currentTime + 30);

		if (endTime && mePlayer.media.currentTime > endTime) {
			mePlayer.media.setCurrentTime(endTime);
		}

		return false;
	});

	// Jump to beginning
	$(".transcript textarea").bind("keydown", "ctrl+0", function() {
		if (startTime) {
			mePlayer.media.setCurrentTime(startTime);
		} else {
			mePlayer.media.setCurrentTime(0);
		}

		return false;
	});
});
