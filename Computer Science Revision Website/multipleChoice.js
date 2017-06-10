// initialise canvas
canvas = document.createElement("canvas");
canvas.width = "300";
canvas.height = "420";
context = canvas.getContext("2d");
canvas.style.border = "2px solid black";
document.getElementById("div").appendChild(canvas);
mouseHold = false; // used for slider

function MultipleChoice(questions){
	this.questions = questions; // questions for all topics
	this.topics = ["1.1","1.2","2","3","4.1","4.2","4.3","5","6","7","D"];
	this.selectedTopics = [];
	this.selectedQuestions = []; // questions for selected topics; displayNextQuestion will choose one of these at random
	this.answeredQuestions = [];
	this.currentQuestion = 0;
	this.numberOfQuestions = 0;
	this.questionNumber = 0;
	this.correctAnswers = 0;
	this.selectedAnswer = "";
	this.currentScreen = 1; // 1 = first screen, 2 = question, 3 = question answer, 4 = results
	
	this.firstScreen = displayFirstScreen; // user selects topics
	this.filterQuestionsAndStart = filterQuestionsAndStart;
	this.nextQuestion = displayNextQuestion;
	this.checkAnswer = checkAnswer;
	this.displayResults = displayResults;
	this.reset = reset;
}

function Question(topics,questionPrompt,answerArray,promptCoords=[20,80]){
	this.topics = topics; // [topic1] or [topic1,topic2,...,topicn]
	this.questionPrompt = questionPrompt;
	this.answers = answerArray; // [a1,a2,a3,a4]
	this.correctAnswer = this.answers[0]; // make sure first answer in array is the correct one
	this.promptCoords = [20,80];
	this.topicCoords = [200,40];
	this.answerLayout = [] // e.g [a2,a4,a1,a3]
};

function TopicButton(x,y,topic){
	this.x = x;
	this.y = y;
	this.topic = topic;
	this.width = 10;
	this.height = 10;
	this.callback = onTopicButtonPress;
	this.activated = false;
}

function Button(x,y,width,height,callback, value=null){
	this.x = x;
	this.y = y;
	this.width = width;
	this.height = height;
	this.callback = callback;
	this.value = value;
}

function Slider(x,y,width,min,max,steps=1,barWidth=10,barHeight=20,lineWidth=2){
	this.realX = x; // of line
	this.x = x - 50; // for isButtonPressed() 
	this.realY = y // of line
	this.y = y-barHeight/2; // for isButtonPressed()
	this.realWidth = width;
	this.width = width + 50; // for isButtonPressed()
	this.height = barHeight; // for isButtonPressed()
	this.min = min;
	this.max = max;
	this.steps = steps;
	this.barWidth = barWidth;
	this.barHeight = barHeight;
	this.lineWidth = lineWidth;
	this.value=this.min; // will be calculated using steps*Math.round((min+(max-min)*((barX-x)/width))/steps)
	this.barX = this.realX; // initial value; assuming this.value = this.min
	this.mouseUpColor = "azure"; // affects bar color
	this.mouseDownColor = "dimgrey"; // affects bar color
}

function updateSlider(slider){
	if(mouseHold){
		requestAnimFrame(function(){updateSlider(slider)});
	}
	context.clearRect(slider.realX-slider.lineWidth-10,slider.realY-slider.barHeight/2-slider.lineWidth,
	                  slider.realWidth+slider.lineWidth+20,slider.barHeight+slider.lineWidth*2);
	context.clearRect(210,305,50,20);
	context.beginPath();
	context.moveTo(slider.realX,slider.realY);
	context.lineTo(slider.realX+slider.realWidth,slider.realY);
	context.linerealWidth = slider.linerealWidth;
	context.stroke();
	
	if(typeof mousePos !== 'undefined' && mousePos && isButtonPressed(slider)){
		if(mousePos.x>slider.realX+slider.realWidth-slider.barWidth/2){
			slider.barX = slider.realX + slider.realWidth - slider.barWidth/2-4;
		}
	    else if(mousePos.x<slider.realX){
			slider.barX = slider.realX - slider.barWidth/2+4;
		}
		else{slider.barX = mousePos.x-slider.barWidth/2;}
	}
	context.lineWidth = 1;
	context.rect(slider.barX,slider.realY-slider.barHeight/2,slider.barWidth,slider.barHeight);
	if(mouseHold){context.fillStyle=slider.mouseDownColor;}
	else{context.fillStyle=slider.mouseUpColor;}
	context.fill();
	context.stroke();
	context.font = "12pt Calibri";
	context.fillStyle = "black";
	slider.value = slider.steps*Math.round((slider.min+(slider.max-slider.min)
	                                   *((slider.barX-slider.realX+slider.barWidth/2)/slider.realWidth))/slider.steps);

	context.fillText(slider.value,220,325);
	
}

