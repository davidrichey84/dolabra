import gunicorn.app.base
import falcon
import json

class Classify(object):
    def __init__(self):
        model = 'utilities/syslog_ner.model'
        try:
            self.ner_model = spacy.load(model)
        except:
            print("Could not locate model!")
            sys.exit(1)

    def on_get(self, req, resp):
        payload = req.media
        try:
            classify_log = ''
            if 'data' in payload:
                classify_log = self.ner_model(payload['data'])
                if classify_log and len(classify_log) > 1:
                    payload = {'results':[]}
                    for item in classify_log.ents:
                        payload['results'].append({item.label_: item.text})
                    resp.body = ujson.dumps(payload)
                    resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        except Exception as e:
            resp.body = str(e)
            resp.status = falcon.HTTP_500

class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

class REST(object):
    def __init__(self, params):
        bind_info = params['bind'].split(":")
        int_bind = bind_info[0]
        port_bind = bind_info[1]
        workers = params['workers', 2]
        options = {'bind': '%s:%s' % (int_bind, port_bind), 'workers': %s % (workers)}
        app = falcon.API()
        classify_log = Classify()
        app.add_route('/api/classify', classify_log)
        StandaloneApplication(app, options).run()