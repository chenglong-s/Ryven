from NIENV import *
from ..ryvencore.src.ryvencore import Node
from ..ryvencore.src.NodePort import NodeInput, NodeOutput


class SetVar_Node(Node):

    title = 'set var'
    description = 'sets the value of a script variable'
    init_inputs = [
        NodeInput(type_='exec'),
        NodeInput(type_='data', label='var',
                 widget='std line edit m', widget_pos='besides'),
        NodeInput(type_='data', label='val',
                 widget='std line edit m', widget_pos='besides')
    ]
    init_outputs = [
        NodeOutput(type_='exec'),
        NodeOutput(type_='data', label='val')
    ]
    style = 'extended'
    color = '#c69a15'

    def __init__(self, params):
        super(SetVar_Node, self).__init__(params)

        self.special_actions['make passive'] = {'method': M(self.action_make_passive)}
        self.active = True

        self.var_name = ''

    def update_event(self, input_called=-1):
        if self.active and input_called == 0:
            self.var_name = self.input(1)
            if self.set_var_val(self.input(1), self.input(2)):
                self.set_output_val(1, self.input(2))
            self.exec_output(0)
        elif not self.active:
            self.var_name = self.input(0)
            if self.set_var_val(self.input(0), self.input(1)):
                self.set_output_val(0, self.get_var_val(self.var_name))


    def action_make_passive(self):
        self.active = False
        self.delete_input(0)
        self.delete_output(0)
        del self.special_actions['make passive']
        self.special_actions['make active'] = {'method': M(self.action_make_active)}

    def action_make_active(self):
        self.active = True
        self.create_input('exec', '', pos=0)
        self.create_output('exec', '', pos=0)
        del self.special_actions['make active']
        self.special_actions['make passive'] = {'method': M(self.action_make_passive)}

    def get_data(self):
        return {'active': self.active}

    def set_data(self, data):
        self.active = data['active']

    def remove_event(self):
        pass