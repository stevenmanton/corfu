
import json
from uuid import uuid4

from jinja2 import Template

class D3Vis(object):

    def __init__(self):
        # Visualization uuid:
        self.id = uuid4()
        self.id_str = "vis_" + str(self.id).replace("-", "")

        self.vis_css_template = ''
        self.vis_js_template = ''
        return

    @property
    def html_template(self):
        html_template = Template("""
        <div id="{{ vis_str }}"></div>

        <style>
            {{ vis_css }}
        </style>

        <script type="text/javascript">
        require.config({paths: {d3: "http://d3js.org/d3.v3.min"}});

        require(["d3"], function(d3) {
          console.log(d3.version);
          
          {{ vis_js }}
        });

        </script>
        """)

        template_dict = {'vis_str': self.id_str,
            'vis_js': self.vis_js_template,
            'vis_css': self.vis_css_template,
            'vis_data_json': self.data_json}
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

class CalendarView(D3Vis):
    def __init__(self, data={}):
        D3Vis.__init__(self)

        self.vis_css_template = """
            body {
              font: 10px sans-serif;
              shape-rendering: crispEdges;
            }

            .day {
              fill: #fff;
              stroke: #ccc;
            }

            .month {
              fill: none;
              stroke: #000;
              stroke-width: 2px;
            }

            .RdYlGn .q0-11{fill:rgb(165,0,38)}
            .RdYlGn .q1-11{fill:rgb(215,48,39)}
            .RdYlGn .q2-11{fill:rgb(244,109,67)}
            .RdYlGn .q3-11{fill:rgb(253,174,97)}
            .RdYlGn .q4-11{fill:rgb(254,224,139)}
            .RdYlGn .q5-11{fill:rgb(255,255,191)}
            .RdYlGn .q6-11{fill:rgb(217,239,139)}
            .RdYlGn .q7-11{fill:rgb(166,217,106)}
            .RdYlGn .q8-11{fill:rgb(102,189,99)}
            .RdYlGn .q9-11{fill:rgb(26,152,80)}
            .RdYlGn .q10-11{fill:rgb(0,104,55)}
            """

        self.vis_js_template = """
            var width = 960,
                height = 136,
                cellSize = 17; // cell size

            var day = d3.time.format("%w"),
                week = d3.time.format("%U"),
                percent = d3.format(".1%"),
                format = d3.time.format("%Y-%m-%d");

            var color = d3.scale.quantize()
                .domain([-.05, .05])
                .range(d3.range(11).map(function(d) { return "q" + d + "-11"; }));

            var svg = d3.select("#{{ vis_str }}").selectAll("svg")
                .data(d3.range(2000, 2002))
              .enter().append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("class", "RdYlGn")
              .append("g")
                .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");

            svg.append("text")
                .attr("transform", "translate(-6," + cellSize * 3.5 + ")rotate(-90)")
                .style("text-anchor", "middle")
                .text(function(d) { return d; });

            var rect = svg.selectAll(".day")
                .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
              .enter().append("rect")
                .attr("class", "day")
                .attr("width", cellSize)
                .attr("height", cellSize)
                .attr("x", function(d) { return week(d) * cellSize; })
                .attr("y", function(d) { return day(d) * cellSize; })
                .datum(format);

            rect.append("title")
                .text(function(d) { return d; });

            svg.selectAll(".month")
                .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
              .enter().append("path")
                .attr("class", "month")
                .attr("d", monthPath);

            var data = {{ vis_data_json }};

              rect.filter(function(d) { return d in data; })
                  .attr("class", function(d) { return "day " + color(data[d]); })
                .select("title")
                  .text(function(d) { return d + ": " + percent(data[d]); });

            function monthPath(t0) {
              var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
                  d0 = +day(t0), w0 = +week(t0),
                  d1 = +day(t1), w1 = +week(t1);
              return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
                  + "H" + w0 * cellSize + "V" + 7 * cellSize
                  + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
                  + "H" + (w1 + 1) * cellSize + "V" + 0
                  + "H" + (w0 + 1) * cellSize + "Z";
            }

            d3.select(self.frameElement).style("height", "2910px");"""

        self.data = data
    
    @property
    def data_json(self):
        return json.dumps(self.data)


    