window.onload = function(){
	var body = document.getElementsByTagName("body");
	var div = document.createElement("div");
	
	var outputWindow = document.createElement("p");
	
	var button0 = document.createElement("button");
	var button1 = document.createElement("button");
	var button2 = document.createElement("button");
	var button3 = document.createElement("button");
	var button4 = document.createElement("button");
	var button5 = document.createElement("button");
	var button6 = document.createElement("button");
	var button7 = document.createElement("button");
	var button8 = document.createElement("button");
	var button9 = document.createElement("button");
	
	var plusOperator = document.createElement("button");
	var minusOperator = document.createElement("button");
	var mulitplyOperator = document.createElement("button");
	var divideOperator = document.createElement("button");
	var equalsOperator = document.createElement("button");
	

	var digitButtons =[button0,button1,button2,button3,
						button4,button5,button6,button7,
						button8,button9];
	
	var operators = [plusOperator,minusOperator,mulitplyOperator,divideOperator];
						
	// push the elements in order (outputwindow, clear+memory buttons, digits 9-7, div operator, etc)
	var elements = [];
	//var myElements = document.querySelectorAll(".bar");
	
	div.style.width="250px";
	div.style.height="280px";
	div.style.backgroundColor="black";
	
	div.align = "center";
	div.position = "relative";
	
	rect = button1.getBoundingClientRect();
	
	
	
	for (i=0;i<=9;i++){
		if (i==0){
			digitButtons[i].style.width = "100px";
		}
		else{
			digitButtons[i].style.width = "50px";
		}
		digitButtons[i].style.height = "40px"
		digitButtons[i].appendChild(document.createTextNode(i));
		digitButtons[i].position = "absolute";
	
		div.appendChild(digitButtons[i]);
	}
	
	
	
	body[0].appendChild(div);
}