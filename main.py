from api import app, logger

if __name__ == '__main__':
    logger.info("System Started!")
    app.run(debug=True)
