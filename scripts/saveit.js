$(document).ready(function(){
	
// Change date using the calendar	
	$('.cal').date_input({ 
		changeEntry: function(year, month, day) {
			$("input[name='year']").val(year);
			$("input[name='month']").val(month);
			$("input[name='day']").val(day);
		
			$("textarea").val(function(){
				var val = null;

				$.ajax({
					'async': false,
					'global': false,
					'url': '/get',
					'data': ({
						year: year,
						month: month,
						day: day
						}),
					'success': function(data){
						val = data;
					}
				});

				return val;
			});
		} 
	});

// Save with AJAX
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