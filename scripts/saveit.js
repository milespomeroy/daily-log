$(document).ready(function(){
	
	$('.cal').click(function(){
		$('.date').text('Friday, December 12, 2012');
		$("input[name='year']").val('2012');
		$("input[name='month']").val('12');
		$("input[name='day']").val('12');
		$("textarea").val('The Future is Here.');
	});
	
	// set the typed global variable
	var typed = 0;
	
	$('textarea').keyup(function() {
		// increment typed to show that typing is occuring
		typed++;
		// saving is happening
		$('#status').html('Saving...');
		
		// wait for 2 secs then see if there has been more typing.
		// if not, post the entry form. And mark it saved.
		// if so, subtract your number from the typed variable.
		setTimeout(function() {
			if (typed === 1)
			{
				// post individual elements instead of the whole form to 
				// bypass Safari content not saved dialog.
				$.post("/post", {
					content: $("textarea").val(),
					year: $("input[name='year']").val(),
					month: $("input[name='month']").val(),
					day: $("input[name='day']").val()	
					});
				$('#status').html('Saved');
			}
			typed--;
		}, 2000);
	});
});