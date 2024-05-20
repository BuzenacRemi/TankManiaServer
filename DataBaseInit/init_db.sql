-- Création de la table user
CREATE TABLE "user" (
    id          SERIAL PRIMARY KEY,
    username    VARCHAR(16) NOT NULL,
    hashed_pass VARCHAR NOT NULL,
    uuid        UUID NOT NULL UNIQUE
);

-- Création de la table rank
CREATE TABLE rank (
  id SERIAL PRIMARY KEY,
  uuid_player UUID NOT NULL UNIQUE,
  value INTEGER NOT NULL,
  FOREIGN KEY (uuid_player) REFERENCES "user"(uuid)
);

-- Création de la table session
CREATE TABLE session (
  id SERIAL PRIMARY KEY,
  uuid_player UUID NOT NULL,
  session_key VARCHAR(255) UNIQUE NOT NULL,
  expiration_date TIMESTAMP WITH TIME ZONE NOT NULL,
  FOREIGN KEY (uuid_player) REFERENCES "user"(uuid)
);

-- Création de la table game_history
CREATE TABLE game_history (
  id SERIAL PRIMARY KEY,
  uuid_player1 UUID NOT NULL,
  uuid_player2 UUID NOT NULL,
  uuid_winner UUID,
  FOREIGN KEY (uuid_player1) REFERENCES "user"(uuid),
  FOREIGN KEY (uuid_player2) REFERENCES "user"(uuid),
  FOREIGN KEY (uuid_winner) REFERENCES "user"(uuid)
);

-- Création de la table game_stats
CREATE TABLE game_stats (
  id SERIAL PRIMARY KEY,
  id_game INTEGER NOT NULL,
  uuid_player UUID NOT NULL,
  success_missiles INTEGER NOT NULL,
  missiles_launched INTEGER NOT NULL,
  damages_received INTEGER NOT NULL,
  movement_distance INTEGER NOT NULL,
  FOREIGN KEY (id_game) REFERENCES game_history(id),
  FOREIGN KEY (uuid_player) REFERENCES "user"(uuid)
);

create user api with password 'Passw0rd';
GRANT pg_read_all_data TO api;
GRANT pg_write_all_data TO api;