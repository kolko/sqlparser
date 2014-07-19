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
select * from users where (name=1 or (surname=2 and last_name=3) or name = 4) and id < 3;
select * from users where name = 'Test user name';
select "from" from users;
select * from users where name = 'Aprill O\'neel';
select z.a from b as z where b=z.c;
SeLeCt * FrOm UsErS As u;
select first 10 id from users;
select last 20 id from users;
select (id) from users;
select (id, name) from users; --Don't know this is correct
select first 30 *
from abonents
where modified in (1,2,3);
select * from users where COALESCE(deleted, 0)=0;
select sum(balance) from users;
select count(*) from users;
select first 1 random() from users;
select debit - credit from users;
select (debit - credit + ostatok) as balance from users;
select first 1 1 - 2 / 3 from users; -- трабла с порядком вычислений - забиваем
select * from users where id <> 1 and id != 2;
select u.*
from USERS_USLUGA uu
--left join USLUGA u on uu.usluga_id=u.id
where uu.abonent_id = 1 and uu.activated=1 and u.system_type=9 and COALESCE(UU.DELETED, 0) != 1;
select first 2 U.ID,
U.ABONENT_ID,
ABON.ACCOUNT_ID,
U.OVER_LIMIT_DATE,
U.MODIFIED,
abon.MODIFIED as abonent_modified
from USERS U
-- left join ABONENTS ABON on U.ABONENT_ID = ABON.ID
where ((U.IP = '127.0.0.1' or U.IP is null) and(u.id=1 or 1 is null or 1 = -1))
and (abon.deleted=0 or abon.deleted is null)
and U.IS_TEMPLATE <> 1;
select * from actor limit 10 OFFSET 20;
select * from users where id in (1,2,3,4) LIMIT 2;
select * from users where id between 19 and random();
select actor_id between 19 and 19 from actor where actor_id between 19 and random();
select * from staff join actor ON actor.actor_id BETWEEN 10 and 20; -- sqlite valid :O
select * from users join abonents join attributes join u_attributes join a_attributes;
select * from users left join abonents ON abonents.id = users.abonent_id;
select * from users u left join abonents ON a.id = u.abonent_id;