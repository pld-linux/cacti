-- 
-- Table structure for table `plugin_config`
-- 

CREATE TABLE `plugin_config` (
  `id` int(8) NOT NULL auto_increment,
  `directory` varchar(32) NOT NULL default '',
  `name` varchar(64) NOT NULL default '',
  `status` tinyint(2) NOT NULL default '0',
  `author` varchar(64) NOT NULL default '',
  `webpage` varchar(255) NOT NULL default '',
  `version` varchar(8) NOT NULL default '',
  PRIMARY KEY  (`id`),
  KEY `status` (`status`),
  KEY `directory` (`directory`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `plugin_hooks`
-- 

CREATE TABLE `plugin_hooks` (
  `id` int(8) NOT NULL auto_increment,
  `name` varchar(32) NOT NULL default '',
  `hook` varchar(64) NOT NULL default '',
  `file` varchar(255) NOT NULL default '',
  `function` varchar(128) NOT NULL default '',
  `status` int(8) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `hook` (`hook`),
  KEY `status` (`status`)
) TYPE=MyISAM;

-- --------------------------------------------------------

-- 
-- Table structure for table `plugin_realms`
-- 

CREATE TABLE `plugin_realms` (
  `id` int(8) NOT NULL auto_increment,
  `plugin` varchar(32) NOT NULL default '',
  `file` text NOT NULL,
  `display` varchar(64) NOT NULL default '',
  PRIMARY KEY  (`id`),
  KEY `plugin` (`plugin`)
) TYPE=MyISAM;


CREATE TABLE `plugin_db_changes` (
  `id` int(10) NOT NULL auto_increment,
  `plugin` varchar(16) NOT NULL default '',
  `table` varchar(64) NOT NULL default '',
  `column` varchar(64) NOT NULL,
  `method` varchar(16) NOT NULL default '',
  PRIMARY KEY  (`id`),
  KEY `plugin` (`plugin`),
  KEY `method` (`method`)
) TYPE=MyISAM;


REPLACE INTO `plugin_realms` VALUES (1, 'internal', 'plugins.php', 'Plugin Management');
INSERT INTO `plugin_hooks` VALUES (1, 'internal', 'config_arrays', '', 'plugin_config_arrays', 1);
INSERT INTO `plugin_hooks` VALUES (2, 'internal', 'draw_navigation_text', '', 'plugin_draw_navigation_text', 1);
