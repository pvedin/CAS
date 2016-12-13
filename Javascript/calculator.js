/*
	TODO:
	- Define onclick functions for miscButtons and memoryButtons
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
	sqrt = Math.sqrt;
	pow = Math.pow;
	
	// define variables that need to be defined before a button is pressed
	allowNumInput = 1;
	operatorPressed = 0;
	memory = 0;
	
	// output will be shown in this variable
	var outputWindow = document.createElement("div");
	outputWindow.style.width = "246px";
	outputWindow.style.height = "63px";
	outputWindow.style.marginBottom = "0px";
	outputWindow.style.backgroundColor = "#EDEDED";
	outputWindow.style.border = "2px solid black";
	outputWindow.style.position = "relative";
	
	
	
	// displays current calculation in upper right corner (e.g the Windows calculator)
	outputCalculation = document.createElement("p");
	outputCalculation.style.fontSize = "10px";
	outputCalculation.style.textAlign = "right";
	outputCalculation.style.color = "#a0a0a0";
	outputCalculation.style.top = "0";
	outputCalculation.style.right = "0";
	outputCalculation.style.position = "absolute";
	outputCalculation.innerHTML = "";
	outputCalculation.scale = 1;
	
	// displays numbers that are input as well as the result of the calculation 
	// after the equals button is pushed
	outputText = document.createElement("p");
	outputText.style.verticalAlign = "middle";
	outputText.style.fontSize = "25px";
	outputText.style.textAlign = "right";
	outputText.style.fontWeight = "bold";
	outputText.style.fontFamily = "default";
	outputText.style.lineHeight = "0px";
	outputText.style.bottom = "0";
	outputText.style.right = "0";
	outputText.style.position = "absolute";
	outputText.innerHTML += "0";
	outputText.scale = 1;
	
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
			return function(){							  //can be passed to OnDigitClicks
				OnDigitClicks(i);						  //(otherwise, the function would
			}											  //immediately on page load and would
		})(i);											  //not respond to button clicks
	
	}
		
	// define operators
	var operators = {};
	var signs = ["+","-","*","/"];
	operators["plus"] = document.createElement("button");
	operators["minus"] = document.createElement("button");
	operators["multiply"] = document.createElement("button");
	operators["divide"] = document.createElement("button");
	i = 0	// used to assign signs to operators in the for loop below
	for (var key in operators){
		operators[key].style.width = "50px";
		operators[key].style.height = "40px";
		operators[key].appendChild(document.createTextNode(signs[i]));
		operators[key].position = "absolute";
		operators[key].onclick = (function(key){          
			return function(){	
				OnOperatorClicks(key);					
			}											  
		})(key);	
		i += 1;
	}
	
	// define buttons that are not operators or digits
	var miscButtons = {};
	var miscButtonSigns = ["C","CE","←","±","%",".","√","x²","xʸ","="];
	var onMiscClicks = {"clear": OnClearClick,
						"clearEntry": OnClearEntryClick,
						"backspace": OnBackspaceClick,
						"changeSign": OnChangeSignClick,
						"percentage": OnPercentageClick,
						"decimalPoint": OnDecimalPointClick,
						"sqrt": OnSqrtClick,
						"pow2": OnPow2Click,
						"powY": OnPowYClick,
						"equals": OnEqualsClick};
	miscButtons["clear"] = document.createElement("button");
	miscButtons["clearEntry"] = document.createElement("button");
	miscButtons["backspace"] = document.createElement("button");
	miscButtons["changeSign"] = document.createElement("button");
	miscButtons["percentage"] = document.createElement("button");
	miscButtons["decimalPoint"] = document.createElement("button");
	miscButtons["sqrt"] = document.createElement("button");
	miscButtons["pow2"] = document.createElement("button");
	miscButtons["powY"] = document.createElement("button");
	miscButtons["equals"] = document.createElement("button");
	
	
	i = 0 // assign sign to button in the loop below
	for (var key in miscButtons){
		miscButtons[key].style.width = "50px";
		miscButtons[key].style.height = "40px";
		miscButtons[key].appendChild(document.createTextNode(miscButtonSigns[i]));
		miscButtons[key].position = "absolute";
		miscButtons[key].onclick = (function(key){          
			return function(){	
				onMiscClicks[key](key);					
			}											  
		})(key);
		i++;
	}
	

	

	
	// define MS, MC, MR, M+ and M- 
	var memoryButtons = {};
	var onMemoryClicks = {"store": OnMStoreClick,
						"clear": OnMClearClick,
						"recall": OnMRecallClick,
						"plus": OnMPlusClick,
						"minus": OnMMinusClick};
	memoryText = ["MS","MC","MR","M+","M-"];
	memoryButtons["store"] = document.createElement("button");
	memoryButtons["clear"] = document.createElement("button");
	memoryButtons["recall"] = document.createElement("button");
	memoryButtons["plus"] = document.createElement("button");
	memoryButtons["minus"] = document.createElement("button");
	i = 0;  // used to assign labels to memory buttons in the for loop below
	for (var key in memoryButtons){
		memoryButtons[key].style.width = "50px";
		memoryButtons[key].style.height = "40px";
		memoryButtons[key].appendChild(document.createTextNode(memoryText[i]));
		memoryButtons[key].position = "absolute";
		memoryButtons[key].onclick = (function(key){          
			return function(){	
				onMemoryClicks[key](key);					
			}											  
		})(key);
		i += 1;
	}
	
	
	
						
	// push the elements in order (outputWindow, memory buttons, digits 9-7, div operator, etc)
	var elements = [outputWindow,
		memoryButtons["clear"],memoryButtons["recall"],memoryButtons["store"],memoryButtons["plus"],memoryButtons["minus"],
		miscButtons["backspace"],miscButtons["clearEntry"],miscButtons["clear"],miscButtons["changeSign"], miscButtons["percentage"],
		digitButtons["7"],digitButtons["8"],digitButtons["9"],operators["divide"],miscButtons["sqrt"],
		digitButtons["4"],digitButtons["5"],digitButtons["6"],operators["multiply"],miscButtons["pow2"],
		digitButtons["1"],digitButtons["2"],digitButtons["3"],operators["minus"],miscButtons["powY"],
		digitButtons["0"],miscButtons["decimalPoint"],operators["plus"],miscButtons["equals"]];
	
	
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
				outputText.innerHTML.length <= 10 && allowNumInput == 1) {
				outputText.innerHTML += buttonNumber.toString();
		}
		else if (outputText.innerHTML.length > 10); //do nothing; prevent else clause from running
		else {
			outputText.innerHTML = buttonNumber.toString();
			operatorPressed = 0;
		}
	}
	
	function OnOperatorClicks(sign){
		if (outputText.innerHTML !== "" && sign !== "minus" && operatorPressed == 0){
			operatorPressed = 1;
			allowNumInput = 1;
			outputCalculation.innerHTML += outputText.innerHTML + operators[sign].innerHTML;
			outputText.innerHTML = "0";
		}
		else if (sign == "minus" && operatorPressed == 0){
			if (outputText.innerHTML == ""){
				operatorPressed = 1;
				allowNumInput = 1;
				outputCalculation.innerHTML = "0" + operators[sign].innerHTML;
				outputText.innerHTML = "0";
			}
			else{
				operatorPressed = 1;
				allowNumInput = 1;
				outputCalculation.innerHTML += outputText.innerHTML + operators[sign].innerHTML;
				outputText.innerHTML = "0";
			}
		}
		
		
		
	}
	
	function OnClearClick(){
		outputText.innerHTML = "0";
		outputCalculation.innerHTML = "";
	}
	function OnClearEntryClick(){
		outputText.innerHTML = "0";
	}
	function OnBackspaceClick(){
		if (outputText.innerHTML !== "0"){
			outputText.innerHTML = outputText.innerHTML.slice(0,-1); //remove last character
			if (outputText.innerHTML == ""){
				outputText.innerHTML = "0";
			}
		}
	}
	function OnChangeSignClick(){
		if (outputText.innerHTML[0] != "-"){
			outputText.innerHTML = "-" + outputText.innerHTML;
		}
		else{
			outputText.innerHTML = outputText.innerHTML.substr(1); //remove first character
		}
	}
	function OnPercentageClick(){
		outputCalculation.innerHTML += (eval(outputCalculation.innerHTML.slice(0,-1)) *(parseFloat(outputText.innerHTML) / 1000)*10); 
		outputText.innerHTML = "0";
	}
	function OnDecimalPointClick(){
		if (!outputText.innerHTML.includes(".")){
			outputText.innerHTML += ".";
		}
	}
	function OnSqrtClick(){
		allowNumInput = 0;
		outputText.innerHTML = "sqrt(" + outputText.innerHTML + ")";
	}
	function OnPow2Click(){
		allowNumInput = 0;
		outputText.innerHTML = "pow(" + outputText.innerHTML + ",2)";
	}
	function OnPowYClick(){
		allowNumInput = 0;
		power = prompt("Enter value for y (x^y):");
		outputText.innerHTML = "pow(" + outputText.innerHTML + "," + power + ")";
	}
	function OnEqualsClick(){
		allowNumInput = 1;
		if (outputText.innerHTML !== "0"){
			outputCalculation.innerHTML += outputText.innerHTML;
		}
		result = eval(outputCalculation.innerHTML);
		if ((result.toString()).length <= 10){
			outputText.innerHTML = (result.toPrecision(result.length));
		}
		else{
			outputText.innerHTML = (result.toPrecision(10));
		}
		outputCalculation.innerHTML = "";
	}
	
	function OnMClearClick(){
		memory = 0;
	}
	function OnMRecallClick(){
		if (outputText.innerHTML == "0"){
			outputText.innerHTML = memory.toString();
		}
		else{
			outputText.innerHTML += memory.toString();
		}
	}
	function OnMStoreClick(){
		memory = parseFloat(outputText.innerHTML);
	}
	function OnMPlusClick(){
		memory += parseFloat(outputText.innerHTML);
	}
	function OnMMinusClick(){
		memory -= parseFloat(outputText.innerHTML);
	}
	
	
	//make sure text always fits into element (not implemented yet)
	function ScaleText(element,upOrDown){
		if (upOrDown == "up"){
			element.scale += 0.1;
			element.style.transform = "scale("+element.scale+",1)";
		}
		else if(upOrDown == "down"){
			element.scale -= 0.1;
			element.style.transform = "scale("+element.scale+",1)";
		}
	}

	
	for (var buttonIndex in elements){
		div.appendChild(elements[buttonIndex]); // add elements to div
	}
	
	container.appendChild(div); // add div to container
}
