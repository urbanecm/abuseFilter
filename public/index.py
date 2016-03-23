#!/usr/bin/env python
#-*- coding: utf-8 -*-

print """
<html>
  <head>
  <meta charset="utf-8" />
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">

      // Load the Visualization API and the piechart package.
      google.load('visualization', '1.0', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table, 
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

      // Create the data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Topping');
      data.addColumn('number', 'Slices');
      data.addRows([
      """
import json

f = open('/data/project/urbanecmbot/abuseFilter/result.json', 'r')
data = json.loads(f.read())

res = []
res.append('["Ukončeno", ' + str(data['ended']) + '],')
res.append('["Stránka smazána", ' + str(data['pageDeleted']) + '],')
res.append('["Uloženo", ' + str(data['saved']) + '],')
res.append('["Upraveno", ' + str(data['edited']) + ']')
for i in res:
        print i
print """
      ]
      );

      // Set chart options
      var options = {'title':'Editační filtr 15 - statistika',
                     'width':400,
                     'height':300};

      // Instantiate and draw our chart, passing in some options.
      var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }
    </script>
  </head>

  <body>
    <div id="chart_div" style="width:400; height:300"></div>
  </body>
</html>
"""
