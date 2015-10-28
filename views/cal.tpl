<head>
  % import re
  <link rel="stylesheet" type="text/css" href="/assets/cal.css/"/>
</head>

<body>
  <h2>HackiCal</h2>
  <div> {{!cal}} </div>
  <div>
    <% p_y, p_m, n_y, n_m = adjacent
     if p_y:
         if p_m:
    %>
            <a href="/{{p_y}}/{{p_m}}/">Prev</a>
    %     else:
            <a href="/{{p_y}}/">Prev</a>
    %     end
    % end
    <% if n_y:
         if n_m:
    %>
            <a href="/{{n_y}}/{{n_m}}/">Next</a>
    %    else:
            <a href="/{{n_y}}/">Next</a>
    %    end
    % end
  </div>
<div>
  <h2>Historical Events</h2>
  <ol>
  % for e in events:
    % desc = re.split(r'\.(ref|{|<a href|amp)', e["description"])[0]
    % desc = re.sub(r'{{.+}}', '', desc.replace('ampndash', '–').replace("\\'", "'"))
    % date = '/'.join(reversed(e["date"].split('/'))) if e["date"] else ''
    <li>{{!desc}} -- {{date}}</li>
  % end
  </ol>
</div>
</body>
