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
	
	// output during calculations will be shown using this variable
	var outputWindow = document.createElement("div");
	outputWindow.style.width = "246px";
	outputWindow.style.height = "63px";
	outputWindow.style.marginBottom = "0px";
	outputWindow.style.backgroundColor = "#EDEDED";
	outputWindow.style.border = "2px solid black";
	
	// define C, CE, backspace (right arrow), changeSign
	// define backspace, changeSign
	var miscButtons = {};
	var miscButtonSigns = ["C","CE","←","±","%",".","√","x²","xʸ"];
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
	
	//var myElements = document.querySelectorAll(".bar");
	for (var buttonIndex in elements){
		div.appendChild(elements[buttonIndex]);
	}
	
	
	
	
	container.appendChild(div);
}
