USE app;

--------------------------------------------------------------------- CATEGORY
-- CREATE TABLE `category`(
--   `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
--   `user_id` INT(10) UNSIGNED NOT NULL DEFAULT 1, -- TODO: assign instead of default.
--   `name` VARCHAR(50),
--   `description` VARCHAR(255),
--   `createTime` DATETIME NOT NULL DEFAULT NOW(),
--   `updateTime` DATETIME NOT NULL DEFAULT NOW(), -- TODO: assign instead of default.
--   PRIMARY KEY (`id`),
--   FOREIGN KEY (`user_id`) REFERENCES `user`(`id`)
-- );

INSERT INTO `category`(`name`, `description`)
  VALUES
    ("Coffee tables","A coffee table is a low table designed to be placed in a sitting area for convenient support of beverages, remote controls, magazines, books, decorative objects, and other small items."),
    ("Side tables"," Just as its name suggests, a side table is placed beside a piece of furniture a person would sit on, such as a couch or a bed. Its main purpose is to ensure that essential items are within easy reach."),
    ("Sideboards","A sideboard is a long cupboard which is about the same height as a table. Sideboards are usually kept in dining rooms to put plates and glasses in. "),
    ("Bookcases and shelves","A bookcase is a piece of furniture with shelves that you keep books on."),
    ("TV cabinets","A tv cabinet is a  cabinet on which a television set is placed or in which it is encased."),
    ("Armchairs","An armchair is a comfortable, cushioned chair with a support on each side, where you can rest your arms while you sit."),
    ("sofas","A sofa is a long, comfortable seat with a back and usually with arms, which two or three people can sit on.")
  ;

---------------------------------------------------------------------- PRODUCT
-- CREATE TABLE `product`(
--   `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
--   `user_id` INT(10) UNSIGNED NOT NULL DEFAULT 1, -- TODO: assign instead of default.
--   `category_id` INT(10) UNSIGNED NOT NULL DEFAULT 1, -- TODO: assign instead of default.
--   `name` VARCHAR(100),
--   `description` VARCHAR(255),
--   `reference` VARCHAR(255),
--   `price` FLOAT(24),
--   `quantity` INT(10),
--   `createTime` DATETIME NOT NULL DEFAULT NOW(),
--   `updateTime` DATETIME NOT NULL DEFAULT NOW(), -- TODO: assign instead of default.
--   PRIMARY KEY (`id`),
--   FOREIGN KEY (`user_id`) REFERENCES `user`(`id`),
--   FOREIGN KEY (`category_id`) REFERENCES `category`(`id`)
-- );

