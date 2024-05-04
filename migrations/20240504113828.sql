UPDATE users
SET nickname = 'my_nickname'
WHERE nickname IS NULL;
ALTER users
ALTER COLUMN nickname SET NOT NULL;


