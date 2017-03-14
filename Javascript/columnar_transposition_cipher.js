// encryption wrong; fix. (look at rumkin)

function runCTC(){ // create visual elements
	// get element with id "columnarTranspositionCipher" from html file and define container
	var container = document.getElementById("columnarTranspositionCipher");
	var div = document.createElement("div");

	var leftDiv = document.createElement("div"); // hold input + output
	var rightDiv = document.createElement("div"); // visualise (en/de)cryption process

	container.position = "relative";

	leftDiv.style.width = "50%";
	rightDiv.style.width = "50%";
	leftDiv.style.float = "left";
	rightDiv.style.float = "right";
	rightDiv.align = "right";

	// set container properties
	div.style.height="500px";
	div.align = "left";

	// left div
	var inputForm = document.createElement("form");
	inputForm.style.width = "30%";
	inputForm.align = "center";
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
	var outputTextBox= document.createElement("textarea");

	encryptOrDecryptList.id = "encryptOrDecrypt";
	textInput.style.width="100%";
	textInput.style.resize="vertical";
	textInput.id = "textInput";
	textInput.type = "text";
	textInput.placeholder = "Input text here";
	encryptDecryptButton.innerHTML = "Go!";
	encryptDecryptButton.onclick = main;
	key.id = "key";
	key.placeholder = "Comma-separated numbers, e.g '4,3,1,5,2'";
	key.style.width = "89%";
	keyText.innerHTML = "Key:";
	keyText.style.width = "35px";
	keyText.style.margin = "0px";
	keyText.style.float = "left";
	outputTextBox.style.width = "100%";
	outputTextBox.style.resize="vertical";
	outputTextBox.readOnly = "true";
	outputTextBox.id = "outputBox";
	outputTextBox.placeholder = "Encrypted/Decrypted text will appear here";
	
	inputForm.appendChild(encryptOrDecryptList);

	// right div
	var table = document.createElement("table");
	var tableHeader = document.createElement("tr");
	var unencodedHeader = document.createElement("td");
	var rearrangedHeader = document.createElement("td");
	var outputRow = document.createElement("tr");
	var unencodedColumns = document.createElement("td");
	var rearrangedColumns = document.createElement("td");

	table.style.border = "2px solid black";
	table.style.tableLayout = "fixed";
	unencodedHeader.innerHTML = "Unencoded";
	rearrangedHeader.innerHTML = "Rearranged";
	unencodedColumns.id = "unEncOutput";
	rearrangedColumns.id = "rearrOutput";

	// tcs = [t]able [c]ell[s]
	tcs = [unencodedHeader, rearrangedHeader, unencodedColumns, rearrangedColumns];
	for (i=0;i<tcs.length;i++){
	tcs[i].style.border = "1px solid";
	tcs[i].style.textAlign = "center";
	tcs[i].style.wordWrap = "break-word";
	}
	unencodedColumns.width = "50%";
	rearrangedColumns.width = "50%";

	tableHeader.appendChild(unencodedHeader);
	tableHeader.appendChild(rearrangedHeader);
	outputRow.appendChild(unencodedColumns);
	outputRow.appendChild(rearrangedColumns);
	table.appendChild(tableHeader);
	table.appendChild(outputRow);

	leftDiv.appendChild(inputForm);
	leftDiv.appendChild(keyText);
	leftDiv.appendChild(key);
	leftDiv.appendChild(textInput);
	leftDiv.appendChild(encryptDecryptButton);
	leftDiv.appendChild(outputTextBox);
	rightDiv.appendChild(table);
	div.appendChild(leftDiv);
	div.appendChild(rightDiv);
	container.appendChild(div);
}


function main(){
	key = document.getElementById("key");
	choice = document.getElementById("encryptOrDecrypt");
	columns = key.value.split(",");
	text = document.getElementById("textInput").value;
	
	if(choice.value == "Encrypt"){
		encrypt()
	}
	else{ // choice.value == "Decrypt"
		decrypt()
	}
}

function encrypt(){
	var rows = textToRows(text);
	indexOrder = findIndexOrder(columns,"Encrypt"); // [indexOrder,columnsSorted]

	displayText("Unencoded","Encrypt",rows);
	displayText("Rearranged","Encrypt",rows); // also creates displayedRows
	var cipherText = createCipherText(displayedRows);
	
	document.getElementById("outputBox").innerHTML = cipherText;
}

function decrypt(){ 
	var rows = textToColumns(text);
	indexOrder = findIndexOrder(columns,"Decrypt"); // [indexOrder,columnsSorted]

	displayText("Unencoded","Decrypt",rows);
	displayText("Rearranged","Decrypt",rows);
	var plainText = createPlainText(displayedRows);
	
	document.getElementById("outputBox").innerHTML = plainText;
}

function textToRows(text){
	var outputArray = [];
	var newRow = true;
	var currentRowIndex = 0;
	for(i=0;i<text.length;i++){
		if((i-(currentRowIndex*columns.length)) % columns.length == 0){
			newRow = true;
		}
		if(newRow){
			outputArray.push([]);
			currentRowIndex = outputArray.length-1;
		}
		outputArray[currentRowIndex].push(text[i]);
		newRow = false;
	}
	return outputArray
}

