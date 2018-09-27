#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
from app import app
#
# exc_logger = logging.getLogger('Exception')
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# def config_logging():
#     # 配置日志
#     formatter = logging.Formatter(
#         "[%(asctime)s] %(levelname)s - %(message)s")
#     handler = RotatingFileHandler(app.config['LOGPATH'] + 'operator.log', maxBytes=10000000,
#                                   backupCount=50)
#     app.logger.setLevel(logging.INFO)
#     handler.setFormatter(formatter)
#     app.logger.addHandler(handler)
#
#     handler2 = RotatingFileHandler(app.config['LOGPATH'] + '/exception/' + 'operator.log',
#                                    maxBytes=10000000,
#                                    backupCount=50)
#     exc_logger.setLevel(logging.INFO)
#     handler2.setFormatter(formatter)
#     exc_logger.addHandler(handler2)

if __name__ == '__main__':
    # config_logging()
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'], threaded=True)