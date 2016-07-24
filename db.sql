drop database if exists web_analyse;
create database web_analyse;
use web_analyse;
drop table if exists web_analyse;
CREATE TABLE `web_analyse` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ip` bigint(32) NOT NULL,
  `time` bigint(32) not null,
  `total_time` int(11) NOT NULL,
  `visit_count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `analyse_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8