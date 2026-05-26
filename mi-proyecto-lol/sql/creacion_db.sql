CREATE DATABASE lol_ranked_s15;
USE lol_ranked_s15;

-- Tabla de organizaciones/equipos
CREATE TABLE Teams (
    team_id INT PRIMARY KEY AUTO_INCREMENT,
    team_name VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de campeones
CREATE TABLE Champions (
    champion_id INT PRIMARY KEY,
    champion_name VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla de partidas
CREATE TABLE Games (
    game_id BIGINT PRIMARY KEY,
    start_utc DATETIME NOT NULL,
    duration INT NOT NULL CHECK (duration > 0),
    queue VARCHAR(50) NOT NULL,
    platform_id VARCHAR(10) NOT NULL,
    map_id INT NOT NULL,
    game_mode VARCHAR(20) NOT NULL,
    game_version VARCHAR(50) NOT NULL
);

-- Relación partida-equipo con side
CREATE TABLE GameTeams (
    game_id BIGINT NOT NULL,
    team_id INT NOT NULL,
    side ENUM('BLUE','RED') NOT NULL,
    PRIMARY KEY (game_id, side),
    FOREIGN KEY (game_id) REFERENCES Games(game_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES Teams(team_id) ON DELETE CASCADE
);

-- Jugadores en partida
CREATE TABLE Participants (
    participant_id INT NOT NULL CHECK (participant_id BETWEEN 1 AND 10),
    game_id BIGINT NOT NULL,
    champion_id INT NOT NULL,
    team_id INT NOT NULL,
    side ENUM('BLUE','RED') NOT NULL,
    position ENUM('TOP','JUNGLE','MIDDLE','BOTTOM','UTILITY'),
    win BOOLEAN NOT NULL,
    kills INT DEFAULT 0,
    deaths INT DEFAULT 0,
    assists INT DEFAULT 0,
    kda_ratio FLOAT,
    kill_participation FLOAT,
    gold_earned INT DEFAULT 0,
    gold_spent INT DEFAULT 0,
    gold_per_min FLOAT,
    damage_dealt INT DEFAULT 0,
    damage_per_min FLOAT,
    damage_to_champ INT DEFAULT 0,
    damage_champ_per_min FLOAT,
    damage_taken INT DEFAULT 0,
    vision_score INT DEFAULT 0,
    item0 VARCHAR(100),
    item1 VARCHAR(100),
    item2 VARCHAR(100),
    item3 VARCHAR(100),
    item4 VARCHAR(100),
    item5 VARCHAR(100),
    item6 VARCHAR(100),
    solo_tier VARCHAR(20),
    solo_rank VARCHAR(10),
    solo_lp INT DEFAULT 0,
    solo_wins INT DEFAULT 0,
    solo_losses INT DEFAULT 0,
    flex_tier VARCHAR(20),
    flex_rank VARCHAR(10),
    flex_lp INT DEFAULT 0,
    flex_wins INT DEFAULT 0,
    flex_losses INT DEFAULT 0,
    mastery_level INT DEFAULT 0,
    mastery_points INT DEFAULT 0,
    mastery_lastPlayTime DATETIME,
    mastery_pointsSinceLastLevel INT DEFAULT 0,
    mastery_pointsUntilNextLevel INT DEFAULT 0,
    mastery_tokens INT DEFAULT 0,
    final_abilityHaste INT DEFAULT 0,
    final_abilityPower INT DEFAULT 0,
    final_armor INT DEFAULT 0,
    final_attackDamage INT DEFAULT 0,
    final_attackSpeed FLOAT DEFAULT 0,
    final_movementSpeed INT DEFAULT 0,
    final_health INT DEFAULT 0,
    final_healthMax INT DEFAULT 0,
    final_lifesteal INT DEFAULT 0,
    final_omnivamp INT DEFAULT 0,
    final_power INT DEFAULT 0,
    final_powerMax INT DEFAULT 0,
    final_spellVamp INT DEFAULT 0,
    PRIMARY KEY (game_id, participant_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id) ON DELETE CASCADE,
    FOREIGN KEY (champion_id) REFERENCES Champions(champion_id) ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (game_id, side) REFERENCES GameTeams(game_id, side)
);

-- Estadísticas globales por equipo en la partida
CREATE TABLE TeamStats (
    game_id BIGINT NOT NULL,
    team_id INT NOT NULL,
    side ENUM('BLUE','RED') NOT NULL,
    baron_kills INT DEFAULT 0,
    dragon_kills INT DEFAULT 0,
    tower_kills INT DEFAULT 0,
    champ_kills INT DEFAULT 0,
    riftHerald_kills INT DEFAULT 0,
    inhibitor_kills INT DEFAULT 0,
    PRIMARY KEY (game_id, side),
    FOREIGN KEY (game_id, side) REFERENCES GameTeams(game_id, side),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);
