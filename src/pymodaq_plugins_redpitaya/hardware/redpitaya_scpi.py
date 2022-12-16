"""SCPI access to Red Pitaya."""

import socket

__author__ = "Luka Golinar, Iztok Jeras"
__copyright__ = "Copyright 2015, Red Pitaya"


class scpi (object):
    """SCPI class (=objet) used to access Red Pitaya over an IP network."""
    # Ceci est la liste des fonctions qui seront reconnu par un objet de class scpi.
    delimiter = '\r\n'

    def __init__(self, host, timeout=None, port=5000):
        """Initialize object and open IP connection.
        Host IP should be a string in parentheses, like '192.168.1.100'.
        """
        self.host    = host
        self.port    = port
        self.timeout = timeout

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if timeout is not None:
                self._socket.settimeout(timeout)

            self._socket.connect((host, port))

        except socket.error as e:
            print('SCPI >> connect({!s:s}:{:d}) failed: {!s:s}'.format(host, port, e))
            raise Exception('not connected')

    def __del__(self):
        if self._socket is not None:
            self._socket.close()
        self._socket = None

    def close(self):
        """Close IP connection."""
        self.__del__()



    def rx_txt(self, chunksize = 4096):
        """Receive text string and return it after removing the delimiter."""
        msg = ''
        while 1:
            chunk = self._socket.recv(chunksize).decode('utf-8') # Receive chunk size of 2^n preferably
            msg += chunk
            if (len(msg) and msg[-2:] == self.delimiter):
                break
        return msg[:-2]

    def rx_arb(self):
        numOfBytes = 0
        """ Recieve binary data from scpi server"""
        str=b''
        while (len(str) != 1):
            str = (self._socket.recv(1))
        if not (str == b'#'):
            return False
        str=b''
        while (len(str) != 1):
            str = (self._socket.recv(1))
        numOfNumBytes = int(str)
        if not (numOfNumBytes > 0):
            return False
        str=b''
        while (len(str) != numOfNumBytes):
            str += (self._socket.recv(1))
        numOfBytes = int(str)
        str=b''
        while (len(str) != numOfBytes):
            str += (self._socket.recv(4096))
        return str

    def tx_txt(self, msg):
        """Send text string ending and append delimiter."""
        return self._socket.sendall((msg + self.delimiter).encode('utf-8')) # was send(().encode('utf-8'))

    def txrx_txt(self, msg):
        """Send/receive text string."""
        self.tx_txt(msg)
        return self.rx_txt()

# IEEE Mandated Commands

    def cls(self):
        """Clear Status Command"""
        return self.tx_txt('*CLS')

    def ese(self, value: int):
        """Standard Event Status Enable Command"""
        return self.tx_txt('*ESE {}'.format(value))

    def ese_q(self):
        """Standard Event Status Enable Query"""
        return self.txrx_txt('*ESE?')

    def esr_q(self):
        """Standard Event Status Register Query"""
        return self.txrx_txt('*ESR?')

    def idn_q(self):
        """Identification Query"""
        return self.txrx_txt('*IDN?')

    def opc(self):
        """Operation Complete Command"""
        return self.tx_txt('*OPC')

    def opc_q(self):
        """Operation Complete Query"""
        return self.txrx_txt('*OPC?')

    def rst(self):
        """Reset Command"""
        return self.tx_txt('*RST')

    def sre(self):
        """Service Request Enable Command"""
        return self.tx_txt('*SRE')

    def sre_q(self):
        """Service Request Enable Query"""
        return self.txrx_txt('*SRE?')

    def stb_q(self):
        """Read Status Byte Query"""
        return self.txrx_txt('*STB?')

# :SYSTem

    def err_c(self):
        """Error count."""
        return self.txrx_txt('SYST:ERR:COUN?')

    def err_c(self):
        """Error next."""
        return self.txrx_txt('SYST:ERR:NEXT?')

###################### Fonctions perso #######################"

    def prep_acq(self, decimation: int = 1):
        """Prepare the Red Pitaya board to the acquisition """
        # s'assurer que l'argument est bien un entier entre 1 et 16 du log de 2 de l'argument
        self.tx_txt('ACQ:RST')
        self.tx_txt(f'ACQ:DEC {decimation}')
        self.tx_txt(f'ACQ:TRI:LEV 0.5')

        self.start_analog_gen()


    def start_analog_acq(self):
        """ Start the acquisition of the signal and return it into a list of float"""
                              #Lance l'aquisition
        self.tx_txt('ACQ:TRIG 1')                     #Active le trigger instantanément
        self.tx_txt('ACQ:START')

    def start_analog_gen(self):
        wave_form = 'sine'
        freq = 500
        ampl = 1

        self.tx_txt('GEN:RST')

        self.tx_txt('SOUR1:FUNC ' + str(wave_form).upper())
        self.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
        self.tx_txt('SOUR1:VOLT ' + str(ampl))

        # Enable output
        self.tx_txt('SOUR1:TRIG:INT')
        self.tx_txt('OUTPUT1:STATE ON')

    def test_ready(self):
        self.tx_txt('ACQ:TRIG:STAT?')            # Demande le statut du trigger --> TD ou WAIT
        return self.rx_txt() == 'TD'                # si cela renvoie TD, alors il est activé et on break pour sortir du while

    def get_data(self, source: int = 1):
        #verifier si la source est bien 1 ou 2 sinon erreur
        #le buffer du redpitaya est de 16384 valeurs
        self.tx_txt(f'ACQ:SOUR{source}:DATA?')  # Lit le buffer entier de l'entrée 1, en commencant par le plus vieux échantillons (celui juste après le trigger)
        buff_string = self.rx_txt()  # On crée une variable buff_string de type string

        buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
        # avec .strip on retire les caractères {}\n\r du texte (correspond aux délimiteurs du texte
        # avec .replace permet de remplacer un espace par une zone de texte vide (On supprime les espaces)
        # avec .split on sépare la chaine de texte en une liste en spécifiant que le séparateur à prendre en compte pour la création de la liste est la virgule

        buff = list(map(float,buff_string))
        # création d'une liste "buff" de float à partir de la liste "buff_string" contenant des chaines de caractères
        # map permet de convertir un à un en float les éléments de la liste en faisant float(élément1) puis float(élément2) etc.
        # "list" convertie l'objet map en une liste

        return buff

    def stop_analog_acq(self):
        """ Start the acquisition of the signal"""
        self.tx_txt('ACQ:STOP')
