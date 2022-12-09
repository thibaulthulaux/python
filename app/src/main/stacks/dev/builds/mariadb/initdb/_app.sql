SET time_zone = '+00:00';

-- Create application database
USE app;
-------------------------------------------------------------------------- USER
CREATE TABLE `user`(
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `title` VARCHAR(10),
    `firstName` VARCHAR(50),
    `lastName` VARCHAR(50),
    `company` VARCHAR(255),
    `address` VARCHAR(255),
    `city` VARCHAR(255),
    `postalCode` VARCHAR(255),
    `country` VARCHAR(255),
    `phone` VARCHAR(255),
    `valid` BIT(1) DEFAULT 0, -- TODO: assign instead of default.
    `validationUid` VARCHAR(255),
    `validationTimeout` DATETIME,
    -- `validationTimeout` DATETIME NOT NULL DEFAULT NOW() + INTERVAL 1 HOUR,
    `createTime` DATETIME NOT NULL DEFAULT NOW(),
    `updateTime` DATETIME NOT NULL DEFAULT NOW(), -- TODO: assign instead of default.
    PRIMARY KEY (`id`)
);

INSERT INTO `user`(`email`,`password`,`title`,`firstName`,`lastName`,`company`,`address`,`city`,`postalCode`,`country`,`phone`)
  VALUES
    ("admin",SHA2("admin",512),"Title","admin","Last name","Admin Company","Address","City","Postal code","Country","Phone"),
    ("user",SHA2("user",512),"Title","user","Last name","User Company","Address","City","Postal code","Country","Phone"),
    ("donald.duck@mail.com",SHA2("donald",512),"M.","Donald","Duck","Acme Company","66 Route 66","Dreamland","67000","France","0606060606")
  ;

-------------------------------------------------------------------------- ROLE
CREATE TABLE `role`(
    `id` INT(10) UNSIGNED NOT NULL,
    `name` VARCHAR(80) NOT NULL UNIQUE,
    PRIMARY KEY (`id`)
);

INSERT INTO `role`(`id`,`name`)
  VALUES
    ("1","admin"),
    ("2","user")
  ;

--------------------------------------------------------------------- USER_ROLE
CREATE TABLE `user_role`(
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` INT(10) UNSIGNED NOT NULL,
    `role_id` INT(10) UNSIGNED NOT NULL DEFAULT 2, -- default to user role
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`id`),
    FOREIGN KEY (`role_id`) REFERENCES `role`(`id`)
);

INSERT INTO `user_role`(`user_id`,`role_id`)
  VALUES
    (1,1), -- admin(1):admin
    (1,2), -- admin(1):user
    (2,2) -- user(2):user
  ;

---------------------------------------------------------------------- CATEGORY
CREATE TABLE `category`(
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT(10) UNSIGNED NOT NULL DEFAULT 2, -- TODO: assign instead of default.
  `name` VARCHAR(50),
  `description` VARCHAR(255),
  `createTime` DATETIME NOT NULL DEFAULT NOW(),
  `updateTime` DATETIME NOT NULL DEFAULT NOW(), -- TODO: assign instead of default.
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
);

----------------------------------------------------------------------- PRODUCT
CREATE TABLE `product`(
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT(10) UNSIGNED NOT NULL DEFAULT 2, -- TODO: assign instead of default.
  `category_id` INT(10) UNSIGNED NOT NULL DEFAULT 1, -- TODO: assign instead of default.
  `name` VARCHAR(100),
  `description` VARCHAR(255),
  `reference` VARCHAR(255),
  `price` FLOAT(24),
  `quantity` INT(10),
  `createTime` DATETIME NOT NULL DEFAULT NOW(),
  `updateTime` DATETIME NOT NULL DEFAULT NOW(), -- TODO: assign instead of default.
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `user`(`id`),
  FOREIGN KEY (`category_id`) REFERENCES `category`(`id`)
);
