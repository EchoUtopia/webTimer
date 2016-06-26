drop database if exists web_analyse;
create database web_analyse;
use web_analyse;
drop table if exists web_analyse;
CREATE TABLE `web_analyse` (
  `user_id` bigint not null,
  `ip` bigint(32) NOT NULL,
  `time` bigint(24) not null,
  `total_time` smallint NOT NULL,
  `visit_count` int(11) NOT NULL,
  PRIMARY KEY (`time`),
  KEY `analyse_user` (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8