# https://neuron.yale.edu/neuron/docs/ball-and-stick-model-part-1
from neuron import h
from neuron.units import ms, mV
import matplotlib.pyplot as plt
from neuron import gui

# Load standard run library to give high-level stimulation control functions
h.load_file('stdrun.hoc') 

# Defining cell morphology - ball = soma, stick = dendrite/axon
class BallAndStick():
    """Basic neuron simulation class - contains neuron soma and dendrite"""
    def __init__(self, gid):
        self._gid = gid
        self.morphology()
        self.electrophys()

    def morphology(self):
        self.soma = h.Section(name = 'soma', cell = self)
        self.dend = h.Section(name = 'dend', cell = self)
        self.all = [self.soma, self.dend]
        # Connecting soma and dendrite at loc 0.5
        self.dend.connect(self.soma(0.5)) 
        # Customizing section styles
        self.soma.L = self.soma.diam = 12.6157
        self.dend.L = 200
        self.dend.diam = 1

    def electrophys(self):
        for sec in self.all:
            sec.Ra = 100            # Axial resistance in Ohm * cm
            sec.cm = 1              # Membrane capacitance in micro Farads / cm^2
        # Apply Hodgkin-Huxley membrane dynamics
        self.soma.insert('hh')      
        for seg in self.soma:                                                    
            seg.hh.gnabar = 0.12    # Sodium conductance in S/cm2           
            seg.hh.gkbar = 0.036    # Potassium conductance in S/cm2       
            seg.hh.gl = 0.0003      # Leak conductance in S/cm2          
            seg.hh.el = -54.3       # Reversal potential in mV  
        # Insert passive (leak) current in the dendrite
        self.dend.insert('pas')                                        
        for seg in self.dend:                                  
            seg.pas.g = 0.001  # Passive conductance in S/cm2 
            seg.pas.e = -65    # Leak reversal potential mV

        
    def __repr__(self):
        return 'BallAndStick{}'.format(self._gid)

cell = BallAndStick(2)
h.topology()

# Stimulation
stim = h.IClamp(cell.dend(1))       # Define and position of clamp object
stim.delay = 5
stim.dur = 1
stim.amp = 0.1
soma_v = h.Vector().record(cell.soma(0.5)._ref_v)
dend_v = h.Vector().record(cell.dend(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

# Matplotlib 

plot1 = h.PlotShape(False).plot(plt)
plt.show()

h.finitialize(-65)
h.continuerun(25)
f1 = plt.figure()
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.plot(t, soma_v, linewidth=2)
plt.show()

f = plt.figure()
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
amps = [0.075 * i for i in range(1, 5)]
colors = ['green', 'blue', 'red', 'black']
for amp, color in zip(amps, colors):
    stim.amp = amp
    for cell.dend.nseg, width in [(1, 2), (101, 1)]:
        h.finitialize(-65)
        h.continuerun(25)
        plt.plot(t, list(soma_v),
               linewidth=width,
               label='amp=%g' % amp if cell.dend.nseg == 1 else None,
               color=color)
        plt.plot(t, list(dend_v), '--',
               linewidth=width,
               color=color)
plt.legend()
plt.show()