// Format the query on Samples using sample_id
frappe.form.link_formatters['Samples'] = function(value, doc) {
    if (doc.sample_id && doc.sample_id !== value) {
        return value + ': ' + doc.sample_id;
    } else {
        return value;
    }
}