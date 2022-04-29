from parseChannel import Parser
import schedule
import time

if __name__ == '__main__':
    parser = Parser()
    parser.initialize()
    schedule.every().week.do(parser.update_information)

    while True:
        schedule.run_pending()
        time.sleep(1)
