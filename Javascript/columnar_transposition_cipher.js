function runCTC(){
	// get element with id "columnarTranspositionCipher" from html file and define container
	var container = document.getElementById("columnarTranspositionCipher");
	var div = document.createElement("div");
	
	var leftDiv = document.createElement("div"); // hold input
	var rightDiv = document.createElement("div"); // hold output
	
	container.style.position = "absolute";
	container.style.width = "780px";

	leftDiv.style.width = "38%";
	rightDiv.style.width = "60%";
	leftDiv.style.float = "left";
	rightDiv.style.float = "right";
	leftDiv.style.border = "2px dashed red";
	rightDiv.style.border = "2px dotted blue";
	
	// set container properties
	div.style.height="500px";
	div.align = "left";
	div.position = "relative";
	div.style.border = "2px solid black";
	
	// create drop-down list
	var inputForm = document.createElement("form");
	inputForm.style.width = "30%";
	inputForm.align = "center";
	inputForm.style.border = "2px dashed green";
	var encryptOrDecryptList = document.createElement("select");
	var encryptOrDecryptOptions = [document.createElement("option"),
								   document.createElement("option")];
								   
	var encryptOrDecryptValues = ["Encrypt", "Decrypt"]
	for (i=0;i<2;i++){
		encryptOrDecryptOptions[i].value = encryptOrDecryptValues[i];
		encryptOrDecryptOptions[i].innerHTML = encryptOrDecryptValues[i];
		encryptOrDecryptList.appendChild(encryptOrDecryptOptions[i]);
	}
	
	var key = document.createElement("input");
	var keyText = document.createElement("p");
	var textInput = document.createElement("textarea");
	var encryptDecryptButton = document.createElement("button");
	
	
	encryptOrDecryptList.id = "encryptOrDecrypt";
	textInput.style.width="100%";
	textInput.style.resize="vertical";
	textInput.id = "textInput";
	textInput.type = "text";
	encryptDecryptButton.innerHTML = "Go!"
	encryptDecryptButton.onclick = main;
	key.id = "key";
	keyText.innerHTML = "Key:"
	keyText.style.width = "15%";
	keyText.style.margin = "0px";
	keyText.style.float = "left";
	
	inputForm.appendChild(encryptOrDecryptList);
	
	
	
	// right div
	var table = document.createElement("table");
	var tableHeader = document.createElement("tr");
	var plainTextHeader = document.createElement("td");
	var cipherTextHeader = document.createElement("td");
	var outputRow = document.createElement("tr");
	var plainTextOutput = document.createElement("td");
	var cipherTextOutput = document.createElement("td");
	
	table.style.border = "2px solid black";
	table.style.tableLayout = "fixed";
	plainTextHeader.innerHTML = "Plaintext";
	cipherTextHeader.innerHTML = "Ciphertext";
	plainTextOutput.id = "ptOutput";
	cipherTextOutput.id = "ctOutput";
	
	tds = [plainTextHeader, cipherTextHeader, plainTextOutput, cipherTextOutput];
	for (i=0;i<tds.length;i++){
		tds[i].style.border = "1px solid";
		tds[i].style.textAlign = "center";
		tds[i].style.wordWrap = "break-word";
	}
	plainTextOutput.width = "50%";
	cipherTextOutput.width = "50%";

	tableHeader.appendChild(plainTextHeader);
	tableHeader.appendChild(cipherTextHeader);
	outputRow.appendChild(plainTextOutput);
	outputRow.appendChild(cipherTextOutput);
	table.appendChild(tableHeader);
	table.appendChild(outputRow);
	
	leftDiv.appendChild(inputForm);
	leftDiv.appendChild(keyText);
	leftDiv.appendChild(key);
	leftDiv.appendChild(textInput);
	leftDiv.appendChild(encryptDecryptButton);
	rightDiv.appendChild(table);
	div.appendChild(leftDiv);
	div.appendChild(rightDiv);
	container.appendChild(div);

	/* retrieve value from list example
	var e = document.getElementById("ddlViewBy");
	var strUser = e.options[e.selectedIndex].value;
	*/
}

function main(){
	key = document.getElementById("key");
	choice = document.getElementById("encryptOrDecrypt");
	console.log(key.value);
	console.log(choice.value);
	
	displayPlainText();
	displayCipherText();
}

function displayPlainText(){
	var columns = key.value.split(",");
	var text = document.getElementById("textInput").value;
	var rows = [];
	
	var table = document.createElement("table");
	var firstRow = document.createElement("tr");
	for(i=0;i<columns.length;i++){
		newCell = document.createElement("td");
		newCell.innerHTML = columns[i];
		firstRow.appendChild(newCell);
	}
	table.appendChild(firstRow);
	
	var newRow = true // initial value
	var j = -1; // initial value 
	for(i=0;i<text.length;i++){
		if(i%columns.length == 0){
			newRow = true;
		}
		if(newRow){
			rows.push(document.createElement("tr"));
			j += 1;
		}
		newCell = document.createElement("td");
		newCell.innerHTML = text[i];
		rows[j].appendChild(newCell);
		newRow = false;
	}

	for (i=0;i<rows.length;i++){
		table.appendChild(rows[i]);
	}
	
	var pt = document.getElementById("ptOutput");
	while(pt.firstChild){
		pt.removeChild(pt.firstChild);
	}
	pt.appendChild(table);
}

function displayCipherText(){
	
}