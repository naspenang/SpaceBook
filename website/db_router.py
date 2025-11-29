class MainRouter:
    route_app_labels = {"website"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "main"
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "main"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels
            and obj2._meta.app_label in self.route_app_labels
        ):
            return True
        if (
            obj1._meta.app_label not in self.route_app_labels
            and obj2._meta.app_label not in self.route_app_labels
        ):
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == "main"
        return db == "default"
