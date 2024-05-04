-- Backfill existing data in the nickname column
UPDATE users
SET nickname = 'my_nickname'
WHERE nickname IS NULL;

-- Alter the nickname column to set it to NOT NULL
ALTER users
ALTER COLUMN nickname SET NOT NULL;


