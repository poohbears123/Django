//variables
var location1;
var location2;
var location3;

var guess;
var hits =  0;
var guesses = 0;

var isSunk = false;

while(isSunk == false ){
    guess = prompt("Ready, Aim, Fire(enter number)")
    if (guess <0 || guess >6){
        alert ("please put a valid number")
    }
    else{ guesses = guesses + 1 
        if (guess == location1|| guess == location2 || guess == location3){
            hits += 1;
            if (hits == 3 ){
                isSunk = true;
                alert (" you sank my ship")
            }
        }
    }
}
var state = "you sank my battleship at " + guesses + "guesses" + "and your accuracy is" + (3/guesses) 

alert(state)