document.onload = () => {
	
};
const rate_question = like => {
	if (like) {
		$("#question_like").toggleClass("text-success");
	} else {
		$("#question_dislike").toggleClass("text-danger");
	}
	//$.ajax();
}