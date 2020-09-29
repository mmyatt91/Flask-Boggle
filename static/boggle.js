// STEP THREE
class Game_Boggle {
    // Create new game at this DOM id 
    constructor(boardId, secs = 60) {
        this.secs = secs; // the length of the game
        this.showTimer() // display timer and starting secs

        // Game Starts
        this.score = 0 
        this.words = new Set ();
        this.board = $("#" + boardId);

        this.timer = setInterval(this.tick.bind(this), 1000)

        $(".sub-guess", this.board).on("submit", this.handleSubmit.bind(this));
    }

    // Show checked word in list 
    showWord(word) {
        $(".words", this.board).append($("<li>", { text:word }));
    }

    // Show Updated Score
    showScore() {
        $(".score", this.board).text(this.score);
    }

    // Show msg 
    showMessage(msg, cls) {
        $(".msg", this.board)
           .text(msg)
           .removeClass()
           .addClass(`msg ${cls}`);
    }

    // Takes care of submission of word 
    async handleSubmit(e) {
        e.preventDefault();
        const $word = $(".word", this.board);
    
        let word = $word.val();
        if(!word) return;
    
        if(this.words.has(word)) {
            this.showMessage(`Already found ${word}`, "err");
            return; 
    }
    

    // Check for validity of word submitted -- using check_valid_word function from boogle.py
    const res = await axios.get("/check-word", { params: {word:word}});

    if (res.data.result === "not-word") {
        this.showMessage(`${word} not found in Webster's Dictionary`, "err"); 
    } else if (res.data.result === "not-on-board" ) {
        this.showMessage(`${word} not found on Boggle Board`, "err");
    } else {
        this.showWord(word);
        this.score += word.length;
        this.showScore();
        this.words.add(word);
        this.showMessage(`Great Guess! Added: ${word}`, "ok")
    }

    $word.val("").focus();
    }

    // Update Timer in Dom 
    showTimer() {
        $(".timer", this.board).text(this.secs);
    }

    async tick () {
        this.secs -= 1;
        this.showTimer();

        if(this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    async scoreGame() {
        $(".sub-guess", this.board).hide();
        const res = await axios.post("/post-score", {score: this.score});

        if (res.data.brokeRecord) {
            this.showMessage(`New Highest Score: ${this.score}`, "ok");
        } else {
            this.showMessage(`Final Score: ${this.score}`, "ok");
        }
    }
}