import re

with open('client/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the broken image map and legend
# The broken image is: <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/India_map_en.svg/800px-India_map_en.svg.png"...>
map_div_replacement = '''
                    <!-- Google GeoChart Container -->
                    <div id="regions_div" class="w-full h-[220px]"></div>
'''

content = re.sub(r'<!-- Using a generic India map placeholder -->.*?</div>', map_div_replacement, content, flags=re.DOTALL)

# Add google charts script to the end of the file before </body>
google_charts_script = '''
    <!-- Google Charts for Map -->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {
        'packages':['geochart'],
      });
      google.charts.setOnLoadCallback(drawRegionsMap);

      function drawRegionsMap() {
        var data = google.visualization.arrayToDataTable([
          ['State', 'Projects'],
          ['Uttar Pradesh', 25],
          ['Maharashtra', 18],
          ['Gujarat', 15],
          ['Karnataka', 12],
          ['Tamil Nadu', 9],
          ['Bihar', 8],
          ['Madhya Pradesh', 4],
          ['Rajasthan', 3],
          ['Odisha', 2],
          ['Kerala', 1]
        ]);

        var options = {
          region: 'IN',
          displayMode: 'regions',
          resolution: 'provinces',
          colorAxis: {colors: ['#dcfce7', '#166534']},
          backgroundColor: 'transparent',
          datalessRegionColor: '#f8fafc',
          defaultColor: '#f8fafc',
          tooltip: {textStyle: {fontName: 'Inter', fontSize: 12}},
          legend: 'none'
        };

        var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
        chart.draw(data, options);
      }
    </script>
</body>
'''
content = content.replace('</body>', google_charts_script)

with open('client/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Google GeoChart map successfully integrated into dashboard!")