function displayFirstScreen(){ // display topic choices
	this.currentScreen = 1;
	context.clearRect(0,0,canvas.width,canvas.height);
	context.beginPath();
	context.font = "12pt Calibri";
	context.fillText("Select question topics:",canvas.width/5,20);
	context.fillText("SL/HL Core",100,40);
	context.fillText("HL extension",90,200);
	context.fillText("Options",80,280);
	context.fillText("HL?",150,280);
	context.fillText("Number of questions = ",60,325);
	context.strokeStyle = "black";
	context.stroke();
	context.closePath();
	context.beginPath();
	displayButton(topicButtons["D (HL)"]);
	for(i=0;i<this.topics.length;i++){
		context.font = "12pt Calibri";
		context.fillText(this.topics[i],topicButtons[this.topics[i]].x-30,
		                 topicButtons[this.topics[i]].y+topicButtons[this.topics[i]].height);
		displayButton(topicButtons[this.topics[i]]);
		var plural = "";
		if(findNumberOfQuestionsPerTopic(this.topics[i],this.questions) !== 1){
			plural += "s";
		}
		context.fillText("(" + findNumberOfQuestionsPerTopic(this.topics[i],this.questions) 
		                 +" question"+plural+" in this topic area)",topicButtons[this.topics[i]].x
						 +topicButtons[this.topics[i]].width+10,topicButtons[this.topics[i]].y
						 +topicButtons[this.topics[i]].height);
	}
	context.font = "bold 36pt Calibri";
	context.fillText("Start",generateQuestionsButton.x*2,generateQuestionsButton.y+
	                 generateQuestionsButton.height*0.8);
	updateSlider(numberOfQuestionsSlider);
	displayButton(generateQuestionsButton);
	context.lineWidth = 2;
	context.stroke();
	this.currentScreen = 1;
}

function filterQuestionsAndStart(){ // only include questions from selected topics
	this.selectedTopics = [];
	this.selectedQuestions = [];
	this.numberOfQuestions = numberOfQuestionsSlider.value;
	
	for(i=0;i<this.topics.length;i++){
		if(topicButtons[this.topics[i]].activated){
			this.selectedTopics.push(this.topics[i]);
		}
	}
	if(topicButtons["D (HL)"].activated && this.selectedTopics.indexOf("D") !== -1){
		this.selectedTopics.push("D (HL)");
	}
	
	for(i=0;i<this.questions.length;i++){
		for(j=0;j<this.questions[i].topics.length;j++){
			if(this.selectedTopics.indexOf(this.questions[i].topics[j]) !== -1){
				this.selectedQuestions.push(this.questions[i]);
				break; // next question
			}
		}
	}
	if(this.selectedQuestions.length !== 0){
		this.nextQuestion();
	}
	// else do nothing
}

