<head>
<link rel="stylesheet" type="text/css" href="/assets/cal.css/"/>
</head>
<body>
<h1>Cal</h1>
<div> {{!cal}} </div>
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
</body>
