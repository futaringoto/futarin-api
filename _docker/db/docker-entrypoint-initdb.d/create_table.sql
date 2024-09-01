USE futaringoto_db;

DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `raspis`;
DROP TABLE IF EXISTS `groups`;
DROP TABLE IF EXISTS `texts`;
DROP TABLE IF EXISTS `messages`;

CREATE TABLE `users` (
    `id` CHAR(36),
    `username` VARCHAR(20),
    `raspi_id` CHAR(36),
    `group_id` CHAR(36),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`raspi_id`) REFERENCES raspis (`id`),
    FOREIGN KEY (`group_id`) REFERENCES groups (`id`)
);

CREATE TABLE `raspis` (
    `id` CHAR(36),
    `mac_address` CHAR(17),
    PRIMARY KEY (`id`)
);

CREATE TABLE `groups` (
    `id` CHAR(36),
    `uuid_1` CHAR(36),
    `uuid_2` CHAR(36),
    PRIMARY KEY (id),
    FOREIGN KEY (`uuid_1`) REFERENCES users (`id`),
    FOREIGN KEY (`uuid_2`) REFERENCES users (`id`)
);

CREATE TABLE texts (
    `id` CHAR(36),
    `uuid` CHAR(36),
    `prompt` VARCHAR(1000),
    `generated_text` VARCHAR(1000),
    `created_at` DATE,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`uuid`) REFERENCES users (`id`)
);

CREATE TABLE messages (
    `id` CHAR(36),
    `uuid` CHAR(36),
    `send_message` VARCHAR(1000),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`uuid`) REFERENCES users (`id`)
);