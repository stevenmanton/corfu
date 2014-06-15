
from uuid import uuid4

from jinja2 import Template

class D3Vis(object):

	def __init__(self):
		# Visualization uuid:
		self.id = uuid4()
		self.id_str = "vis_" + str(self.id).replace("-", "")

		self.vis_js_template = ''
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

		template_dict = {'vis_str': self.id_str,
			'vis_js': self.vis_js_template}
		return render(html_template, template_dict)

	def _to_html(self):
		return self.html_template

class TestVis(D3Vis):

	def __init__(self):
		# Class inheritance; pick your poison:
		# super(TestVis, self).__init__()  # becomes super().__init__() in py3
		D3Vis.__init__(self)

		self.vis_js_template = """
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

def render(template, template_dict):
	# Render the jinja2 template twice because some substitute strings also
	# need rendering:
	return Template(template.render(template_dict)).render(template_dict)


