import numpy as np
from easydict import EasyDict as edict
from pymodaq.utils.daq_utils import ThreadCommand, getLineInfo
from pymodaq.utils.data import DataFromPlugins, Axis
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter
from pymodaq_plugins_redpitaya.hardware.redpitaya_scpi import scpi


class DAQ_1DViewer_Redpitaya(DAQ_Viewer_base):
    """
    """
    params = comon_parameters+[
        ## TODO for your custom plugin
        # elements to be added here as dicts in order to control your custom stage
        ############
        ]

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller: scpi = None
        # Besoin de mettre "redpitaya_scpi.py" ici ??

        # TODO declare here attributes you want/need to init with a default value

        self.x_axis = None

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "a_parameter_you've_added_in_self.params":
           self.controller.your_method_to_apply_this_param_change()
#        elif ...
        ##

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        self.ini_detector_init(old_controller=controller,
                               new_controller=scpi('169.254.168.242'))
        # On définit un nouvel objet de type scpi que l'on appel controller, il représente notre carte d'acquisition


        # note: you could either emit the x_axis once (or a given place in the code) using self.emit_x_axis() as shown
        # above. Or emit it at every grab filling it the x_axis key of DataFromPlugins)
        info = self.controller.idn_q()
        initialized = True
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        self.controller.close()

    def prepare_acquisition(self):
        self.controller.prep_acq()


    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        ## TODO for your custom plugin
        self.prepare_acquisition()
        ##synchrone version (blocking function)
        data_tot = self.controller.start_analog_acq()




        self.data_grabed_signal.emit([DataFromPlugins(name='Mock1', data=[np.array(data_tot)],
                                                      dim='Data1D', labels=['dat0'],
                                                      x_axis=Axis())])
        # note: you could either emit the x_axis once (or a given place in the code) using self.emit_x_axis() as shown
        # above. Or emit it at every grab filling it the x_axis key of DataFromPlugins, not shown here)

        ##asynchrone version (non-blocking function with callback)
        #self.controller.your_method_to_start_a_grab_snap(self.callback)
        # on en a pas besoin ??

        #########################################################

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        self.controller.stop_analog_acq()
        return ''


if __name__ == '__main__':
    main(__file__)