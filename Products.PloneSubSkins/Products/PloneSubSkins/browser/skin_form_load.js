function loadPloneSubSkinsForm() {
   if (jQuery('form#subskins_prefs_styles')[0] == null) {
	   jQuery.get('css_debug_mode_control', null, function(data, textstatus){
	       if (data=='true') {
		   doLoadPloneSubSkinsForm();
	       } else {
		   if (confirm("Css debug mode is off. Do you want to turn it on and configure the skin?")) {
		       jQuery.get('css_debug_mode_control', {enable:'1'}, function(data, textstatus){
			   window.location.reload();
		       });
		   }
		   
	       }       
	   }, 'text'); 
   }
}

function doLoadPloneSubSkinsForm() {
    jQuery.get("subskins_choice_form", {detatched:true}, 
		    function(data, textstatus){
		        jQuery('body').append(data);
			var hidden_came_from = '<';
			hidden_came_from += 'input type="hidden" name="came_from" value="';
			hidden_came_from += window.location.href;
			hidden_came_from += '" />';
			jQuery('form#subskins_prefs_styles').append(hidden_came_from);
			jQuery('#subskins_prefs_styles legend').click(function(){
				jQuery('#choice_form_body').toggle()
			});
		    }
    , 'text');
}
jQuery(function(){
	jQuery('#siteaction-subskins_setup a').click(function(e){
		e.preventDefault();
		loadPloneSubSkinsForm();
	});
});
