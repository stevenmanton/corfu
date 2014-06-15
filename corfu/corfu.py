
from uuid import uuid4

from jinja2 import Template

class d3vis(object):

	def __init__(self):
		self.id = uuid4()
		self.id_str = "vis_" + str(self.id).replace("-", "")
		return

	@property
	def html_template(self):
		html_template = Template("""
		<div id="{{ vis_str }}"></div>

		<script type="text/javascript">
		require.config({paths: {d3: "http://d3js.org/d3.v3.min"}});

		require(["d3"], function(d3) {
		  console.log(d3.version);
		  
		  {{ vis_js }}
		});

		</script>
		""")

		return html_template.render(vis_str = self.id_str,
			vis_js = self.vis_js_template)

	def _to_html(self):
		return self.html_template

class testvis(d3vis):
	vis_js_template = """
	console.log(d3.version);
	  
	  var svg = d3.select("#{{ vis_str }}").append("svg")
	    .attr("height",100)
	  
	  var circle = svg.selectAll("circle")
	    .data([10, 20, 30, 40])
	    .enter()
	    .append("circle")
	    .attr("r", function(d) { return d })
	    .attr("cx", function(d, i){return 50 + (i*80)})
	    .attr("cy", 50);
	"""

	test_str = "yo yo yo"




