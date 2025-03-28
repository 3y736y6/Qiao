import pymysql
import sys

# 数据库配置参数
DB_HOST = '47.109.23.253'  # 数据库主机地址
DB_USER = 'root'  # 数据库用户名
DB_PASSWORD = 'zijipojie'  # 数据库密码
DB_NAME = 'machine1'  # 数据库名称
DB_PORT = 8306  # 数据库端口号

# 要清空的表列表，按照外键依赖关系排列（先清空子表）
TABLES_TO_TRUNCATE = [
    'chart_data'
]


def confirm_action():
    """
    提示用户确认是否继续执行删除操作。
    """
    confirmation = input(
        "您确定要清空以下表的数据吗？\n" + "\n".join(TABLES_TO_TRUNCATE) + "\n请输入 'yes' 继续，或其他键取消：")
    return confirmation.lower() == 'yes'


def clear_tables(cursor):
    """
    清空指定的数据库表，暂时禁用外键检查。
    """
    try:
        print("暂时禁用外键检查...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        for table in TABLES_TO_TRUNCATE:
            print(f"正在清空表 {table} ...")
            cursor.execute(f"TRUNCATE TABLE `{table}`;")
            print(f"表 {table} 已清空。")

        print("重新启用外键检查...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    except pymysql.MySQLError as e:
        print(f"清空表时发生数据库错误: {e}")
        sys.exit(1)


def main():
    if not confirm_action():
        print("操作已取消。")
        sys.exit(0)

    try:
        # 连接到数据库
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False  # 手动提交事务
        )
        cursor = conn.cursor()

        # 清空表数据
        clear_tables(cursor)

        # 提交事务
        conn.commit()
        print("所有指定表的数据已成功清空。")

    except pymysql.MySQLError as e:
        print(f"数据库连接或操作错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生未知错误: {e}")
        sys.exit(1)
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


if __name__ == '__main__':
    main()
