### Creating the Database

(optionally, rm ../db.sqlite to start fresh)

sqlite3 ../db.sqlite

.read 01.create_lists.sql 
.read 02.create_items.sql 
.read 03.insert_lists.sql 
.read 04.insert_items.sql 

select * from lists;
select * from items;
select * from items i, lists l where i.listname = l.name;

(read those SQL files yourself to see the schema and sample data)
