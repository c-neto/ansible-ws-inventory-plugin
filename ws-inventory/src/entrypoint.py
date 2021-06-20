import controllers
import conf


if __name__ == "__main__":
    conf.set_log_level(conf.settings['LOG_LEVEL'])
    controllers.run()
