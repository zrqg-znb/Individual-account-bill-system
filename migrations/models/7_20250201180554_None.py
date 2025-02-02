from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `api` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `path` VARCHAR(100) NOT NULL  COMMENT 'API路径',
    `method` VARCHAR(6) NOT NULL  COMMENT '请求方法',
    `summary` VARCHAR(500) NOT NULL  COMMENT '请求简介',
    `tags` VARCHAR(100) NOT NULL  COMMENT 'API标签',
    KEY `idx_api_created_78d19f` (`created_at`),
    KEY `idx_api_updated_643c8b` (`updated_at`),
    KEY `idx_api_path_9ed611` (`path`),
    KEY `idx_api_method_a46dfb` (`method`),
    KEY `idx_api_summary_400f73` (`summary`),
    KEY `idx_api_tags_04ae27` (`tags`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `auditlog` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL  COMMENT '用户ID',
    `username` VARCHAR(64) NOT NULL  COMMENT '用户名称' DEFAULT '',
    `module` VARCHAR(64) NOT NULL  COMMENT '功能模块' DEFAULT '',
    `summary` VARCHAR(128) NOT NULL  COMMENT '请求描述' DEFAULT '',
    `method` VARCHAR(10) NOT NULL  COMMENT '请求方法' DEFAULT '',
    `path` VARCHAR(255) NOT NULL  COMMENT '请求路径' DEFAULT '',
    `status` INT NOT NULL  COMMENT '状态码' DEFAULT -1,
    `response_time` INT NOT NULL  COMMENT '响应时间(单位ms)' DEFAULT 0,
    KEY `idx_auditlog_created_cc33d0` (`created_at`),
    KEY `idx_auditlog_updated_2f871f` (`updated_at`),
    KEY `idx_auditlog_user_id_4b93fa` (`user_id`),
    KEY `idx_auditlog_usernam_b187b3` (`username`),
    KEY `idx_auditlog_module_04058b` (`module`),
    KEY `idx_auditlog_summary_3e27da` (`summary`),
    KEY `idx_auditlog_method_4270a2` (`method`),
    KEY `idx_auditlog_path_b99502` (`path`),
    KEY `idx_auditlog_status_2a72d2` (`status`),
    KEY `idx_auditlog_respons_8caa87` (`response_time`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `dept` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(20) NOT NULL UNIQUE COMMENT '部门名称',
    `desc` VARCHAR(500)   COMMENT '备注',
    `is_deleted` BOOL NOT NULL  COMMENT '软删除标记' DEFAULT 0,
    `order` INT NOT NULL  COMMENT '排序' DEFAULT 0,
    `parent_id` INT NOT NULL  COMMENT '父部门ID' DEFAULT 0,
    KEY `idx_dept_created_4b11cf` (`created_at`),
    KEY `idx_dept_updated_0c0bd1` (`updated_at`),
    KEY `idx_dept_name_c2b9da` (`name`),
    KEY `idx_dept_is_dele_466228` (`is_deleted`),
    KEY `idx_dept_order_ddabe1` (`order`),
    KEY `idx_dept_parent__a71a57` (`parent_id`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `deptclosure` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `ancestor` INT NOT NULL  COMMENT '父代',
    `descendant` INT NOT NULL  COMMENT '子代',
    `level` INT NOT NULL  COMMENT '深度' DEFAULT 0,
    KEY `idx_deptclosure_created_96f6ef` (`created_at`),
    KEY `idx_deptclosure_updated_41fc08` (`updated_at`),
    KEY `idx_deptclosure_ancesto_fbc4ce` (`ancestor`),
    KEY `idx_deptclosure_descend_2ae8b1` (`descendant`),
    KEY `idx_deptclosure_level_ae16b2` (`level`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `menu` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(20) NOT NULL  COMMENT '菜单名称',
    `remark` JSON   COMMENT '保留字段',
    `menu_type` VARCHAR(7)   COMMENT '菜单类型',
    `icon` VARCHAR(100)   COMMENT '菜单图标',
    `path` VARCHAR(100) NOT NULL  COMMENT '菜单路径',
    `order` INT NOT NULL  COMMENT '排序' DEFAULT 0,
    `parent_id` INT NOT NULL  COMMENT '父菜单ID' DEFAULT 0,
    `is_hidden` BOOL NOT NULL  COMMENT '是否隐藏' DEFAULT 0,
    `component` VARCHAR(100) NOT NULL  COMMENT '组件',
    `keepalive` BOOL NOT NULL  COMMENT '存活' DEFAULT 1,
    `redirect` VARCHAR(100)   COMMENT '重定向',
    KEY `idx_menu_created_b6922b` (`created_at`),
    KEY `idx_menu_updated_e6b0a1` (`updated_at`),
    KEY `idx_menu_name_b9b853` (`name`),
    KEY `idx_menu_path_bf95b2` (`path`),
    KEY `idx_menu_order_606068` (`order`),
    KEY `idx_menu_parent__bebd15` (`parent_id`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `role` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(20) NOT NULL UNIQUE COMMENT '角色名称',
    `desc` VARCHAR(500)   COMMENT '角色描述',
    KEY `idx_role_created_7f5f71` (`created_at`),
    KEY `idx_role_updated_5dd337` (`updated_at`),
    KEY `idx_role_name_e5618b` (`name`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `username` VARCHAR(20) NOT NULL UNIQUE COMMENT '用户名称',
    `alias` VARCHAR(30)   COMMENT '姓名',
    `email` VARCHAR(255) NOT NULL UNIQUE COMMENT '邮箱',
    `phone` VARCHAR(20)   COMMENT '电话',
    `password` VARCHAR(128)   COMMENT '密码',
    `is_active` BOOL NOT NULL  COMMENT '是否激活' DEFAULT 1,
    `is_superuser` BOOL NOT NULL  COMMENT '是否为超级管理员' DEFAULT 0,
    `last_login` DATETIME(6)   COMMENT '最后登录时间',
    `dept_id` INT   COMMENT '部门ID',
    KEY `idx_user_created_b19d59` (`created_at`),
    KEY `idx_user_updated_dfdb43` (`updated_at`),
    KEY `idx_user_usernam_9987ab` (`username`),
    KEY `idx_user_alias_6f9868` (`alias`),
    KEY `idx_user_email_1b4f1c` (`email`),
    KEY `idx_user_phone_4e3ecc` (`phone`),
    KEY `idx_user_is_acti_83722a` (`is_active`),
    KEY `idx_user_is_supe_b8a218` (`is_superuser`),
    KEY `idx_user_last_lo_af118a` (`last_login`),
    KEY `idx_user_dept_id_d4490b` (`dept_id`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `bill` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `status` VARCHAR(6) NOT NULL  COMMENT '账单状态' DEFAULT 'unpaid',
    `remark` LONGTEXT   COMMENT '备注',
    `total_amount` DECIMAL(10,2) NOT NULL  COMMENT '总金额',
    `paid_amount` DECIMAL(10,2) NOT NULL  COMMENT '已支付金额' DEFAULT 0,
    `owner_id` BIGINT NOT NULL COMMENT '所属用户',
    CONSTRAINT `fk_bill_user_346e3521` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    KEY `idx_bill_created_9ab937` (`created_at`),
    KEY `idx_bill_updated_9b8bad` (`updated_at`),
    KEY `idx_bill_status_cb6f45` (`status`),
    KEY `idx_bill_owner_i_0ee6e8` (`owner_id`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `bill_item` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `product_name` VARCHAR(100) NOT NULL  COMMENT '商品名称',
    `price` DECIMAL(10,2) NOT NULL  COMMENT '商品价格',
    `quantity` DECIMAL(10,2) NOT NULL  COMMENT '商品数量',
    `unit` VARCHAR(20) NOT NULL  COMMENT '商品单位',
    `purchase_time` DATETIME(6) NOT NULL  COMMENT '购买时间',
    `buyer_name` VARCHAR(50) NOT NULL  COMMENT '购买人姓名',
    `status` VARCHAR(8) NOT NULL  COMMENT '商品状态' DEFAULT 'unpaid',
    `payment_method` VARCHAR(6) NOT NULL  COMMENT '结算方式' DEFAULT 'credit',
    `settler_name` VARCHAR(50)   COMMENT '结算人姓名',
    `remark` LONGTEXT   COMMENT '备注',
    `amount` DECIMAL(10,2) NOT NULL  COMMENT '商品总金额',
    `paid_amount` DECIMAL(10,2) NOT NULL  COMMENT '已支付金额' DEFAULT 0,
    `bill_id` BIGINT NOT NULL COMMENT '所属账单',
    CONSTRAINT `fk_bill_ite_bill_0b637ede` FOREIGN KEY (`bill_id`) REFERENCES `bill` (`id`) ON DELETE CASCADE,
    KEY `idx_bill_item_created_44b7dc` (`created_at`),
    KEY `idx_bill_item_updated_c0638e` (`updated_at`),
    KEY `idx_bill_item_product_73b06b` (`product_name`),
    KEY `idx_bill_item_purchas_115c73` (`purchase_time`),
    KEY `idx_bill_item_buyer_n_66fa3a` (`buyer_name`),
    KEY `idx_bill_item_status_710116` (`status`),
    KEY `idx_bill_item_settler_1cc1be` (`settler_name`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `role_menu` (
    `role_id` BIGINT NOT NULL,
    `menu_id` BIGINT NOT NULL,
    FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `role_api` (
    `role_id` BIGINT NOT NULL,
    `api_id` BIGINT NOT NULL,
    FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`api_id`) REFERENCES `api` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user_role` (
    `user_id` BIGINT NOT NULL,
    `role_id` BIGINT NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
