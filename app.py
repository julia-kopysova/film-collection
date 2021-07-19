"""
Module for managing project
"""
import logging


from app import application, urls


if __name__ == "__main__":
    application.debug = True
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    application.run()
