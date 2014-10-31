$(document).ready(function() {
	$(".toggle-layout").on("click", function() {
		$("#main.transcribe").toggleClass("side-by-side");
	});

	$(".toggle-lights").on("click", function() {
		$("body").toggleClass("dark");
	});
});