function displayNextQuestion(){
	context.clearRect(0,0,canvas.width,canvas.height);
	this.currentScreen = 2;
	this.currentQuestion = Math.floor(Math.random()*this.selectedQuestions.length);
	
	if(this.questionNumber < this.numberOfQuestions){
		if(this.selectedQuestions.length !== 0){
			this.questionNumber += 1;
			context.beginPath();
			context.font = "24pt Calibri";
			context.fillStyle = "black";
			context.fillText("Question "+this.questionNumber,70,40);
			context.font = "10pt Calibri";
			if(this.selectedQuestions[this.currentQuestion].topics.length>1){
				context.fillText("Topics:",245,20);
				var topicsString = "";
				for(i=0;i<this.selectedQuestions[this.currentQuestion].topics.length;i++){
					topicsString += this.selectedQuestions[this.currentQuestion].topics[i] + ", ";
				}
				topicsString = topicsString.slice(0,-2);
				context.fillText(topicsString,260-topicsString.length*2,35);
			}
			else{
				context.fillText("Topic:",245,20);
				context.fillText(this.selectedQuestions[this.currentQuestion].topics[0],
				                 260-this.selectedQuestions[this.currentQuestion].topics[0].length*2,35);
			}
			context.font = "16pt Calibri";
			wrapText(context,this.selectedQuestions[this.currentQuestion].questionPrompt,
			         this.selectedQuestions[this.currentQuestion].promptCoords[0],
					 this.selectedQuestions[this.currentQuestion].promptCoords[1],
					 280, 25);
			
			answersLeft = this.selectedQuestions[this.currentQuestion].answers.slice(0);
			drawAnswerBoxes(answersLeft);
		}
		else{
			// ran out of questions
			this.displayResults();
		}
	}
	else{
		this.displayResults();
	}

}

function checkAnswer(answer){ // once an answer button has been pressed
	this.currentScreen = 3;
	if(answer == this.selectedQuestions[this.currentQuestion].answers[0]){
		this.correctAnswers += 1;
		context.font = "10pt Calibri";
		context.fillStyle = "green";
		context.fillText("Correct! (click anywhere in this window to continue)",10,415);
	}
	else{
		context.font = "10pt Calibri";
		context.fillStyle = "red";
		context.fillText("Wrong! (click anywhere in this window to continue)",10,415);
	}
	
	for(i=0;i<answerBoxes.length;i++){
		if(this.selectedQuestions[this.currentQuestion].answers[0]==answerBoxes[i].value){
			correctBoxNumber = i;
		}
	}
	drawAnswerBoxes(answersLeft,true,correctBoxNumber);
	
	this.answeredQuestions.push(this.selectedQuestions.splice(this.currentQuestion,1));
}

function displayResults(){ // when all questions have been answered
	this.currentScreen = 4;
	var score = Math.round(this.correctAnswers/this.questionNumber * 100 * 10) / 10;
	
	context.clearRect(0,0,canvas.width,canvas.height);
	context.font = "36pt Calibri";
	context.fillStyle = "black";
	context.fillText("Score",100,40);
	context.fillText(this.correctAnswers+"/"+this.questionNumber+" =",40,130);
	if(score<60){context.fillStyle = "red";}
	else if(score<80){context.fillStyle = "orange"}
	else{context.fillStyle = "green"}
	context.fillText(score+"%",170,130);
	context.font = "12pt Calibri";
	context.fillStyle = "black";
	context.textAlign = "center";
	if(this.questionNumber<this.numberOfQuestions){
		wrapText(context,"The quiz ended early because there is not yet enough questions "
		         +"for the topic(s) you chose.",canvas.width/2,180,canvas.width-20,20);
	}
	wrapText(context,"Click anywhere in this window to return to the menu.",
	         canvas.width/2,300,canvas.width-20,20);
	context.textAlign = "start";
}

function reset(){
	this.correctAnswers = 0;
	this.selectedQuestions = [];
	this.answeredQuestions = [];
	this.selectedTopics = [];
	this.questionNumber = 0;
	this.firstScreen();
}

function displayButton(button){
	context.beginPath();
	context.rect(button.x,button.y,
	             button.width,button.height);
	context.strokeStyle = "black";
	context.lineWidth = 2;
	context.stroke();
	if(button.activated == 1){
		context.fillStyle = "black";
		context.fill();
	}
	context.closePath();
}

