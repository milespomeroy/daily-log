$(document).ready(function(){
	// set the typed global variable
	typed=0;
	
	$('textarea').keyup(function() {
		// increment typed to show that typing is occuring
		typed++;
		// saving is happening
		$('#status').html('Saving...');
		
		// wait for 2 secs then see if there has been more typing.
		// if not, post the entry form. And mark it saved.
		// if so, subtract your number from the typed variable.
		setTimeout(function() {
			if (typed==1)
			{
				$.post("/post", $("#entry").serialize());
				$('#status').html('Saved');
			}
			typed--;
		}, 2000);
	});
});