-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.0.17-nt - MySQL Community Edition (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for facebvotingweb
CREATE DATABASE IF NOT EXISTS `facebvotingweb` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `facebvotingweb`;

-- Dumping structure for table facebvotingweb.candidates
CREATE TABLE IF NOT EXISTS `candidates` (
  `id` int(11) NOT NULL auto_increment,
  `cname` varchar(150) NOT NULL default '0',
  `party` varchar(150) NOT NULL default '0',
  `symbol` varchar(150) NOT NULL default '0',
  `cid` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_candidates_constituencies` (`cid`),
  CONSTRAINT `FK_candidates_constituencies` FOREIGN KEY (`cid`) REFERENCES `constituencies` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table facebvotingweb.candidates: ~2 rows (approximately)
/*!40000 ALTER TABLE `candidates` DISABLE KEYS */;
INSERT INTO `candidates` (`id`, `cname`, `party`, `symbol`, `cid`) VALUES
	(1, 'yeddyurappa', 'bjp', 'bjp.jpg', 1),
	(2, 'siddharamayya', 'congress', 'congress.png', 1);
/*!40000 ALTER TABLE `candidates` ENABLE KEYS */;

-- Dumping structure for table facebvotingweb.constituencies
CREATE TABLE IF NOT EXISTS `constituencies` (
  `id` int(11) NOT NULL auto_increment,
  `consname` varchar(150) NOT NULL default '0',
  `status` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table facebvotingweb.constituencies: ~2 rows (approximately)
/*!40000 ALTER TABLE `constituencies` DISABLE KEYS */;
INSERT INTO `constituencies` (`id`, `consname`, `status`) VALUES
	(1, 'shivamogga', 'Active'),
	(2, 'mandya', 'Active');
/*!40000 ALTER TABLE `constituencies` ENABLE KEYS */;

-- Dumping structure for table facebvotingweb.eauthority
CREATE TABLE IF NOT EXISTS `eauthority` (
  `id` int(11) NOT NULL auto_increment,
  `userid` varchar(150) NOT NULL default '0',
  `pass` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table facebvotingweb.eauthority: ~1 rows (approximately)
/*!40000 ALTER TABLE `eauthority` DISABLE KEYS */;
INSERT INTO `eauthority` (`id`, `userid`, `pass`) VALUES
	(1, 'abc123', '123');
/*!40000 ALTER TABLE `eauthority` ENABLE KEYS */;

-- Dumping structure for table facebvotingweb.voters
CREATE TABLE IF NOT EXISTS `voters` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '0',
  `phone` varchar(150) NOT NULL default '0',
  `gender` varchar(150) NOT NULL default '0',
  `aadharid` varchar(150) NOT NULL default '0',
  `voterid` varchar(150) NOT NULL default '0',
  `cid` int(11) NOT NULL default '0',
  `pass` varchar(150) NOT NULL default '0',
  `status` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_voters_constituencies` (`cid`),
  CONSTRAINT `FK_voters_constituencies` FOREIGN KEY (`cid`) REFERENCES `constituencies` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table facebvotingweb.voters: ~1 rows (approximately)
/*!40000 ALTER TABLE `voters` DISABLE KEYS */;
INSERT INTO `voters` (`id`, `name`, `phone`, `gender`, `aadharid`, `voterid`, `cid`, `pass`, `status`) VALUES
	(1, 'abhi', '9632262392', 'Male', '123456789012', '1234567890', 1, '123', 'not voted');
/*!40000 ALTER TABLE `voters` ENABLE KEYS */;

-- Dumping structure for table facebvotingweb.votes
CREATE TABLE IF NOT EXISTS `votes` (
  `id` int(11) NOT NULL auto_increment,
  `cid` int(11) NOT NULL default '0',
  `votes` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_votes_candidates` (`cid`),
  CONSTRAINT `FK_votes_candidates` FOREIGN KEY (`cid`) REFERENCES `candidates` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table facebvotingweb.votes: ~2 rows (approximately)
/*!40000 ALTER TABLE `votes` DISABLE KEYS */;
INSERT INTO `votes` (`id`, `cid`, `votes`) VALUES
	(1, 1, 0),
	(2, 2, 0);
/*!40000 ALTER TABLE `votes` ENABLE KEYS */;

-- Dumping structure for trigger facebvotingweb.candidates_after_insert
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `candidates_after_insert` AFTER INSERT ON `candidates` FOR EACH ROW  BEGIN
insert into votes(cid,votes) values(new.id,0);
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