function drawAnswerBoxes(answersLeft,textOnly=false,correctBoxNumber=null){
	if(!textOnly){
		for(i=0;i<answerBoxes.length;i++){
		var answerIndex = Math.floor(Math.random()*answersLeft.length);
		answerBoxes[i].value = answersLeft[answerIndex];
		answersLeft.splice(answerIndex,1);
		context.rect(answerBoxes[i].x,answerBoxes[i].y,
					 answerBoxes[i].width,answerBoxes[i].height);
		context.stroke();
		context.textAlign = "center";
		context.font = "12pt Calibri";
		wrapText(context,answerBoxes[i].value,answerBoxes[i].x+answerBoxes[i].width/2,
				 answerBoxes[i].y+answerBoxes[i].height/(2+(answerBoxes[i].value.split(" ").length/4)),answerBoxes[i].width-2,15);
		context.textAlign = "start"; // return to default value
		}
	}
	else{
		for(i=0;i<answerBoxes.length;i++){
			context.clearRect(answerBoxes[i].x+1,answerBoxes[i].y+1,
			                  answerBoxes[i].width-2,answerBoxes.height-2);
			if(answerBoxes[i].value==answerBoxes[correctBoxNumber].value){
				context.fillStyle="green";
			}
			else{context.fillStyle="red";}
			context.textAlign = "center";
			context.font = "12pt Calibri";
			wrapText(context,answerBoxes[i].value,answerBoxes[i].x+answerBoxes[i].width/2,
					 answerBoxes[i].y+answerBoxes[i].height/(2+(answerBoxes[i].value.split(" ").length/4)),answerBoxes[i].width-2,15);
			context.textAlign = "start"; // return to default value
		}
	}
}

function findNumberOfQuestionsPerTopic(topic,questionArray){
	questionsInTopic = 0;
	for(qIndex=0;qIndex<questionArray.length;qIndex++){
		questionIsInTopic = false;
		for(tIndex=0;tIndex<questionArray[qIndex].topics.length;tIndex++){
			if(questionArray[qIndex].topics[tIndex] == topic){
				questionIsInTopic = true;
			}
		}
		if(questionIsInTopic){
			questionsInTopic += 1;
		}	
	}
	if(topic=="D" && topicButtons["D (HL)"].activated == 1){
		questionsInTopic += findNumberOfQuestionsPerTopic("D (HL)",questionArray);
	}
	return questionsInTopic
}

function getMousePos(canvas, evt) {
	var rect = canvas.getBoundingClientRect();
	return {
	  x: evt.clientX - rect.left,
	  y: evt.clientY - rect.top
	};
}

function onTopicButtonPress(){
	if(!this.activated){this.activated = true;}
	else{this.activated = false;}
	main.firstScreen(); //update canvas
};

function isButtonPressed(button){ // also used for the slider
	if(mousePos.x>button.x && mousePos.x<button.x+button.width &&
	   mousePos.y>button.y && mousePos.y<button.y+button.height){
		return true
	}
	else{
		return false
	}
}

window.requestAnimFrame = (function(){ // used for slider
return window.requestAnimationFrame || window.webkitRequestAnimationFrame || 
       window.mozRequestAnimationFrame || 
	   function( callback ){ window.setTimeout(callback, 1000 / 60); };
})();

canvas.addEventListener('mouseup', function(evt) {
        mousePos = getMousePos(canvas, evt);
		mouseHold = false;
		//insert collision detection here
		if(main.currentScreen == 1){
				if(isButtonPressed(generateQuestionsButton)){
					main.filterQuestionsAndStart();
				}
			for(i=0;i<main.topics.length;i++){  //topicButtons
				if(isButtonPressed(topicButtons[main.topics[i]])){
					topicButtons[main.topics[i]].callback();
				}
			}
			if(isButtonPressed(topicButtons["D (HL)"])){ // since "D (HL)" is not in main.topics
				topicButtons["D (HL)"].callback();
			}
		}
		else if(main.currentScreen == 2){
			if(isButtonPressed(answerBoxes[0])){ // apparently a for loop for all 4 boxes does not work
				answerBoxes[0].callback()}
			if(isButtonPressed(answerBoxes[1])){answerBoxes[1].callback()}
			if(isButtonPressed(answerBoxes[2])){answerBoxes[2].callback()}
			if(isButtonPressed(answerBoxes[3])){answerBoxes[3].callback()}
		}
		else if(main.currentScreen == 3){main.nextQuestion()}
		else if(main.currentScreen == 4){main.reset()}
		else{
			alert("This message should not appear. Have you been messing with the currentScreen attribute?");
			main.reset();
		}
}, false);

