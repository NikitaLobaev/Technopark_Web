$("#ajax_comment_to_question").submit(event => {
	event.preventDefault();
}).on("submit", () => {
	$.ajax({
		error: response => alert("error: " + response.responseJSON.error),
		data: $("#ajax_comment_to_question").serialize(),
		success: data => {
			ajax_comment_to_question(data.profile_url, data.avatar_url, data.text);
		},
		type: 'POST',
		url: '/ajax/comment_to_question'
	});
});
const ajax_rate_question = like => {
	let lastRating = parseInt($(this).text(), 10), rating, question_rating = $("#question_rating");
	if (like) {
		$("#question_like").toggleClass("text-success");
		rating = lastRating + 1;
		switch (lastRating) {
			case -1:
				question_rating.toggleClass("text-danger");
				break;
			case 0:
				question_rating.toggleClass("text-success");
				break;
		}
	} else {
		$("#question_dislike").toggleClass("text-danger");
		rating = lastRating - 1;
		switch (lastRating) {
			case 1:
				question_rating.toggleClass("text-success");
				break;
			case 0:
				question_rating.toggleClass("text-danger");
				break;
		}
	}
	$("#id_like").prop("checked", like);
	$.ajax({
		error: response => alert("error: " + response.responseJSON.error),
		data: $("#ajax_question_rating").serialize(),
		success: () => {
			/*switch (rating) {
				case 0:
					if (lastRating === 1) {
						question_rating.toggleClass("text-success");
					} else {
						question_rating.toggleClass("text-danger");
					}
					break;
				case 1:
					if (lastRating === 0) {
						question_rating.toggleClass("text-success");
					}
					break;
				case -1:
					if (lastRating === 0) {
						question_rating.toggleClass("text-danger");
					}
					break;
			}*/
			question_rating.val(rating);
		},
		type: 'POST',
		url: '/ajax/rate_question'
	});
}
const ajax_comment_to_question = (profile_url, avatar_url, text) => {
	$("#comments_to_question").append("<div class=\"media mb-4\">\n" +
		"\t<a href=\"" + profile_url + "\">\n" +
		"\t\t<img class=\"d-flex mr-3 rounded-circle\" src=\"" + avatar_url + "\" style=\"width: 64px; height: 64px;\" alt=\"Аватар пользователя\">\n" +
		"\t</a>\n" +
		"\t<div class=\"media-body\">\n" +
		"\t\t<h5 class=\"mt-0\"><a href=\"" + profile_url + "\">{{ comment.author }}</a></h5>\n" +
		"\t\t" + text + "\n" +
		"\t</div>\n" +
		"</div>");
}
			/*$('html,body').animate({
				scrollTop: $("#answer_" + data.answer_id).offset().top
			}, 'slow');*/