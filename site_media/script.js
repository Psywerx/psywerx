jQuery(document).ready(function(){
	
	
	function relativeShadow(element, color){
		
		
		
		middle = function(el){
			m = new Object();
			m.top = el.offset().top + el.height()/2;
			m.left = el.offset().left +  el.width()/2;	   
   
			return m 
		};
		normalize = function(diff){
			LIMIT = 3;
			d = -diff/200;
			if (d > LIMIT) d = LIMIT;
			if (d < -LIMIT) d = -LIMIT;
			
			return d;			
		}
		
		$(document).mousemove(function(e){
			   
			var p = middle(element);
			diff = new Object();
			diff.top = e.pageY - p.top;
			diff.left = e.pageX - p.left;
		
		  
			element.css('text-shadow', normalize(diff.left) + "px " + normalize(diff.top) +"px 0px " + color);
		  
		 //$('h1').html(e.pageX +', '+ e.pageY + ' ' + diff.top + ' ' + diff.left);
		 }); 
		
		
	} 

	r1 = new relativeShadow($("#header-h"), 'black');
	
   
   

});