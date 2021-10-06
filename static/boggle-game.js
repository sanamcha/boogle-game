class BoggleGame {

    constructor(boardId, seconds = 60) {
        this.seconds = seconds;
        this.showTimer();
        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);
        this.time = setInterval(this.ticTick.bind(this), 1000);
        $(".add-word", this.board).on("submit", this.handleSubmitBtn.bind(this));
    }

    showWord(word){
        $(".words", this.board).append($("<li>", { text: word}));
    }

    showScore(){
        $(".score", this.board).text(this.score);
    }

    showMessage(message, clues) {
        $(".message",this.board).text(message).removeClass().addClass(`message ${clues}`);
    }

    async handleSubmitBtn(e){
        e.preventDefault();
        let $word = $(".word", this.board)

        let word = $word.val();
        if(!word) return;

        if(this.words.has(word)){
            this.showMessage(`Try again, you already selected ${word}`, "err");
            return;
        }

        //check for validity in server
        const resp = await axios.get("/check-word", { params: { word: word }});

        if(resp.data.result === "not-word") {
            this.showMessage(`sorry, ${word} is not a valid word`, "err");
        } else {
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`Good job, Word added: ${word}`, "ok");
        }
        $word.val("").focus();
    }
    //timer
    showTimer(){
        $(".time", this.board).text(this.seconds);
    }

    //time sec passing
    async ticTick() {
        this.seconds -= 1;
        this.showTimer();

        if(this.seconds === 0) {
            clearInterval(this.time);
            await this.gameScore();
        }
    }
    //update score and message

    async gameScore() {
        $(".add-word", this.board).hide();
        const resp = await axios.post("/get-score", { score: this.score });
        if (resp.data.newBestScore) {
            this.showMessage(`New best record: ${this.score}`, "ok");
        } else {
            this.showMessage(`Final score: ${this.score}`, "ok");
        }
    }
}

let game = new BoggleGame("boggle-game", 60);