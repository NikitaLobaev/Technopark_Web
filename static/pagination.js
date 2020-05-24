const pagination_form_submit = page => {
	let $form = $('form#pagination');
	$('#id_page').val(page);
	$form.submit();
};