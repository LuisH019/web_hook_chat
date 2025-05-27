from models.chat_app_model import ChatAppModel

if __name__ == "__main__":
    app = ChatAppModel("a", 5000, "b", 5001)
    app.run()