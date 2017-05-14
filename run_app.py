# -*- coding: utf-8 -*-
from src.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', port=9000)
