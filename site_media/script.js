jQuery(document).ready(function(){
	
	
	function relativeShadow(element, color, shadow){
		
		
		
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
		  
			element.css(shadow, normalize(diff.left) + "px " + normalize(diff.top) +"px 2px "  + color);
		  
		 //$('h1').html(e.pageX +', '+ e.pageY + ' ' + diff.top + ' ' + diff.left);
		 }); 
		
		
	} 

	r1 = new relativeShadow($("#header-h"), 'black', 'text-shadow');

	
	function rotate(element, deg){
		$(element).transform({rotate: deg});
		$(element).hover(function(){
			
			$(element).animate({rotate: '0deg'}, "fast", "swing");
		}, function(){
			
			$(element).animate({rotate: deg}, "fast", "swing");
		});
	}
	rotate("#projects", '1deg');
	rotate("#team", '-1deg');
	
		
   
   

});