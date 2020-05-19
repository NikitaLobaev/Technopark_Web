const questions_pagination_form_submit = page => {
	let questions_pagination_form = document.forms["questions_pagination_form"];
	questions_pagination_form.elements["page"].value = page;
	questions_pagination_form.submit();
};