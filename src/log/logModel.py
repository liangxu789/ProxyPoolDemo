import logging

# 创建一个logging对象
logger = logging.getLogger()
# 创建一个屏幕对象
sh = logging.StreamHandler()
# 配置显示格式  可以设置两个配置格式  分别绑定到文件和屏幕上
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
sh.setFormatter(formatter)

logger.addHandler(sh)
logger.setLevel(10)  # 总开关

# requests模块在运行过程中无法记录日志
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

# debug日志
def log_debug(message):
    logging.debug(message)

# info日志
def log_info(message):
    logging.info(message)

#warning日志
def log_warning(message):
    logging.warning(message)

#error日志
def log_error(message):
    logging.error(message)
