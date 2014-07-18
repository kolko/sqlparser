select id from users;
select id, name from users;
select name from users;  --blaffjsh fusdif gie73e23
select name from users where id = 1;
select name from users where id = ( select userid from abonents);
select field as name from users;
select field, (select name from abonents where user_id=1) from users;
select field, (select name from abonents where user_id=users.id) from users;
select * from users;
select users.* from users;
select * from users where last_name is null;
select u.* from users u;
select
   b.*
from abonents_block b
where b.abonent_id=1
and (b.usluga_id=2 or 2 is null)
and (b.users_usluga_id=3 or 3 is null);
select * from users where id=1 or id=2 or id=3;