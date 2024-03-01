from logging.config import dictConfig

def load():
    import os
    if not os.path.exists('logs'):
        os.mkdir('logs')
    dictConfig({
      'version': 1.0, # type: ignore
      'formatters':{
        "standard": {
          'format': '%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s',
          'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
          'format': '%(asctime)s [%(name)s] %(levelname)s  %(message)s',
          'datefmt': '%Y-%m-%d %H:%M:%S',
        }
      },
      'handlers': {
        'console_debug_handler': {
            'level': 'DEBUG',  # 日志处理的级别限制
            'class': 'logging.StreamHandler',  # 输出到终端
            'formatter': 'simple'  # 日志格式
        },
        'access': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'filename': 'logs/access.log',
            'maxBytes': 501 * 1024,
            'backupCount': 50,
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'logs': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'filename': 'logs/logs.log',
            'maxBytes': 128*1024,
            'backupCount': 10,
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
      },
      'loggers':{
        'tornado.access':{
          'handlers': ['console_debug_handler', 'access'],
          'level': 'INFO',
          'propagate': False,
        },
        '':{
          'handlers': ['console_debug_handler', 'logs'],
          'level': 'INFO',
          'propagate': False,
        }
      }
    })
    