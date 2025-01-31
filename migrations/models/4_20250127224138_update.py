from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `bill_item` ALTER COLUMN `payment_method` SET DEFAULT 'credit';
        ALTER TABLE `bill_item` MODIFY COLUMN `payment_method` VARCHAR(6) NOT NULL  COMMENT '结算方式' DEFAULT 'credit';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `bill_item` MODIFY COLUMN `payment_method` VARCHAR(6)   COMMENT '结算方式';
        ALTER TABLE `bill_item` ALTER COLUMN `payment_method` DROP DEFAULT;"""
