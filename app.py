"""
Module for managing project
"""
import logging


from app import application, urls

from app.swagger import swaggerui_blueprint


if __name__ == "__main__":
    application.debug = True
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    application.register_blueprint(swaggerui_blueprint)
    application.run(debug=True, host='0.0.0.0', port=5000, use_debugger=False, use_reloader=False)
