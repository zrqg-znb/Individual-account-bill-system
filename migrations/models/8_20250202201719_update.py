from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `bill_item` ADD `settle_time` DATETIME(6)   COMMENT '结算时间';
        ALTER TABLE `bill_item` ADD INDEX `idx_bill_item_settle__01e83a` (`settle_time`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `bill_item` DROP INDEX `idx_bill_item_settle__01e83a`;
        ALTER TABLE `bill_item` DROP COLUMN `settle_time`;"""
