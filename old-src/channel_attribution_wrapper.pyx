# distutils: language = c++
# distutils: sources = ChannelAttribution.h


cdef extern from "ChannelAttribution.h" namespace "pychattr":
    cdef cppclass Fx:
        pass