function wrapText(context, txt, x, y, maxWidth, lineHeight) { //html5canvastutorials
        var words = txt.split(' ');
        var line = '';

        for(var n = 0; n < words.length; n++) {
          var testLine = line + words[n] + ' ';
          var metrics = context.measureText(testLine);
          var testWidth = metrics.width;
          if (testWidth > maxWidth && n > 0) {
            context.fillText(line, x, y);
            line = words[n] + ' ';
            y += lineHeight;
          }
          else {
            line = testLine;
          }
        }
        context.fillText(line, x, y);
      }

canvas.addEventListener("mousedown", function(evt) {
	mousePos = getMousePos(canvas, evt);
	mouseHold = true;
	if(isButtonPressed(numberOfQuestionsSlider) && main.currentScreen == 1){
		requestAnimFrame(function(){updateSlider(numberOfQuestionsSlider)});
	}
}, false);


// FIRST SCREEN VARIABLES//
// Question(topics,questionPrompt,answerArray);
q = [];
q[0] = new Question("2","Binary can best be defined as:",["A base-2 numeral system","A base-8 numeral system","A base-10 numeral system","A base-16 numeral system"]);
q[1] = new Question("2","One of the advantages of primary memory in comparison to secondary memory is that primary memory:",["is faster","is non-volatile","is cheaper", "usually has a higher storage capacity"]);
q[2] = new Question("2","One of the disadvantages of primary memory in comparison to secondary memory is that primary memory:",["is mainly volatile","is slower","is mainly read-only","is cheaper"]);
q[3] = new Question("2","What is the best reason why a computer's memory shouldn't consist entirely of primary memory?",["RAM is volatile","Primary memory is expensive compared to secondary memory","ROM cannot be written to", "Primary memory is too fast and will therefore overheat your CPU"])
q[4] = new Question("2","What is the binary number 01100111 in hexadecimal?",["67","C6","6C","76"]);
q[5] = new Question("2","The stages in the machine instruction cycle are, in order:",["Fetch, Decode, Execute, Store", "Fetch, Store, Decode, Execute", "Decode, Fetch, Execute, Store", "Decode, Execute, Fetch, Store"]);
q[6] = new Question("2","The main difference between RAM and ROM is that:",["ROM is read-only","ROM is larger than RAM","ROM is secondary memory","RAM is faster than ROM"]);
q[7] = new Question("2",'Why is the NAND gate sometimes referred to as an "universal" gate?',["It can be used to create every other gate","It is the most widely used logic gate","It is used in software all over the world","All intelligent species in the observable universe use it"]);
q[8] = new Question("2","What is the difference between an OR gate and an XOR gate?",["In an XOR gate, the output is 0 if both inputs are 1","In an XOR gate, the output is the opposite of an OR gate","In an XOR gate, there is only one input","In an XOR gate, the output is always 1"]);

//buttons
topicButtons = {};
topicButtons["1.1"] = new TopicButton(40,50,"1.1");
topicButtons["1.2"] = new TopicButton(40,70,"1.2");
topicButtons["2"] = new TopicButton(40,90,"2");
topicButtons["3"] = new TopicButton(40,110,"3");
topicButtons["4.1"] = new TopicButton(40,130,"4.1");
topicButtons["4.2"] = new TopicButton(40,150,"4.2");
topicButtons["4.3"] = new TopicButton(40,170,"4.3");
topicButtons["5"] = new TopicButton(40,210,"5");
topicButtons["6"] = new TopicButton(40,230,"6");
topicButtons["7"] = new TopicButton(40,250,"7");
topicButtons["D"] = new TopicButton(40,290,"D");
topicButtons["D (HL)"] = new TopicButton(180,270,"D (HL)"); // include HL questions

numberOfQuestionsSlider = new Slider(40,340,220,5,20);
generateQuestionsButton = new Button(50,360,200,50,filterQuestionsAndStart);

main = new MultipleChoice(q);
main.firstScreen();

// SECOND SCREEN VARIABLES //
answerBoxes = [];
answerBoxes[0] = new Button(20,240,130,80,function(){main.checkAnswer(this.value)});
answerBoxes[1] = new Button(150,240,130,80,function(){main.checkAnswer(this.value)});
answerBoxes[2] = new Button(20,320,130,80,function(){main.checkAnswer(this.value)});
answerBoxes[3] = new Button(150,320,130,80,function(){main.checkAnswer(this.value)});