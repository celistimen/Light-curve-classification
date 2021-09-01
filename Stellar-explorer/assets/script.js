// This is not the file you're looking for
// This script contains a combination of tooltips, and small snippets of code to ensure a smooth user experience

// help.json contains data for a help button


console.log("Custom script.js is active")

// this runs after 10s to ensure that the webpage is loaded correctly, then modifications can be made to the UI
window.onload = function(){
	setTimeout(onStartListener, 10000)
}

// This only works the first time the page is loaded, if the app is restarted (as Dash does on an update, this does not get called)
// can be used to add tooltips 
function onStartListener() {	
	addTooltips();	
}


// ------------------ Tooltips:------------------------- (not used at the moment)
// object which contains all the id's and information
tooltipobj = {    'example_id':'Example explanation...',
}
				
//chechklists are a bit more tedious to add tooltips
checklist_tooltips = {
	"checklist1_id":[
		"item_1_explanation", 
		"item_2_explanation"],
	"checklist2_id":[
		"item_1_explanation", 
		"item_2_explanation"],
}

function addTooltips(){
	// normal objects
	for (var key in tooltipobj) {
		// the object that should have a tooltip
		try{
			tooltipped_object = document.getElementById(key);
			// check whether the tooltip should be on the right or left side, to prevent it from going out of the window
			tooltip_position = getPosition(tooltipped_object)
			
			addTooltipText(tooltipped_object, tooltipobj[key], tooltip_position)
		}
		catch(err){
			console.log("Node "+ key + " is not found in the layout, no tooltip is attached. (addTooltips)")
		}
	}
	
	// checklists and their children need special treatment (children don't have id)
	for (var key in checklist_tooltips){
		console.log(key)
		try{
			tooltipped_object = document.getElementById(key);
			tooltip_text_array = checklist_tooltips[key]
			children = tooltipped_object.childNodes[0].childNodes[0].childNodes[0].childNodes
			var i = 0
			list = Array.from(children)
			list.forEach(function(node){
				if (i < additional_filter_tooltips.length){
					tooltip_position = getPosition(node);
					addTooltipText(node, tooltip_text_array[i], tooltip_position)
				}
				else{
					print("additional_tooltips array is not long enough")
				}
				i+=1

			})
			addTooltipTextChecklist(key, checklist_tooltips[key])
		}
		catch(err){
			console.log("Node "+ key + " is not found in the layout, no tooltip is attached. (addTooltips)")
		}
	}

	for (var key in class_tooltips) {
		// the object that should have a tooltip
		try{
			tooltipped_object = document.getElementsByClassName(key)[0];
			console.log(tooltipped_object)
			// check whether the tooltip should be on the right or left side, to prevent it from going out of the window
			tooltip_position = getPosition(tooltipped_object)
			
			addTooltipText(tooltipped_object, tooltipobj[key], tooltip_position)
		}
		catch(err){
			console.log("Node "+ key + " is not found in the layout, no tooltip is attached. (addTooltips)")
		}
	}
	

}

function getPosition(tooltipped_object){
	body_rect = document.body.getBoundingClientRect();
	element_rect = tooltipped_object.getBoundingClientRect();
	left_offset = element_rect.left - body_rect.left;
	right_offset = body_rect.right - element_rect.right;
	tooltip_position = "right";
	if (left_offset > right_offset){
		tooltip_position = "left";
	}
	return tooltip_position
}

function addTooltipText(node, text, tooltip_position){	
		var element = document.createElement('span');
		element.className = 'tooltiptext';
		if (tooltip_position == "left"){
			element.className = "tooltiptextleft";
		}
		element.innerHTML =  text;
		if (node.classList){
			node.classList.add("tooltipped");
		}
		else{
			node.className = "tooltipped"
		}
		node.appendChild(element);
}


// in chrome the console.log("Custom script.js is active") gets called twice

// todo: change to first page on filter change


//######################################################################################################
//##################################   Clienside Callbacks   ###########################################
//######################################################################################################
// Dash allows some callbacks to be executed client side for a smoother user experience
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        checkNewPulse: function(newpulse_shotno, modify) {
        	// return value does not matter
        	// it is not straightforward to conditionally trigger a dash update from javascript, aparently clicking a button works
        	// datawindow listens to dummy_button n_clicks, so clicking this button triggers 
        	if (modify == true){
        		dummy_button = document.getElementById("dummy_button")
        		dummy_button.click()
        		return [0]
        	}
        	return [0]
        	
        }
    }
});
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside2: {
        updatePersonalFilterOptions: function(new_filter, personal_filter_dropdown_options) {
        	exists = false
        	// The callback is fired on startup, so if new_filter is not yet made, just return
        	if (typeof new_filter !=='undefined'){
        		if (Number.isNaN(new_filter)){// don't add NaN to the list
        			return personal_filter_dropdown_options
        		}
	        		
	        	for (var i = 0; i< personal_filter_dropdown_options.length; i++){
	        		if (personal_filter_dropdown_options[i]["value"] == new_filter){
	        			exists = true
	        		}
	        	}
	        	if (exists == false){
	        		personal_filter_dropdown_options.push({"label":new_filter,"value":new_filter})
	        	}
	        	//Sort ascending, based on the numeric label
	        	personal_filter_dropdown_options.sort(function(a,b){
	        		if (a["label"] > b["label"]){
	        			return 1
	        		}
	        		else{
	        			return -1
	        		}
	        	})


	        	return personal_filter_dropdown_options
	        }
	        else{
	        	return personal_filter_dropdown_options
        	}
        }
}});


window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside3: {
        openElementWithId: function(n, is_open,id){ // multiple buttons can trigger this function, the information is unnecessary but the parameters are required
        	//updateTooltips(id);
            if(n){
               return !is_open ;
           }
            return is_open;
        }
    }

});
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside4: {
        openElementWithId2: function(n,n2, is_open,id){ // multiple buttons can trigger this function, the information is unnecessary but the parameters are required
        	//updateTooltips(id);
            if(n){
               return !is_open ;
           }
            return is_open;
        }
    }

});