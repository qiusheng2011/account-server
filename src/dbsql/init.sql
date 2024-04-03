-- 创建数据库
CREATE DATABASE IF NOT EXISTS tts CHARACTER
SET = "utf8mb4" COLLATE = "utf8mb4_bin" COMMENT = "TTS";
Use tts;
-- 账户表
CREATE TABLE IF NOT EXISTS `accounts` (
    `aid` INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT "账户内在id",
    `email` VARCHAR (50) NOT NULL UNIQUE KEY COMMENT "账户email",
    `account_name` VARCHAR (50) NOT NULL UNIQUE KEY COMMENT "账户名称",
    `hash_password` CHAR (64) NOT NULL COMMENT "账户密码hash值",
    `register_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT "注册时间",
    'activation' int(1) DEFAULT 0 COMMENT "激活状态",
) ENGINE = InnoDB COMMENT "账户表";
-- 账户凭证表
CREATE TABLE IF NOT EXISTS `accounts_certificate_token` (
    `aid` int(10) unsigned NOT NULL,
    `token` char(64) NOT NULL,
    `refresh_token` char(64) NOT NULL,
    PRIMARY KEY (`aid`),
    UNIQUE KEY `token` (`token`),
    UNIQUE KEY `refresh_token` (`refresh_token`),
    CONSTRAINT `act_ibaid_1` FOREIGN KEY (`aid`) REFERENCES `accounts` (`aid`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = InnoDB COMMENT = "账户凭证表";