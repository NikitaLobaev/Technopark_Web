const users_pagination_form_submit = page => {
	let users_pagination_form = document.forms["users_pagination_form"];
	users_pagination_form.elements["page"].value = page;
	users_pagination_form.submit();
};