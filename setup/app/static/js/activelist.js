
// #master
// #saved


var SavedRow = function(item, parentSelection) {
	var nameUI;
	var deleteUI;
	var row;

	row = parentSelection.append('tr');
	nameUI = row.append('td').text(item);
	deleteUI = row.append('td').text('delete');

	deleteUI.on('click', function() {row.remove();});
};

var ActiveRow = function(item, parentSelection, onSave) {
	var nameUI;
	var deleteUI;
	var saveUI;
	var row;

	row = parentSelection.append('tr');
	nameUI = row.append('td').append('a').attr('href', "http://www.behindthename.com" + item['href']).text(item['name']);
	deleteUI = row.append('td').append('span').attr('class', 'glyphicon glyphicon-remove'); //text('delete');
	saveUI = row.append('td').append('span').attr('class', 'glyphicon glyphicon-ok'); //.text('save');

	deleteUI.on('click', function() {row.remove();});
	saveUI.on('click', function() {
		onSave(item);
		row.remove();
	});
};

var masterTable = d3.select("#namebox table");
var savedTable = d3.select("#savedbox table");

var onSave = function(item){
	SavedRow(item, savedTable);
};

// data.forEach(function(item){
// 	ActiveRow(item, masterTable, onSave);
// });

