class Repository:
    def __init__(self, name, id, auto_delete_head_bool, protection_rules = None):
        self.name = name
        self.id = id
        self.auto_delete_head_bool = auto_delete_head_bool
        
        if protection_rules is not None:
            self.protection_rules = protection_rules