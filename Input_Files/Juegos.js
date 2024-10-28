var myGamePiece;
var myScore;
var puntuation = 0;
var countdown = 90;
var end = false;
var game = 0;



function startGame1() {
	game = 1;
	console.log("Hoalala");
	myGameArea.start();
	myBackground = new component(480, 350, "imagenes/fondojuego.jpg", 0, 0,"image");
	myGamePiece = new component(50, 50, "imagenes/chocolate.webp", 10, 50,"image");
	myScore = new component("30px", "Emilys Candy", "black", 300, 40, "text");
	myCountDown = new component("30px", "Ubuntu", "black", 200, 40, "text");
	myFinishText = new component("45px","Ubuntu","red",150,150,"text");
	countdown = 90;
	puntuation = 0;
	end = false;
	
}

function startGame2(){
	game = 2;
	myGameArea.start();
	myBackground = new component(475, 275, "imagenes/diferencias1.jpg", 0, 0,"image");
	mydifference1 = new component(20, 20, "imagenes/blank.png", 2, 188,"image");
	mydifference2 = new component(20, 20, "imagenes/blank.png", 40, 50,"image");
	mydifference3 = new component(20, 20, "imagenes/blank.png", 170, 120,"image");
	mydifference4 = new component(20, 20, "imagenes/blank.png", 40, 150,"image");
	mydifference5 = new component(20, 20, "imagenes/blank.png", 30, 110,"image");
	mydifference6 = new component(20, 20, "imagenes/blank.png", 150, 170,"image");
	mydifference7 = new component(20, 20, "imagenes/blank.png", 130, 250,"image");
	myGamePiece = new component(0, 0, "imagenes/blank.png", 10, 50,"image");
	myScore = new component("0px", "Emilys Candy", "black", 300, 40, "text");
	myCountDown = new component("0px", "Ubuntu", "black", 200, 40, "text");
	myFinishText = new component("0px","Ubuntu","red",150,150,"text");
	
}


var myGameArea = {
	
  canvas : document.createElement("canvas"),
  start : function() {
	
    this.canvas.width = 480;
    this.canvas.height = 270;
	this.canvas.style = "background-color: #f1f1f1;"
    this.context = this.canvas.getContext("2d");
    document.body.insertBefore(this.canvas, document.body.childNodes[0]);
    this.frameNo = 0;
	document.getElementById('juego1').appendChild(this.canvas);
	this.interval = setInterval(updateGameArea, 20);
	if ( end == false){
		window.addEventListener('mousemove', function (e) {
		  myGameArea.x = e.pageX ;
		  myGameArea.y = e.pageY ;
		})
		window.addEventListener('mousedown', function (e) {
			let offset = myGameArea.canvas.getBoundingClientRect();
			myGameArea.x = e.clientX - offset.left;
			myGameArea.y = + e.screenY - offset.top -88;
		})
		 window.addEventListener('mouseup', function (e) {
		  myGameArea.x = false;
		  myGameArea.y = false;
		})
		 window.addEventListener('touchstart', function (e) {
		 let offset = myGameArea.canvas.getBoundingClientRect();
			myGameArea.x = e.clientX - offset.left;
			myGameArea.y = + e.screenY - offset.top -88;
			console.log(myGameArea.x);
			console.log(myGameArea.y);
		})
		window.addEventListener('touchend', function (e) {
		  myGameArea.x = false;
		  myGameArea.y = false;
		})
	}
  },
  clear : function() {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }
}

function component(width, height, color, x, y, type) {
    this.type = type;
    this.score = 0;
	if ( type == "image"){
		this.image = new Image();
		this.image.src = color;
		
	}
    this.width = width;
    this.height = height;
    this.speedX = 0;
    this.speedY = 0;    
    this.x = x;
    this.y = y;
    this.gravity = 0;
    this.gravitySpeed = 0;
	ctx = myGameArea.context;
	this.update = function() {
        if (this.type == "text") {
            ctx.font = this.width + " " + this.height;
            ctx.fillStyle = color;
            ctx.fillText(this.text, this.x, this.y);
        } else  {
			if ( this.type == "image"){
				ctx.drawImage(this.image,
				this.x,
				this.y,
				this.width, this.height);
			}
			else {
            ctx.fillStyle = color;
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
    }}
	this.clicked = function() {
		var myleft = this.x;
		var myright = this.x + (this.width);
		var mytop = this.y;
		var mybottom = this.y + (this.height);
		var clicked = true;
		if ((mybottom < myGameArea.y) || (mytop > myGameArea.y) || (myright < myGameArea.x) || (myleft > myGameArea.x) || (end = false)) {
			clicked = false;
			}
		return clicked;
  }

}

function updateGameArea() {
	console.log(game);
	myGameArea.clear();
	if ( game == 1){
	  if (myGameArea.x && myGameArea.y){
		if (myGamePiece.clicked()){
			myGamePiece.x = Math.floor(Math.random()*400) + 1;
			myGamePiece.y = Math.max(Math.floor(Math.random()*200) + 30, )
			puntuation += 1;
			}
	  }
	  myBackground.update();
	  myGamePiece.update();
	  myScore.text = "Puntos: " + puntuation;
	  myScore.update();
	  myCountDown.text = countdown;
	  myCountDown.update();
	  myFinishText.text = " ";
	  if(end == true){
			myFinishText.text = "Game Over"
		}
		myFinishText.update();
	}
	if (game == 2){
		 if (myGameArea.x && myGameArea.y){
			if (mydifference1.clicked()){
				mydifference1.image.src = "imagenes/red_circle.png";
				}
			if (mydifference2.clicked()){
				mydifference2.image.src = "imagenes/red_circle.png";
				}
			if (mydifference3.clicked()){
				mydifference3.image.src = "imagenes/red_circle.png";
				}
			if (mydifference4.clicked()){
				mydifference4.image.src = "imagenes/red_circle.png";
				}
			if (mydifference5.clicked()){
				mydifference5.image.src = "imagenes/red_circle.png";
				}
			if (mydifference6.clicked()){
				mydifference6.image.src = "imagenes/red_circle.png";
				}
			if (mydifference7.clicked()){
				mydifference7.image.src = "imagenes/red_circle.png";
				}
		  }
		myBackground.update();
		mydifference1.update();
		mydifference2.update();
		mydifference3.update();
		mydifference4.update();
		mydifference5.update();
		mydifference6.update();
		mydifference7.update();
}

}
  
function updateCountDown(){
	if (countdown < 0){ 
	end = true;}
	else {
	countdown = countdown - 1;
	end = false;}
	
}

count = setInterval(updateCountDown, 1000);