from app import app, socketIo

if __name__ == '__main__':
    socketIo.run(app)
