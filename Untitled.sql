CREATE TABLE `device` (
  `id` int,
  `name` int,
  `user_id` int
);

CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `full_name` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `pump` (
  `id` int PRIMARY KEY,
  `time_stamp` timestamp,
  `signal` bool,
  `device_id` int
);

ALTER TABLE `device` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `pump` ADD FOREIGN KEY (`device_id`) REFERENCES `users` (`id`);
