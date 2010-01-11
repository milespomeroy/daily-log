$(document).ready(function(){
	typed=0;
	posted=0;
	
	$('textarea').keyup(function() {
		typed++;
		$('#status').html('Typed: '+typed+' Posted: '+posted);
	});
	
	$('textarea').keyup(function() {
		$('#button').val('Saving...');
		setTimeout(function() {
			// $.post("/post", $("textarea").serialize());
			// 			$('#status').html('saved');
			if (typed==1)
			{
				posted++;
				$('#button').val('Saved');
			}
			typed--;
		}, 2000);
	});
});