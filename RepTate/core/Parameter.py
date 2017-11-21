import enum
import math

class ShiftType(enum.Enum):
    linear=0
    log=1

class ParameterType(enum.Enum):
    real = 0
    integer = 1
    discrete = 2

class Parameter(object):
    """Abstract class to describe theory parameters

        Args:
            name            (str): Parameter name
            description     (str): Meaning of parameter
            type           (enum): Type of parameter (real, integer, discrete)
            value          (real): Value of parameter
            min_flag       (bool): Is this parameter optimized?
            min_factor     (real): Factor to scale this parameter during minimization
            min_shift_type (user): How do we shift this parameter during minimization
            bracketed      (bool): Is the parameter bracketed?
            min_value      (real): Minimum allowed value for the parameter
            max_value      (real): Maximum allowed value
    """
    def __init__(self, name="", value=0.0, description="", type=ParameterType.real, 
                 min_flag=True, min_factor=1.0, min_shift_type=ShiftType.linear, 
                 bracketed = False, min_value=-math.inf, max_value=math.inf):
        self.name=name
        self.description=description
        self.type = type
        if (self.type==ParameterType.real):
            self.value=float(value)
        elif (self.type==ParameterType.integer):
            self.value=int(value)
        else:
            pass # NOT IMPLEMENTED YET
        self.error=math.inf
        self.min_flag = min_flag
        self.min_factor = min_factor
        self.min_shift_type = min_shift_type
        self.bracketed = bracketed
        self.min_value = min_value
        self.max_value= max_value
        self.min_allowed = min_flag

    def copy(self, par2):
        """ Copy the contents of another paramter"""
        self.name=par2.name
        self.description=par2.description
        self.type = par2.type
        self.value=par2.value
        self.min_flag = par2.min_flag
        self.min_factor = par2.min_factor
        self.min_shift_type = par2.min_shift_type
        self.bracketed = par2.bracketed
        self.min_value = par2.min_value
        self.max_value= par2.max_value
        
    def __str__(self):
        """
        .. todo:: Refine this.
        """
        return "%s=%g"%(self.name,self.value)

    def __repr__(self):
        """
        .. todo:: Refine this.
        """
        return "Parameter(\"%s\",%g,\"%s\",%s,%s,%g,%s,%s,%g,%g)"%(self.name,self.value,self.description, self.type, self.min_flag,\
                self.min_factor, self.min_shift_type, self.bracketed, self.min_value, self.max_value)