INSERT INTO `product`(`category_id`, `name`, `description`, `reference`, `price`, `quantity`)
  VALUES
    (1,"Coffee table with double top","Recycled teak teel- brown - 120 x 35 cm","ref12345678",789.99,12),
    (1,"Coffee table with double top shell","Recycled teak wood - brown and black - Ø 100 cm - H 35 cm","ref87654321",549.99,8),
    (1,"Jonas oval coffee table","Aluminium - golden color - 150 x 60 x 40 cm","ref43215678",649.99,7),
    (1,"Alida round coffee table","Recycled teak with nitrocellulose varnish - 110 x 110 x 36 cm","ref42514260",569.99,5),
    (1,"Square coffee table with shelves","Recycled teak, acacia and  metal - 100 x 100 x 40 cm","ref93360760",549.99,5),
    (1,"Laly round coffee table","Teak and steel - Ø 90 cm - H 47 cm","ref97990934",349.99,5),
    (1,"Coffee table with shell Alida","Recycled teak - 60 x 60 x 34.5 cm","ref56781234",199.99,5),
    (1,"Double top coffee table","Recycled teak - brown - 80 x 35 cm","ref88780497",429.99,7),
    (1,"Round coffee table","Recycled pine - brown - 90 x 32 cm","ref82031924",349.99,0),
    (1,"Natural color coffee table with 4 drawers","Brown - 140 x 70 x 44 cm","ref94570950",649.99,21),
    (1,"Robin square coffee table","Mango tree and metal - 87.5 x 80 x 40 cm","ref63977760",249.99,7),
    (2,"Side table 1 drawer 1 shelf Alida","teak and metal - 47 x 35 x 51.3 cm","ref60121944",239.99,7),
    (2,"2 Jonas side tables","Aluminium and metal - H : 47,5/36 cm","ref7972483",169.99,7),
    (2,"Laly side table","Teak and steel - 60 x 56 x 49 cm","ref14222613",99.99,0),
    (2,"Round side table","Steel and recycled wood - Ø 42 cm - H 49 cm","ref70825737",119.99,8),
    (2,"Square side table","Metal and glass - 45.5 x 45.5 cm","ref74604530",119.99,12),
    (2,"Robin side table","Mango wood and metal - - 52,5 x 45 x 61 cm","ref26218465",139.99,9),
    (2,"Jonas round side table","Aluminum - golden color - Ø: 43 cm, H: 48 cm","ref27167127",159.99,13),
    (3,"Emilio sideboard","Black - 75 x 38 x 85.5 cm","ref60218741",679.99,4),
    (3,"Sideboard 4 doors 1 shelf","Brown - 178 x 40 x 91 cm","ref31592034",1399.99,5),
    (3,"Phuket sideboard","Mango wood - 160 x 45 x 85 cm","ref36006957",899.99,6),
    (3,"Scandinavian sideboard","Fir tree - beige - 85 x 91 x 28.4 cm","ref82625340",599.99,1),
    (4,"Alida 6 Tier Shelving Unit","Teak and metal - 120 x 40 x 180.5 cm","ref88564606",1199.99,10),
    (4,"Alida 1 Drawer Shelf","Teak and metal - 120 x 40 x 180.5 cm","ref49939103",1199.99,10),
    (4,"Wall shelf S","Recycled teak - brown - 35 x 35 x 25.3 cm","ref98452116",59.99,10),
    (4,"Alida 6 Tier Bookcase","Teak,acasia and metal - 120 x 40 x 180 cm","ref48737609",1149.99,10),
    (4,"Sistine wall shelf","Recycled teak - brown - 75 x 15 x 15 cm","ref64161487",79.99,8),
    (4,"Haby wine bottle rack","metal - 70 x 6,5 x 160 cm","ref46152693",229.99,17),
    (4,"Robin bookcase","Recycled pine and metal - brown -  99 x 190 x 40 cm","ref22000887",1299.99,22),
    (4,"Alida 4 Tier Pyramid Shelf","Recycled teak and metal - 140 x 40 x 145,5 cm","ref52466044",1399.99,14),
    (5,"Natural color TV stand with 2 sliding doors","Poplar/Glass/Steel - brown - 180 x 40 x 50 cm","ref68795161",649.99,12),
    (5,"6-drawer TV cabinet","recycled pine - brown - 180,5 x 45 x 55 cm","ref56923055",539.99,17),
    (5,"Alida Rotating TV Stand","Recycled teak - 100 x 40 x 45 cm","ref76613351",649.99,4),
    (5,"Emilio 3-Drawer TV Unit","Black- 120 x 40 x 40 cm","ref64737720",249.99,8),
    (5,"Scandinavian TV cabinet","Tree - beige - 131 x 58 x 27.9 cm","ref27303577",579.99,6),
    (5,"Robin 2-Shelf TV Unit","Metal- 140 x 45 x 55,5 cm","ref9476689",949.99,4),
    (6,"Chesterfield armchair","Cow leather and oak - brown - 117 x 73 x 100 cm","ref66774516",1249.99,21),
    (7,"Rome 2 seater sofa","velvet - brown - 149 x 84 x 76 cm","ref26776503",679.99,8),
    (7,"Chesterfield 3 seater sofa","cow leather and oak - brown - 247 x 73 x 99 cm","ref29180976",1249.99,4) 
  ;
