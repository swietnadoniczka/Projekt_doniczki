CREATE TABLE `users` (
  `id` integer,
  `full_name` varchar(255)
);

CREATE TABLE `device` (
  `id` integer PRIMARY KEY,
  `name` varchar(255),
  `user_id` integer
);

CREATE TABLE `pump` (
  `id` integer PRIMARY KEY,
  `water_time` integer,
  `dane` bool,
  `start_time` datetime,
  `stop_time` datetime,
  `device_id` integer,
  `temperature` integer,
  `humidity` integer,
  `czy_wlano` integer,
  `czy_wylano` integer,
  `stop` integer
);

ALTER TABLE `device` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `pump` ADD FOREIGN KEY (`device_id`) REFERENCES `device` (`id`);
