from models.chat_app_model import ChatAppModel

if __name__ == "__main__":
    app = ChatAppModel("b", 5001, "a", 5000)
    app.run()