function textToColumns(text){
	var outputArray = [];
	for(i=0;i<parseInt(text.length/columns.length);i++){ //create rows
		outputArray[i] = [];
	}
	i = 0; // row count
	j = 0; // col count
	for(currentTextIndex=0;currentTextIndex<text.length;currentTextIndex++){
		outputArray[i][j] = text[currentTextIndex];
		i++;
		if(i==outputArray.length){ // new col
			i=0;
			j++;
		}
	}
	return outputArray;
}

function findIndexOrder(columns,mode){// bubble sort
	if (mode=="Encrypt"){
		columnsSorted = columns.slice(0); // create a copy of column
		for(loopCount=0;loopCount<columnsSorted.length;loopCount++){
			for(i=columnsSorted.length-1;i>0;i--){
				if(parseInt(columnsSorted[i])<parseInt(columnsSorted[i-1])){ 
														 // switch places as appropriate; 
														 // e.g [5,3] returns [3,5], but
					temp = columnsSorted[i];             // not vice versa
					columnsSorted[i] = columnsSorted[i-1];
					columnsSorted[i-1] = temp;
				}
			}
		}
		indexOrder = []; // shows the order columnsSorted should be accessed,
						 // e.g if key = (3,4,2,1), indexOrder = (3,2,0,1)
		for(sortedIndex=0;sortedIndex<columnsSorted.length;sortedIndex++){
			for(originalIndex=0;originalIndex<columns.length;originalIndex++){
				if(columnsSorted[sortedIndex] == columns[originalIndex]){
					indexOrder.push(originalIndex);
				} 
			}
		}
	}
	else if(mode=="Decrypt"){
		columnsSorted = [];
		indexOrder = []; // shows the order columnsSorted should be accessed
						 // (2,5,1,4,3) -> (1,2,3,4,5) => indexOrder = (1,4,0,3,2)
		for(i=0;i<columns.length;i++){columnsSorted[i] = i;}
		for(originalIndex=0;originalIndex<columns.length;originalIndex++){
			for(sortedIndex=0;sortedIndex<columnsSorted.length;sortedIndex++){
				if(columns[originalIndex]-1 == columnsSorted[sortedIndex]){
					indexOrder.push(sortedIndex);
				}
			}
		}
	}
	return [indexOrder,columnsSorted];
}

function createCipherText(displayedRows){
	cipherText = ""
	for(i=0;i<columns.length;i++){
		for(j=0;j<displayedRows.length;j++){
			if(!(displayedRows[j][i] == undefined)){
				cipherText += displayedRows[j][i];
			}
		}
	}
	return cipherText
}

function createPlainText(displayedRows){
	plainText = "";
	for(i=0;i<displayedRows.length;i++){
		for(j=0;j<columns.length;j++){
			plainText += displayedRows[i][j];
		}
	}
	return plainText
}

function displayText(type,mode,rows){
	var partOfTable = ""; // shows where the text should go
	displayedRows = []; // global copy of output, same format as rows
	if (type == "Unencoded"){
		partOfTable = document.getElementById("unEncOutput");
		if(mode == "Encrypt"){
			var initialOrder = [];
			for(i=0;i<columns.length;i++){initialOrder[i] = i;}
			key = [initialOrder,columns];	
		} else if(mode == "Decrypt"){
			var initialOrder = [];
			var orderedKey = [];
			for(i=0;i<columns.length;i++){
				initialOrder[i] = i;
				orderedKey[i] = i+1;
				}
			key = [initialOrder,orderedKey];	
		}
	}
	else if (type == "Rearranged"){ 
		partOfTable = document.getElementById("rearrOutput");
		if(mode == "Encrypt"){
			key = indexOrder; // [indexOrder,rearrangedColumns];
		} else if(mode == "Decrypt"){
			key = indexOrder;
			key[1] = columns;
		}
	}
	
	while(partOfTable.firstChild){ // clear content
		partOfTable.removeChild(partOfTable.firstChild);
	}
	
	var newRow = document.createElement("tr");
	for(i=0;i<key[0].length;i++){ // shows order of columns (e.g 3 2 4 1)
		var newRowData = document.createElement("td");
		newRowData.innerHTML = key[1][i];
		newRow.appendChild(newRowData);
	}
	partOfTable.appendChild(newRow);
	for(j=0;j<rows.length;j++){ // show input message   	
		var newRow = document.createElement("tr");
		displayedRows[j] = [];
		for(i=0;i<key[0].length;i++){
			var newRowData = document.createElement("td");
			if(!(rows[j][key[0][i]] == undefined)){
				newRowData.innerHTML = rows[j][key[0][i]];
				displayedRows[j][i] = rows[j][key[0][i]];
			}
			else{
				newRowData.innerHTML = " ";
				displayedRows[j][i] = " ";
			}
			newRow.appendChild(newRowData);
		}
		partOfTable.appendChild(newRow);
	}
}
