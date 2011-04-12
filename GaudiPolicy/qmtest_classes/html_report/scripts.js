/// Global variable for the summary content.
var test_results = {};

/// Digest the summary JSON object, filling the test_results variable.
function parseSummary(summary) {
	// Prepare the counters
	test_results.counter = {"PASS":     0,
			                "FAIL":     0,
			                "UNTESTED": 0,
			                "ERROR":    0,
			                "total":    summary.length};
	test_results.tests = {};
	test_results.not_passed = [];
	test_results.all_tests = [];
	for (var i in summary) {
		var test = summary[i];
		// Update the counter of the outcome.
		++test_results.counter[test.outcome];
		//var test_path = split(".", test.id);
		test_results.tests[test.id] = test;
		test_results.all_tests.push(test.id);
		if (test.outcome != "PASS") {
			test_results.not_passed.push(test.id);
		}
	}
}

/**
 * Load the annotations file (annotations.json) and fill the annotations block of
 * the DOM.
 */
function loadAnnotations() {
	// Asynchronous retrieval
	$.get('annotations.json', function(data) {
		// Prepare a table with the annotations
		var tbody = $("<tbody/>");
		// This keys are special and must appear first in the table
		var keys = ["qmtest.run.start_time", "qmtest.run.end_time"];
		// Add all the other keys to the list of keys
		for (var key in data) {
			if ($.inArray(key, keys) == -1) {
				keys.push(key);
			}
		}
		// Add the rows of the table
		var running = false;
		for (var i in keys) {
			var key = keys[i];
			var value = data[key];
			if (!value) { // In case of empty value for a key...
				if (key == "qmtest.run.end_time") {
					// ... if the key is "end_time", it means the tests are running
					value = "RUNNING".italics() +
					        " (the page will be updated every 5s)".small();
					running = polling;
				} else {
					// ... otherwise print a meaningful "None"
					value = "None".italics();
				}
			} else {
				if ($.isArray(value)) {
					// In case the value is an Array, let's format it as a list
					var tmp = $('<ul/>');
					for (i in value) {
						tmp.append($('<li/>').text(value[i]))
					}
					value = tmp;
				}
			}
			tbody.append($("<tr/>")
				.append($('<td/>').addClass("key").text(key))
				.append($('<td/>').addClass("value").html(value)));
		}
		// Insert the code in the annotations block and enable the toggle button
		$('#annotations').html($('<table/>').append(tbody)).makeToggleable();
	}, "json");
}

/// Display the summary table
function renderSummary(element) {
	var counter = test_results.counter;
	// Prepare a table layout (like the one produced usually by QMTest).
	var tbody = $("<tbody/>");
	// row with the total
	tbody.append($("<tr/>")
		 .append($("<td align='right'/>").text(counter.total))
		 .append($("<td colspan='3'/><td>tests total</td>")));
	var result_types = ["FAIL", "ERROR", "UNTESTED", "PASS"];
	for (var i in result_types) {
		var result_type = result_types[i];
		if (counter[result_type]) {
			tbody.append($("<tr/>")
				     .append($("<td align='right'/>")
					     .text(counter[result_type]))
				     .append("<td>(</td>")
				     .append($("<td align='right'/>")
					     .text(Math.round(counter[result_type]
							      / counter.total * 100)))
				     .append("<td>%)</td>")
				     .append($("<td/>")
					     .text("tests " + result_type))
				     .addClass(result_type));
		}
	}
	element.html($("<table/>").html(tbody));
}

/** Generate foldable lists.
 */
jQuery.fn.foldable = function() {
    this.each(function() {
	    var me = $(this);
	    me.addClass("folded")
	    // wrap the content of the element with a clickable span
	    // (includes the ul)
	    .wrapInner($("<span class='clickable'/>")
		       .click(function(){
			       var me = $(this);
			       me.next().toggle();
			       me.parent().toggleClass("folded expanded");
			       return false; // avoid bubbling of the event
			   }));
	    // this moves the ul after the span (and hides it in the meanwhile)
	    me.append($("span > ul",me).hide());
	});
};

/** Modify the items that have the "url" data, making them clickable
 *  and followed by a hidden block with the content of the link specified.
 */
jQuery.fn.loader = function() {
    this.each(function() { // loop over all the selected elements
      var me = $(this);
      if (me.data("url")) { // modify the element only if it does have a data "url"
	  me.addClass("folded")
	      // wrap the "text" of the element with a clickable span that loads the url
	      .wrapInner($("<span class='clickable'/>")
			 .click(function(){ // trigger the loading on click
				 var me = $(this);
				 me.after($("<div/>").load(me.parent().data("url")));
				 me.unbind("click"); // replace the click handler
				 me.click(function(){ // this handler just toggle the visibility
					 var me = $(this);
					 me.next().toggle();
					 me.parent().toggleClass("folded expanded");
					 return false; // avoid bubbling of the event
				     });
				 me.parent().toggleClass("folded expanded");
				 return false; // avoid bubbling of the event
			     }));
      }
    });
};

/**
 * Helper function to re-use the code for the toggle button callback
 */
jQuery.fn.toggleNextButton = function(data) {
	if (data === undefined) data = {};
	if (data.hide === undefined) data.hide = "(hide)";
	if (data.show === undefined) data.show = "(show)";
	if (data.start_visible === undefined) data.start_visible = false;
	this.click(function() {
		var me = $(this);
		me.next().toggle();
		if (me.next().is(":visible")) {
			me.text(data.hide);
		} else {
			me.text(data.show);
		}
	}).text(data.start_visible ? data.hide : data.show)
	  .next().toggle(data.start_visible);
	return this;
}

/** Make a given element toggleable using a show/hide button inserted just before
 *  it.
 */
jQuery.fn.makeToggleable = function() {
	this.each(function() {
		var btn = $("<span class='togglelink clickable'/>");
		$(this).before(btn);
		btn.toggleNextButton();
	});
}

/// Display the list of results
function renderResults(element, tests) {
    if (!tests) tests = test_results.not_passed;

    var ul = $("<ul/>");
    for (var i in tests) {
	var test = test_results.tests[tests[i]];

	var entry = $("<li/>")
	    .append($("<span class='testid'/>").text(test.id))
	    .append(": ")
	    .append($("<span/>").addClass(test.outcome).text(test.outcome));
	if (test.cause) {
	    entry.append(" ")
		.append($("<span class='cause'/>")
			.text(test.cause));
	}
	var fields = $("<ul class='fieldid'/>");
	for (var j in test.fields) {
	    fields.append($("<li/>").data("url", test.id + "/" + test.fields[j])
			  .text(test.fields[j]));
	}
	entry.append(fields);
	ul.append(entry);
    }

    $("li", ul).loader();
    $("li:has(ul)", ul).foldable();

    element.append(ul);
}

/// Code executed when the page is ready.
$(function () {
	$.get("summary.json", function(summary) {
		parseSummary(summary);
		renderSummary($("#summary"));
		renderResults($("#results"));

		$("#all_results").hide()
		  .before($("<span class='togglelink clickable'>(show)</span>")
				  .click(function(){
					  var me = $(this);
					  me.unbind("click");
					  renderResults(me.next(), test_results.all_tests);
					  me.toggleNextButton({start_visible: true});
				  }));
	}, "json");

	loadAnnotations();
});
