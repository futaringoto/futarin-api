DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `raspis`;
DROP TABLE IF EXISTS `groups`;
DROP TABLE IF EXISTS `texts`;
DROP TABLE IF EXISTS `messages`;

CREATE TABLE users (
    uuid CHAR(36),
    username VARCHAR(20),
    raspi_id CHAR(36),
    group_id CHAR(36),
    PRIMARY KEY (uuid),
    FOREIGN KEY (raspi_id) REFERENCES raspis (raspi_id),
    FOREIGN KEY (group_id) REFERENCES groups (group_id)
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE raspis (
    raspi_id CHAR(36),
    mac_address CHAR(17),
    PRIMARY KEY (raspi_id)
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE groups (
    group_id CHAR(36),
    uuid_1 CHAR(36),
    uuid_2 CHAR(36),
    PRIMARY KEY (group_id),
    FOREIGN KEY (uuid_1) REFERENCES users (uuid),
    FOREIGN KEY (uuid_2) REFERENCES users (uuid)
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE texts (
    text_id CHAR(36),
    uuid CHAR(36),
    prompt VARCHAR(1000),
    generated_text VARCHAR(1000),
    created_at DATE,
    PRIMARY KEY (text_id),
    FOREIGN KEY (uuid) REFERENCES users (uuid)
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE messages (
    message_id CHAR(36),
    uuid CHAR(36),
    send_message VARCHAR(1000),
    PRIMARY KEY (message_id),
    FOREIGN KEY (uuid) REFERENCES users (uuid)
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;