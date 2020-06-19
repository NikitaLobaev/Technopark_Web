const $questionRatingPictureDislike = $("#question_rating_picture_dislike");
const $questionRatingPictureLike = $("#question_rating_picture_like");
const $questionRatingLike = $("#question_rating_like");
const $questionRating = $("#question_rating");
const $questionRatingForm = $("#question_rating_form");
const $questionRatingRated = $("#question_rating_rated");
const csrfmiddlewaretoken = Cookies.get("csrftoken");
$.ajaxSetup({
	beforeSend: (xhr, settings) => {
		if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
		}
	}
});
if ($questionRatingRated.prop("checked")) {
	if ($questionRatingLike.prop("checked")) {
		$questionRatingPictureLike.toggleClass("text-success");
	} else {
		$questionRatingPictureDislike.toggleClass("text-danger");
	}
}
const ajaxQuestionRating = () => $.ajax({
	error: response => {
		alert("Во время AJAX-запроса произошла ошибка");
		console.log(response);
	},
	data: $questionRatingForm.serialize(),
	type: "POST"
});
$questionRatingPictureDislike.on("click", () => {
	$questionRatingPictureDislike.toggleClass("text-danger");
	const rating = parseInt($questionRating.text(), 10);
	let ratingIsNew = true;
	if ($questionRatingPictureLike.hasClass("text-success")) { //лайк заменён на дизлайк
		$questionRatingPictureLike.removeClass("text-success");
		if (rating === 2) {
			$questionRating.removeClass("text-success");
		} else if (rating === 1) {
			$questionRating.removeClass("text-success");
			$questionRating.addClass("text-danger");
		}
		$questionRating.text(rating - 2);
	} else if ($questionRatingPictureDislike.hasClass("text-danger")) { //дизлайк поставлен
		if (rating === 1) {
			$questionRating.removeClass("text-success");
		} else if (rating === 0) {
			$questionRating.addClass("text-danger");
		}
		$questionRating.text(rating - 1);
	} else { //дизлайк убран
		if (rating === -1) {
			$questionRating.removeClass("text-danger");
		} else if (rating === 0) {
			$questionRating.addClass("text-success");
		}
		$questionRating.text(rating + 1);
		ratingIsNew = false;
	}
	$questionRatingLike.prop("checked", false);
	console.log($questionRatingForm.serialize());
	ajaxQuestionRating();
	$questionRatingRated.prop("checked", ratingIsNew);
});
$questionRatingPictureLike.on("click", () => {
	$questionRatingPictureLike.toggleClass("text-success");
	const rating = parseInt($questionRating.text(), 10);
	let ratingIsNew = true;
	if ($questionRatingPictureDislike.hasClass("text-danger")) { //дизлайк заменён на лайк
		$questionRatingPictureDislike.removeClass("text-danger");
		if (rating === -2) {
			$questionRating.removeClass("text-danger");
		} else if (rating === -1) {
			$questionRating.removeClass("text-danger");
			$questionRating.addClass("text-success");
		}
		$questionRating.text(rating + 2);
	} else if ($questionRatingPictureLike.hasClass("text-success")) { //лайк поставлен
		if (rating === -1) {
			$questionRating.removeClass("text-danger");
		} else if (rating === 0) {
			$questionRating.addClass("text-success");
		}
		$questionRating.text(rating + 1);
	} else { //лайк убран
		if (rating === 1) {
			$questionRating.removeClass("text-success");
		} else if (rating === 0) {
			$questionRating.addClass("text-danger");
		}
		$questionRating.text(rating - 1);
		ratingIsNew = false;
	}
	$questionRatingLike.prop("checked", true);
	console.log($questionRatingForm.serialize());
	ajaxQuestionRating();
	$questionRatingRated.prop("checked", ratingIsNew);
});

/*$("#ajax_comment_to_question").submit(event => {
	event.preventDefault();
}).on("submit", () => {
	$.ajax({
		error: response => alert("error: " + response.responseJSON.error),
		data: $("#ajax_comment_to_question").serialize(),
		success: data => {
			ajax_comment_to_question(data.profile_url, data.avatar_url, data.author, data.text);
		},
		type: 'POST',
		url: '/ajax/comment_to_question'
	});
});
const ajax_comment_to_question = (profile_url, avatar_url, author, text) => {
	$("#comments_to_question").prepend("<div class=\"media mb-4\">\n" +
		"\t<a href=\"" + profile_url + "\">\n" +
		"\t\t<img class=\"d-flex mr-3 rounded-circle\" src=\"" + avatar_url + "\" style=\"width: 64px; height: 64px;\" alt=\"Аватар пользователя\">\n" +
		"\t</a>\n" +
		"\t<div class=\"media-body\">\n" +
		"\t\t<h5 class=\"mt-0\"><a href=\"" + profile_url + "\">" + author + "</a></h5>\n" +
		"\t\t" + text + "\n" +
		"\t</div>\n" +
		"</div>");
}*/
			/*$('html,body').animate({
				scrollTop: $("#answer_" + data.answer_id).offset().top
			}, 'slow');*/
