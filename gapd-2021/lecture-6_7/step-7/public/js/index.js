const width = 1600;
const height = 800;

var links;
var nodes;

var simulation;
var transform;

var canvas = d3.select("canvas");
var context = canvas.node().getContext('2d');

var xmlhttp = new XMLHttpRequest();
var option = "fraudulent-transation"

d3.select("select")
    .on("change", function (d) {
        var selected = d3.select("#d3-dropdown").node().value;
        option = selected;
        load_data(option);
    })


get_graph()

function load_data(option) {
    // Load the data for the selected dropdown option
}

function get_graph() {
    // Get the graph from the server
}
