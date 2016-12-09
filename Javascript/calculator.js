/*
	TODO:
	- Define onclick functions for miscButtons, operators and memoryButtons
	- Make sure outputWindow works as intended (e.g no numbers outside the calculator at any time)
*/

window.onload = function(){
	// get element with id "calculator" from html file and define container
	var container = document.getElementById("calculator");
	var div = document.createElement("div");
	
	// set container properties
	div.style.width="250px";
	div.style.height="308px";
	div.style.backgroundColor="black";
	div.align = "center";
	div.position = "relative";
	
	// define shortcuts for functions from Math
	sqrt = Math.sqrt
	
	// define variables that need to be defined before a button is pressed
	operatorPressed = 0;
	
	// output will be shown in this variable
	var outputWindow = document.createElement("div");
	outputWindow.style.width = "246px";
	outputWindow.style.height = "63px";
	outputWindow.style.marginBottom = "0px";
	outputWindow.style.backgroundColor = "#EDEDED";
	outputWindow.style.border = "2px solid black";
	
	
	// displays current calculation in upper right corner (e.g the Windows calculator)
	outputCalculation = document.createElement("p");
	outputCalculation.style.fontSize = "10px";
	outputCalculation.style.textAlign = "right";
	outputCalculation.style.color = "#a0a0a0";
	outputCalculation.innerHTML +="hello world";
	
	// displays numbers that are input as well as the result of the calculation 
	// after the equals button is pushed
	outputText = document.createElement("p");
	outputText.style.verticalAlign = "middle";
	outputText.style.fontSize = "25px";
	outputText.style.textAlign = "right";
	outputText.style.fontWeight = "bold";
	outputText.style.fontFamily = "default";
	outputText.style.lineHeight = "0px";
	outputText.innerHTML += "0";
	
	// add to the outputWindow container
	outputWindow.appendChild(outputCalculation);
	outputWindow.appendChild(outputText);
	
	// define digit buttons, set properties and append to div (will be changed later)
	var digitButtons = [];
	for (i=0;i<=9;i++){ 
		digitButtons[i] = document.createElement("button");
		if (i==0){
			digitButtons[i].style.width = "100px";
		}
		else{
			digitButtons[i].style.width = "50px";
		}
		digitButtons[i].style.height = "40px"
		digitButtons[i].appendChild(document.createTextNode(i));
		digitButtons[i].position = "absolute";
		digitButtons[i].onclick = (function(i){           //uses "closures" so that "i"
			return function(){			  //can be passed to OnDigitClicks
				OnDigitClicks(i);		  //(otherwise, the function would
			}					  //immediately on page load and would
		})(i);						  //not respond to button clicks
	
	}
		
	// define operators
	var operators = {};
	var signs = ["+","-","*","/","=",];
	operators["plus"] = document.createElement("button");
	operators["minus"] = document.createElement("button");
	operators["multiply"] = document.createElement("button");
	operators["divide"] = document.createElement("button");
	operators["equals"] = document.createElement("button");
	i = 0	// used to assign signs to operators in the for loop below
	for (var key in operators){
		operators[key].style.width = "50px";
		operators[key].style.height = "40px";
		operators[key].appendChild(document.createTextNode(signs[i]));
		operators[key].position = "absolute";
		i += 1;
	}
	
	// define buttons that are not operators or digits
	var miscButtons = {};
	var miscButtonSigns = ["C","CE","←","±","%",".","√","x²","xʸ"];
	var onMiscClicks = [];
	miscButtons["clear"] = document.createElement("button");
	miscButtons["clearEntry"] = document.createElement("button");
	miscButtons["backspace"] = document.createElement("button");
	miscButtons["changeSign"] = document.createElement("button");
	miscButtons["percentage"] = document.createElement("button");
	miscButtons["decimalPoint"] = document.createElement("button");
	miscButtons["sqrt"] = document.createElement("button");
	miscButtons["pow2"] = document.createElement("button");
	miscButtons["powY"] = document.createElement("button");
	
	i = 0 // assign sign to button in the loop below
	for (var key in miscButtons){
		miscButtons[key].style.width = "50px";
		miscButtons[key].style.height = "40px";
		miscButtons[key].appendChild(document.createTextNode(miscButtonSigns[i]));
		miscButtons[key].position = "absolute";
		i++;
	}
	
	//temporary
	miscButtons["clear"].onclick = Clear;
	

	

	
	// define MS, MC, MR, M+ and M- 
	var memoryButtons = {};
	memoryText = ["MS","MC","MR","M+","M-"];
	memoryButtons["store"] = document.createElement("button");
	memoryButtons["clear"] = document.createElement("button");
	memoryButtons["recall"] = document.createElement("button");
	memoryButtons["plus"] = document.createElement("button");
	memoryButtons["minus"] = document.createElement("button");
	i = 0	// used to assign labels to memory buttons in the for loop below
	for (var key in memoryButtons){
		memoryButtons[key].style.width = "50px";
		memoryButtons[key].style.height = "40px";
		memoryButtons[key].appendChild(document.createTextNode(memoryText[i]));
		memoryButtons[key].position = "absolute";
		i += 1;
	}
	
	
	
						
	// push the elements in order (outputWindow, memory buttons, digits 9-7, div operator, etc)
	var elements = [outputWindow,
		memoryButtons["clear"],memoryButtons["recall"],memoryButtons["store"],memoryButtons["plus"],memoryButtons["minus"],
		miscButtons["backspace"],miscButtons["clearEntry"],miscButtons["clear"],miscButtons["changeSign"], miscButtons["percentage"],
		digitButtons["7"],digitButtons["8"],digitButtons["9"],operators["divide"],miscButtons["sqrt"],
		digitButtons["4"],digitButtons["5"],digitButtons["6"],operators["multiply"],miscButtons["pow2"],
		digitButtons["1"],digitButtons["2"],digitButtons["3"],operators["minus"],miscButtons["powY"],
		digitButtons["0"],miscButtons["decimalPoint"],operators["plus"],operators["equals"]];
	
	
	// add functionality to buttons in digitButtons
	/*
		Rules for digits (some may not apply for 0):
		- A number will not be appended if there are more than 10 characters in outputWindow
		  (this is to allow space for "-",".","pow(x,y)","e+xyz" and sqrt() as outputWindow can not contain more
		  than 18 characters without "overflowing", i.e. numbers are displayed outside the area given to outputText
		- If 0 is the only number in outputText, it will be replaced by buttonNumber
		- If an operator was pressed previously (e.g +), outputText will be cleared and buttonNumber will be appended
	*/
	function OnDigitClicks(buttonNumber){
		if (buttonNumber == 0 && outputText.innerHTML.length == 1 && outputText.innerHTML == "0"); // do nothing
		else if ((outputText.innerHTML.length !== 1 || 
				(outputText.innerHTML.length == 1 && outputText.innerHTML !== "0")) &&
				outputText.innerHTML.length <= 10 && operatorPressed == 0) {
				outputText.innerHTML += buttonNumber.toString();
		}
		else if (outputText.innerHTML.length > 10); //do nothing; prevent else clause from running
		else {
			outputText.innerHTML = buttonNumber.toString();
			operatorPressed = 0;
		}
	}
	
	//temporary
	function Clear(){
		outputText.innerHTML = "0";
	}
	


	
	for (var buttonIndex in elements){
		div.appendChild(elements[buttonIndex]); // add elements to div
	}
	
	container.appendChild(div); // add div to container
}
