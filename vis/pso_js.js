$(document).ready(function(){
	if (!data) return console.log('Data file not found..');
	visualize(data);
	//test();
});


function create_single_particle(id_, x, y, xsvg, scale_){
	var particle = xsvg.append("g").attr("id", "p_"+id_).attr("transform", "translate("+scale_(x)+", "+y+")");


	var particle_ = particle.append("rect")
		.attr("class", "particle")
		//.attr("id", "p_"+id_)
		//.attr("x", scale_(x))
		//.attr("y", y)
		.attr("width", 5)
		.attr("height", 25);

	var text_ = particle.append("text")
						//.attr("x", scale_(x))
						//.attr("y", y)
						.attr("dy", -10)
						.text(id_)
						.style("font-size", "5px");

	if (id_ == -1){
		particle.style("stroke", "green")
		particle.style("fill", "blue");
	}
	else if (id_ == -2){
		particle.style("stroke", "red")
		particle.style("fill", "red");
	}
	else{
		particle.style("stroke", "black")
		particle.style("fill", "lightgreen");
	}
}


function visualize(t){
	var created = {};

	//create svg
	var margin = {top: 0, right: 10, bottom: 50, left: 10};
	var width = 1024 - margin.left - margin.right;
    var height = 300 - margin.top - margin.bottom;

    var max_val = Math.max.apply(Math,data.map(function(o){return o.new_x;}));

	var svg = d3.select("#pso_viz").append("svg").attr("width", width).attr("height", height);

	var axisScale = d3.scale.linear().domain([0, max_val]).range([0, 985]);

	var xAxis = d3.svg.axis().scale(axisScale);

	
	var xAxisGroup = svg.append("g")
						.style({'stroke': 'gray', 
								'fill': 'none', 
								'stroke-width': '1px', 
								'font-family': 'monospace',
								'font-size': '11px'})
						.attr("transform", "translate(5," + (height - 40)  + ")")
						.attr("width", width)
						.attr("height", height)
						.call(xAxis.orient("top"));

	//create the particles
	for (each_particle in t){
		var id_ = t[each_particle].id;

		if (!(id_ in created)) {
			var x = t[each_particle].x;
			var y = t[each_particle].y;
			create_single_particle(id_, x, y, xAxisGroup, axisScale);
			created[id_] = true;
		}
	}
	
	
	//move the particles based on their data
	for (each_particle in t){
		_id = "p_"+t[each_particle].id;
		particle = d3.select("#"+_id);

		u = particle
			.transition()
			.ease("cubic-in-out")
			.duration(1000)
			.delay(each_particle * 1000 * 0.1)
			//.attr("x", axisScale(t[each_particle].new_x))
			//.attr("y", t[each_particle].new_y);
			.attr("transform", "translate("+axisScale(t[each_particle].new_x)+", "+t[each_particle].new_y+")");
	}

	//add trace_recs
	var trace_recs = "<li>The target of the objective function here is "+results.target_value+".</li>";
	trace_recs += "<li>The number of particles is "+results.n_particles+".</li>";
	trace_recs += "<li>Max velocity here is "+results.v_max+".</li>";
	trace_recs += "<li>Max number of epochs is "+results.max_epochs+".</li>";

	$('#trace_recs').html(trace_recs);

	//apply the styles
	d3.selectAll(".particle").on("mouseover", mouseover_p).on("mouseout", mouseout_p);
}

//mouseover fancy stuff
function mouseover_p(){
	d3.select(this).style("stroke", "pink");
}

//mouseout fancy stuff
function mouseout_p(){
	if (this.id == "p_-1"){
		d3.select(this).style("stroke", "green");
	}
	else if (this.id == "p_-2"){
		d3.select(this).style("stroke", "red");
	}
	else{
		d3.select(this).style("stroke", "black");
	}
}


function test(){
	max_val = 2300;
	min_val = 0;
	width = 1024;
	height = 250;	
	var svg_container = d3.select("#pso_viz").append("svg").attr("width", width).attr("height", height);	

	var axis_scale = d3.scale.linear().domain([min_val, max_val]).range([0, 100]);

	var x_axis = d3.svg.axis().scale(axis_scale);

	var x_axisg = svg_container.append("g").call(x_axis);

	var group = svg_container.append("g").attr("id", "group");

	rect = group.append("rect").attr("x", 50).attr("y", 50).attr("width", 10).attr("height", 10).style("stroke", "black").style("fill", "none");

	text = group.append("text").attr("x", 55).attr("y", 55).text("wah");

	group.transition().ease("cubic-in-out").duration(1000).attr("transform", "translate(200, 0)");




}