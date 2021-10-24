import uuid
from app import App


def main():
    miner_id = str(uuid.uuid4())
    app = App(miner_id)
    app.cmdloop()


if __name__ == '__main__':
    main()
