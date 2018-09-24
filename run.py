# -*- coding: utf-8 -*-
# Run a test server.
from app import app
import models

models.db.connect(allow_auto_upgrade=True, **app.config['DB_PARAMS'])

if __name__ == '__main__':
    app.run(debug=True)