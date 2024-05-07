frappe.pages['colegios'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Colegios',
		single_column: true
	});
	const response = {}
	page.wrapper.html(frappe.render_template("home",  response ));
}
