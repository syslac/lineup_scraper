select u.name, f.name, e.id_year, sum(p.vote) as sum
from presences r 
left join festival_edition e on e.id = r.id_festival_edition 
left join festival f on f.id = e.id_festival 
left join preferences p on p.id_artist = r.id_artist 
left join users u on u.id = p.id_user 
group by u.name, f.name, e.id_year
order by u.name, sum DESC;
