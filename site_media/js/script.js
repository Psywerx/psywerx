//Konami plugin:

(function($) {

	$.fn.konami = function(callback, code) {
		if(code == undefined) code = "38,38,40,40,37,39,37,39,66,65";
		
		return this.each(function() {
			var kkeys = [];
			$(this).keydown(function(e){
				kkeys.push( e.keyCode );
				if ( kkeys.toString().indexOf( code ) >= 0 ){
					$(this).unbind('keydown', arguments.callee);
					callback(e);
				}
			}, true);
		});
	}

})(jQuery);

jQuery(document).ready(function(){


    $(window).konami(function(){ self.location = '/admin' });
	
	
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

	//annoying if the box is large:
	//dependency: jquery.transform-0.9.3.min.js
	function rotate(element, deg){
		$(element).transform({rotate: deg});
		$(element).hover(function(){
			
			//$(element).animate({rotate: '0deg'}, {duration: "fast", queue : false, easing : "swing"});
		}, function(){
			
			//$(element).animate({rotate: deg}, {duration: "fast", queue : false, easing : "swing"});
		});
	}
	//rotate("#projects", '1deg');
	
	
	function setShadow(element){
		
		$(element).hover(function(){
			
			$(element).animate({boxShadow: '0 0 8px #AAA'}, {duration: "fast", queue : false, easing : "swing"});
		}, function(){
			
			$(element).animate({boxShadow: '0 0 0px #AAA'}, {duration: "fast", queue : false, easing : "swing"});
		});		
	}
	setShadow("#projects");
	setShadow("#team");
   
   

});
